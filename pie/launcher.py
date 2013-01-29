" Entry point module for interpreting "

import os
from pie.interpreter.sourcecode import SourceCode
from pie.interpreter.context import Context
from pie.interpreter.frame import Frame
from pie.interpreter.errors.base import PieError


def run(filename):
    try:
        source = SourceCode(filename)
        source.open()
    except OSError:
        os.write(2, "Could not open input file: %s\n" % filename)
        return 1

    try:
        context = Context(filename)
        source.interpret(context, Frame())
    except PieError as e:
        os.write(2, e.get_message())
        return 1

    return 0
