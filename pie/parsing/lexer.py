from pie.parsing import regex
from pypy.rlib.parsing.lexer import Lexer, SourcePos, Token

class PieLexer(Lexer):
    " Special lexer for php files, adds processing of inline html content "

    IGNORED_TOKES = ["T_WHITESPACE",
                     "T_COMMENT",
                     "T_INLINE_COMMENT",
                     "T_DOC_COMMENT"]

    def __init__(self, token_regexs, names):
        self.token_regexs = token_regexs
        self.names = names
        self.rex = regex.PieLexingOrExpression(token_regexs, names)
        automaton = self.rex.make_automaton()
        self.automaton = automaton.make_deterministic(names)
        self.automaton.optimize() # XXX not sure whether this is a good idea
        for ign in self.IGNORED_TOKES:
            assert ign in names
        self.ignore = dict.fromkeys(self.IGNORED_TOKES)
        self.matcher = self.automaton.make_lexing_code()

    def tokenize(self, text, eof=False):
        pre_parsed_tokens = self.get_pre_tokenizer(text).get_tokens()

        tokens = []
        for token in pre_parsed_tokens:
            if token.name == PiePreTokenizer.PHP_CODE_TOKEN:
                grammar_tokens = self.tokenize_with_grammar(token)
                tokens.extend(grammar_tokens)
            else:
                tokens.append(token)

        return tokens

    def tokenize_with_grammar(self, token):
        " Return a list of Token's from text. "
        runner = self.get_runner(token.source, eof=False)
        runner.lineno = token.source_pos.lineno
        runner.columnno = token.source_pos.columnno
        result = []
        while 1:
            try:
                tok = runner.find_next_token()
                result.append(tok)
            except StopIteration:
                break

        return result

    def get_pre_tokenizer(self, text):
        return PiePreTokenizer(text)


class PiePreTokenizer(object):
    " Class, creating code/notcode tokens "

    PHP_OPEN_TAG = "<?php"
    PHP_CLOSE_TAG = "?>"

    # list of tokens, produced by pre-tokenizer
    INHLINE_HTML_TOKEN = "T_INLINE_HTML"
    OPEN_TAG_TOKEN = "T_OPEN_TAG"
    CLOSE_TAG_TOKEN = "T_CLOSE_TAG"
    PHP_CODE_TOKEN = "PHP_CODE"
    EOF_TOKEN = "EOF"

    def __init__(self, text):
        self.tokens = []
        self.text = text
        self.text_lowered = self.text.lower()

        self.is_html = True # text is treated as html in the begining
        self.last_start= 0
        self.line = 0
        self.column = 0

    def get_tokens(self):
        if len(self.tokens) == 0:
            self.run()

        return self.tokens

    def run(self):
        open_tag_length = len(self.PHP_OPEN_TAG)
        close_tag_length = len(self.PHP_CLOSE_TAG)

        while True:
            if self.is_html:
                index = self.text_lowered.find(self.PHP_OPEN_TAG,
                                               self.last_start)
            else:
                index = self.text_lowered.find(self.PHP_CLOSE_TAG,
                                               self.last_start)

            if index < 0:
                # no needed tag found: end of file
                break

            self.add_content_token(index)
            if self.is_html:
                self.add_open_tag_token()
                index += open_tag_length
            else:
                self.add_close_tag_token()
                index += close_tag_length

            self.last_start = index
            self.is_html = not self.is_html

        if self.last_start < len(self.text):
            # adding last token
            self.add_content_token(len(self.text))

        if not self.is_html:
            # in case code does not ends with close tag, we will
            # explicitly add it for easier parsing
            self.add_close_tag_token()

        self.add_token(self.EOF_TOKEN, "EOF")

    def add_content_token(self, index):
        if index == self.last_start:
            return

        token = self.text[self.last_start: index]

        if self.is_html:
            if len(self.tokens) > 0 and token[0] == "\n":
                # PHP parser ignores first newline symbol after close tag,
                # so we are doing the same
                self.adjust_position("\n")
                if len(token) == 1:
                    return

                token = token[1:]

            self.add_token(self.INHLINE_HTML_TOKEN, token)
        else:
            self.add_token(self.PHP_CODE_TOKEN, token)

    def add_open_tag_token(self):
        self.add_token(self.OPEN_TAG_TOKEN, self.PHP_OPEN_TAG)

    def add_close_tag_token(self):
        self.add_token(self.CLOSE_TAG_TOKEN, self.PHP_CLOSE_TAG)

    def add_token(self, name, text):
        position = SourcePos(self.last_start, self.line, self.column)
        token = Token(name, text, position)
        self.tokens.append(token)
        self.adjust_position(text)

    def adjust_position(self, text):
        newlines = text.count("\n")
        self.line += newlines
        if newlines == 0:
            self.column += len(text)
        else:
            self.column = text.rfind("\n")
