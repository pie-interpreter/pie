__author__ = 'sery0ga'

class Frame:

    def __init__(self):
        self.stack = []
        self.variables = {}
        self.names = {}

        # trace data
        self.function_trace_stack = []