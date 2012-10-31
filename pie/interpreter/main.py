"""
Entry point module for interpreting
"""

from pie.error import PHPError, InterpreterError
from pie.interpreter import interpreter
from pypy.rlib.parsing.deterministic import LexerError
from pypy.rlib.parsing.parsing import ParseError
from pypy.rlib.streamio import open_file_as_stream


def run(filename):
    source = create_source_from_filename(filename)
    try:
        interpreter.interpret(source)
    except PHPError as e:
        print e.print_message()
        return 1
    except InterpreterError as e:
        print e
        return 1
    except LexerError as e:
        print e.nice_error_message(source.filename)
        return 1
    except ParseError as e:
        print e.nice_error_message(source.filename, source.data)
        return 1

    return 0


def create_source_from_filename(filename):
    " Create source object from filename "

    input_file = open_file_as_stream(filename)
    data = input_file.readall()

    return InterpretedSource(data, filename)


class InterpretedSource(object):

    def __init__(self, data, filename):
        self.data = data
        self.filename = filename