from pie.interpreter.errors.noticeerrors import UndefinedVariable
from pie.objspace import space

__author__ = 'sery0ga'


class Frame:

    def __init__(self):
        self.stack = []
        self.variables = {}
        self.names = {}

    def get_variable(self, name, context):
        try:
            return self.variables[name]
        except KeyError:
            UndefinedVariable(context, name).handle()
            return space.null()

    def set_variable(self, name, w_value):
        if name in self.variables:
            self.variables[name].set_value(w_value.deref())
        else:
            self.variables[name] = space.variable(w_value.deref())

    def pop_name(self):
        return self.stack.pop().str_w()

    def pop_and_get(self, context):
        return self.get_variable(self.pop_name(), context)
