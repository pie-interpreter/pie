__author__ = 'sery0ga'

class Bytecode(object):
    """
    Contains data after AST was compiled.
    Contains enough data to run code on interpreter
    """

    def __init__(self):
        self.consts = []
        self.code = ""

    def __repr__(self):
        return "Code: %s\nConstants number: %s" % (self.code, len(self.consts))