__author__ = 'sery0ga'

import sys
from pypy.rlib.streamio import open_file_as_stream
from pypy.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
from pypy.rlib.parsing.parsing import *

def entry_point(argv):
    if len(argv) < 2:
        print __doc__
        return 1
    filename = argv[1]
    file = open_file_as_stream(filename)
    data = file.readall()
    file.close()

    file = open_file_as_stream('grammar.txt')
    grammar = file.readall()
    file.close()
    regexs, rules, ToAST = parse_ebnf(grammar)
    parser = make_parse_function(regexs, rules, eof=True)
    try:
        parser(data)
        print "OK"
    except ParseError, a:
        print a.nice_error_message(filename, data)


if __name__ == '__main__':
    entry_point(sys.argv)