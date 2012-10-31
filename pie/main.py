from pie.error import InterpreterError, PHPError
from pie.interpreter.context import Context
from pie.interpreter.frame import Frame
from pie.objspace import ObjSpace
from pie.parsing.parsing import interpret_file, InterpretedFile
from pypy.rlib.parsing.deterministic import LexerError
from pypy.rlib.parsing.parsing import ParseError
from pypy.rlib.streamio import open_file_as_stream
import sys


def entry_point(argv):
    if len(argv) < 2:
        print 'No input file provided'
        return 1

    file = InterpretedFile(argv[1])
    input_file = open_file_as_stream(file.filename)
    file.data = input_file.readall()
    input_file.close()

    try:
        context = Context()
        context.initialize_function_trace_stack(file.filename)
        interpret_file(file, context, Frame())
    except PHPError as e:
        print e.print_message()
        return 1
    except InterpreterError as e:
        print e
        return 1
    except LexerError as e:
        print e.nice_error_message(file.filename)
        return 1
    except ParseError as e:
        print e.nice_error_message(file.filename, file.data)
        return 1

    return 0

if __name__ == '__main__':
    entry_point(sys.argv)