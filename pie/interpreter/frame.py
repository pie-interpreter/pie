__author__ = 'sery0ga'

class Frame:

    def __init__(self):
        self.stack = []
        self.variables = {}
        self.names = {}

        # trace data
        self.function_trace_stack = []

    def initialize_function_trace_stack(self, filename):
        """
        Inserts {main} trace call to empty stack
        """
        if len(self.function_trace_stack):
            return
        self.function_trace_stack.append(("{main}", 0, filename))