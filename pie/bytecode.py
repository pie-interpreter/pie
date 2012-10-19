__author__ = 'sery0ga'

class Bytecode(object):
    """
    Contains data after AST was compiled.

    Contains enough data to run code on interpreter
    """

    def __init__(self):
        self.consts = []
        self.code = []

    def const(self, index):
        return self.consts[index]