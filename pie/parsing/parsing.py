from pie.parsing.lexer import PieLexer
from pypy.rlib.parsing.ebnfparse import parse_ebnf, check_for_missing_names
from pypy.rlib.parsing.parsing import PackratParser, ParseError
import os
import py


def parse(source):
    """ Parse php code """
    parse_tree = parse_php(source.data)
    parse_tree = transformer.transform(parse_tree)

    return parse_tree


def get_parse_tools():
    grammar = get_grammar_file()
    try:
        regexs, rules, transformer_class = parse_ebnf(grammar)
    except ParseError as e:
        print e.nice_error_message("grammar.ebnf", grammar)
        raise e

    names, regexs = zip(*regexs)
    check_for_missing_names(names, regexs, rules)

    lexer = PieLexer(list(regexs), list(names))
    parser = PackratParser(rules, rules[0].nonterminal)

    def parse(s):
        tokens = lexer.tokenize(s)
        s = parser.parse(tokens)
        return s

    return parse, transformer_class()


def get_grammar_file():
    currentDir = os.path.dirname(os.path.abspath(__file__))
    grammar = py.path.local(currentDir).join('grammar.ebnf').read("rt")

    return grammar


parse_php, transformer = get_parse_tools()
