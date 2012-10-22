from pie.ast.building import build
from pie.compiling import compile_ast
from pie.frame import Frame
from pie.interpreter import Interpreter
from pie.objspace import ObjSpace
from pie.parsing import parsing
from pypy.rlib.parsing.parsing import ParseError
from pypy.rlib.streamio import open_file_as_stream
import sys

def entry_point(argv):
    if len(argv) < 2:
        print 'No input file provided'
        return 1

    input_file = open_file_as_stream(argv[1])
    data = input_file.readall()
    input_file.close()

    try:
        parseTree = parsing.parse(data)
        parseTree.view()
#        ast = build(parseTree)
#        bytecode = compile_ast(ast)
#        objSpace = ObjSpace()
#        Interpreter().interpret(objSpace, Frame(), bytecode)

    except ParseError as e:
        print e.nice_error_message(argv[1], data)
        return 1

    return 0

if __name__ == '__main__':
    entry_point(sys.argv)