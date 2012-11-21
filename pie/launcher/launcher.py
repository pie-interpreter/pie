"""
Entry point module for interpreting
"""
from pie.error import InterpreterError
from pie.launcher.config import config
from pie.interpreter.context import Context
from pie.interpreter.sourcecode import SourceCode
from pie.interpreter.frame import Frame

def run(filename):
    config.set_calling_file(filename)

    try:
        source = SourceCode(filename, "{main}")
        source.open()
    except OSError:
        print "Could not open input file: %s" % filename
        return 1
    try:
        source.compile()
        context = Context(config)
        source.interpret(context, Frame())
    except InterpreterError:
        return 1

    return 0
