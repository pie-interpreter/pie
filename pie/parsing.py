from pypy.rlib.parsing.ebnfparse import parse_ebnf, check_for_missing_names
from pypy.rlib.parsing.lexer import Lexer, Token, SourcePos
from pypy.rlib.parsing.parsing import PackratParser, ParseError
import os
import py

def parse(data):
    " Parse php code "
    parseTree = parser.parse(data)
    return parseTree


class PHPParser(object):
    " Parser of php contained files "

    def parse(self, data):
        result = parse_php(data)
        result = transformer.transform(result)
        return result

    def get_parse_tools(self):
        grammar = self.get_grammar_file()
        try:
            regexs, rules, transformer_class = parse_ebnf(grammar)
        except ParseError as e:
            print e.nice_error_message("grammar.ebnf", grammar);
            raise e

        names, regexs = zip(*regexs)
        check_for_missing_names(names, regexs, rules)

        ignore = ["IGNORE"]
        if "IGNORE" not in names:
            ignore = []

        lexer = PHPLexer(list(regexs), list(names), ignore=ignore)
        parser = PackratParser(rules, rules[0].nonterminal)
        def parse(s):
            tokens = lexer.tokenize(s, eof=True)
            s = parser.parse(tokens)
            return s

        return parse, transformer_class()


    def get_grammar_file(self):
        currentDir = os.path.dirname(os.path.abspath(__file__))
        grammar = py.path.local(currentDir).join('../grammar.ebnf').read("rt")

        return grammar

class PHPLexer(Lexer):
    """ Special lexer for php files, adds processing of inline html content """

    def tokenize(self, text, eof=False):
        pre_parsed_tokens = self.get_pre_tokenizer(text).run()

        tokens = []
        for token in pre_parsed_tokens:
            if token.name == "PHP_CODE":
                grammar_tokens = self.tokenize_with_grammar(token, eof=False)
                tokens.extend(grammar_tokens)
            else:
                tokens.append(token)

        return tokens

    def tokenize_with_grammar(self, token, eof=False):
        """Return a list of Token's from text."""
        r = self.get_runner(token.source, eof)
        r.lineno = token.source_pos.lineno
        r.columnno = token.source_pos.columnno
        result = []
        while 1:
            try:
                tok = r.find_next_token()
                result.append(tok)
            except StopIteration:
                break
        return result

    def get_pre_tokenizer(self, text):
        return PHPPreTokenizer(text)


class PHPPreTokenizer(object):
    "Class, creating code/notcode tokens"

    PHP_START_TAG = "<?php"
    PHP_END_TAG = "?>"

    def __init__(self, text):
        self.text = text
        self.iscode = False
        self.laststart= 0
        self.lineno = 0
        self.columnno = 0

    def run(self):
        tokens = []
        self.laststart = 0
        while True:
            if self.iscode:
                index = self.text.find(self.PHP_END_TAG, self.laststart)
                if index > 0:
                    index += 2 # we need end tag in the code token
            else:
                index = self.text.find(self.PHP_START_TAG, self.laststart)

            if index < 0:
                break

            if index == self.laststart:
                self.iscode = not self.iscode
                continue

            tokens.append(self.create_token(self.text[self.laststart: index]));

            self.laststart = index
            self.iscode = not self.iscode

        if self.laststart < len(self.text):
            tokens.append(self.create_token(
                            self.text[self.laststart: len(self.text)]
                         ))

        tokens.append(Token("EOF", "EOF",
                            SourcePos(self.laststart,
                                      self.lineno,
                                      self.columnno)
                            ))

        return tokens

    def create_token(self, text):
        if self.iscode:
            name = "PHP_CODE"
        else:
            name = "T_INLINE_HTML"

        token = Token(name,
                      text,
                      SourcePos(self.laststart, self.lineno, self.columnno))
        self.adjust_position(text)

        return token

    def adjust_position(self, text):
        newlines = text.count("\n")
        self.lineno += newlines
        if newlines == 0:
            self.columnno += len(text)
        else:
            self.columnno = text.rfind("\n")


parser = PHPParser()
parse_php, transformer = parser.get_parse_tools()