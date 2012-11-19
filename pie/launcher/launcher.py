"""
Entry point module for interpreting
"""
from pie.error import InterpreterError
from pie.launcher.config import config
from pie.interpreter.context import Context
from pie.interpreter.sourcecode import SourceCode, interpret_bytecode

def run(filename):
    config.set_calling_file(filename)

    try:
        source = SourceCode(filename)
        source.open()
    except OSError:
        print "Could not open input file: %s" % filename
        return 1
    try:
        context = Context(config)
        bytecode = source.compile()
        context.initialize_functions(bytecode)
        context.trace.append("{main}", bytecode)
        interpret_bytecode(bytecode, context)
    except InterpreterError:
        return 1

    return 0
