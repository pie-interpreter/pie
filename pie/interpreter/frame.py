from pie.error import UndefinedVariable
from pie.objspace import space

__author__ = 'sery0ga'

class Frame:

    def __init__(self):
        self.stack = []
        self.variables = {}
        self.names = {}

        # trace data
        self.function_trace_stack = []

    def get_variable(self, name, context):
        try:
            return self.variables[name]
        except KeyError:
            error = UndefinedVariable(context, name)
            error.handle()
            return space.null()

    def set_variable(self, name, value):
        if name in self.variables:
            self.variables[name].set_value(value)
        else:
            self.variables[name] = space.variable(value)

    def pop_name(self):
        return self.stack.pop().str_w()

    def pop_and_get(self, context):
        return self.get_variable(self.pop_name(), context)