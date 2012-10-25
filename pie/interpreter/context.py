__author__ = 'sery0ga'

class Context:

    def __init__(self):
        self.functions = {}

        # trace data
        self.function_trace_stack = []

    def initialize_functions(self, bytecode):
        for name, object in bytecode.functions.iteritems():
            self.functions[name] = object

    def initialize_function_trace_stack(self, filename):
        """
        Inserts {main} trace call to empty stack
        """
        self.function_trace_stack.append(("{main}", 0, filename))