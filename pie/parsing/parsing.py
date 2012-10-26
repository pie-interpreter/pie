from pie.ast.building import build
from pie.compiling.compiling import compile_ast
from pie.interpreter.interpreter import Interpreter
from pie.parsing.lexer import PieLexer
from pypy.rlib.parsing.ebnfparse import parse_ebnf, check_for_missing_names
from pypy.rlib.parsing.parsing import PackratParser, ParseError
import os
import py


def interpretFile(filename, data, context, objspace, frame):
    """ Parse and interpret one code file
    """
    parseTree = parse(data)
    ast = build(parseTree)
    bytecode = compile_ast(ast, filename)
    Interpreter(objspace, context).interpret(frame, bytecode)

def parse(data):
    """ Parse php code """
    parseTree = parse_php(data)
    parseTree = transformer.transform(parseTree)

    return parseTree


def get_parse_tools():
    grammar = get_grammar_file()
    try:
        regexs, rules, transformer_class = parse_ebnf(grammar)
    except ParseError as e:
        print e.nice_error_message("grammar.ebnf", grammar);
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
