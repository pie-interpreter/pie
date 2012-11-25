"""
Entry point module for interpreting
"""
from pie.error import InterpreterError
from pie.interpreter.context import Context
from pie.interpreter.sourcecode import SourceCode
from pie.interpreter.frame import Frame


def run(filename):

    try:
        source = SourceCode(filename)
        source.open()
    except OSError:
        print "Could not open input file: %s" % filename
        return 1

    try:
        source.compile()
        context = Context(filename)
        source.interpret(context, Frame())
    except InterpreterError:
        return 1

    return 0
