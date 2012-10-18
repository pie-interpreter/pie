import os
from astnodes import *

__author__ = 'sery0ga'

class InterpreterError(Exception):
    pass

class Interpreter:

    def __init__(self):
        pass

    def interpret(self, code):
        for block in code.blocks:
            if isinstance(block, Statement):
                if isinstance(block.expression, Echo):
                    self.echo(block.expression)

    def echo(self, echo):
        if isinstance(echo.expression, BinOp):
            value = self.bin_op(echo.expression)
        else:
            value = echo.expression.value
        # XXX extra copy of the string if mutable
        os.write(1, str(value))

    def bin_op(self, binaryOp):
        if binaryOp.op == '+':
            return binaryOp.left.value + binaryOp.right.value
        elif binaryOp.op == '-':
            return binaryOp.left.value - binaryOp.right.value
        else:
            raise NotImplementedError