from pie.compiling import compiling
from pie.interpreter.frame import Frame
from pie.error import LexerError, PieError, InterpreterError
import interpreter
from pypy.rlib.parsing.parsing import ParseError
from pypy.rlib.streamio import open_file_as_stream

__author__ = 'sery0ga'


class SourceCode(object):

    def __init__(self, name, data=''):
        self.filename = name
        self.data = data

    def open(self):
        " Create source object from filename "
        input_file = open_file_as_stream(self.filename)
        self.data = input_file.readall()

    def compile(self):
        try:
            bytecode = compiling.compile_source(self)
        except LexerError as e:
            print e.nice_error_message(self.filename)
            raise PieError()
        except ParseError as e:
            print e.nice_error_message(self.filename, self.data)
            raise PieError()
        return bytecode


def interpret_function(bytecode, context, frame=None):
    if frame is None:
        frame = Frame()
    interpreter_object = interpreter.Interpreter(bytecode, context, frame)
    try:
        return interpreter_object.interpret()
    except InterpreterError:
        raise PieError()

def interpret_bytecode(bytecode, context, frame=None):
    if frame is None:
        frame = Frame()
    interpreter_object = interpreter.Interpreter(bytecode, context, frame)
    try:
        return interpreter_object.interpret()
    except InterpreterError:
        raise PieError()
