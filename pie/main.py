from pie.interpreter import Interpreter
from pie.parsing import buildAst
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
        result = buildAst(data)
        interpreter = Interpreter()
        interpreter.interpret(result)
    except ParseError as e:
        print e.nice_error_message(argv[1], data)
        return 1

    return 0

if __name__ == '__main__':
    entry_point(sys.argv)