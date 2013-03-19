from rpython.rlib.streamio import open_file_as_stream

from pie.compiling import compiling
from pie.objspace import space
from pie.interpreter.errors.base import PieError

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

    def interpret(self, context, frame):
        if not self.bytecode:
            try:
                self.bytecode = compiling.compile_source(self)
            except PieError as e:
                e.context = context
                e.handle()
                return space.bool(False)

        from pie.interpreter.interpreter import Interpreter
        Interpreter(self.bytecode, context, frame).interpret()

        # TODO: as debug_trace function appear, a test for
        # this path should appear too
        if frame.stack:
            return frame.stack.pop()
        else:
            return space.null()
