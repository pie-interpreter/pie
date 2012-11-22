from pie.compiling import compiling
from pie.interpreter.frame import Frame
from pie.error import LexerError, PieError, InterpreterError
import interpreter
from pypy.rlib.parsing.parsing import ParseError
from pypy.rlib.streamio import open_file_as_stream

__author__ = 'sery0ga'


class SourceCode(object):

    def __init__(self, filename):
        self.filename = filename
        self.content = ''
        self.bytecode = None

    def open(self):
        " Create source object from filename "
        input_file = open_file_as_stream(self.filename)
        self.content = input_file.readall()

    def compile(self):
        try:
            self.raw_compile()
        except LexerError as e:
            print e.nice_error_message(self.filename)
            raise PieError()
        except ParseError as e:
            print e.nice_error_message(self.filename, self.content)
            raise PieError()

    def raw_compile(self):
        self.bytecode = compiling.compile_source(self)

    def interpret(self, context, frame, function_code_called_from=''):
        context.trace.append(function_code_called_from, self.bytecode)
        context.initialize_functions(self.bytecode)
        interpreter_object = interpreter.Interpreter(self.bytecode, context, frame)
        try:
            return_value = interpreter_object.interpret()
            #TODO: as debug_trace function appear, a test for this path should appear too
            context.trace.pop()
            return return_value
        except InterpreterError:
            context.trace.pop()
            raise PieError()


def interpret_function(bytecode, context, frame=None):
    if frame is None:
        frame = Frame()
    interpreter_object = interpreter.Interpreter(bytecode, context, frame)
    try:
        return interpreter_object.interpret()
    except InterpreterError:
        raise PieError()
