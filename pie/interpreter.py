import os
from parser import Echo

__author__ = 'sery0ga'

class InterpreterError(Exception):
    pass

class Interpreter:

    def __init__(self):
        pass

    def interpret(self, code):
        for statement in code.statements:
            if isinstance(statement, Echo):
                self.echo(statement)

    def echo(self, echo):
        # XXX extra copy of the string if mutable
        os.write(1, str(echo.expression.value))