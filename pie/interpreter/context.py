__author__ = 'sery0ga'

class Context:

    def __init__(self):
        self.functions = {}

    def initialize_functions(self, bytecode):
        for name, object in bytecode.functions.iteritems():
            self.functions[name] = object