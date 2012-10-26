from pie.error import InterpreterError, PHPError
from pie.interpreter.context import Context
from pie.interpreter.frame import Frame
from pie.objspace import ObjSpace
from pie.parsing.parsing import interpretFile
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
        context = Context()
        context.initialize_function_trace_stack(argv[1])
        interpretFile(argv[1], data, context, ObjSpace(), Frame())
    except PHPError as e:
        print e
        return 1
    except InterpreterError as e:
        print e
        return 1
    except ParseError as e:
        print e.nice_error_message(argv[1], data)
        return 1

    return 0

if __name__ == '__main__':
    entry_point(sys.argv)