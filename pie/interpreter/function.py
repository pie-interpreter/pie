" Module with objects, representing functions "

from pie.objspace import space
from pie.objects.variable import W_Variable
from pie.interpreter.frame import Frame
from pie.interpreter.interpreter import Interpreter
from pie.interpreter.errors.fatalerrors import NonVariablePassedByReference
from pie.interpreter.errors.warningerrors import MissingArgument


class AbstractFunction(object):
    "Interface for all functions"

    def call(self, context, stack_values):
        assert False, "Should not be reached"


class BuiltinFunction(AbstractFunction):
    "Built-in function, implemented in python"

    def call(self, context, stack_values):
        assert False, "Not implemented"


class UserFunction(AbstractFunction):
    "Function, defined by user"

    VALUE, REFERENCE = ('value', 'reference')

    def __init__(self, name, return_type, bytecode, arguments, line_declared):
        self.name = name
        self.return_type = return_type
        self.bytecode = bytecode
        self.arguments = arguments
        self.line_declared = line_declared

    def call(self, context, stack_values):
        frame = self._get_frame(context, stack_values)

        context.trace.append(self.name, self.bytecode.filename)
        Interpreter(self.bytecode, context, frame).interpret()
        context.trace.pop()

        return self._get_return_value(frame)

    def _get_frame(self, context, stack_values):
        values_count = len(stack_values)
        frame = Frame()
        for index, argument in enumerate(self.arguments):
            argument_name, argument_type, default = argument
            try:
                value = stack_values[values_count - index - 1]
                if argument_type == self.REFERENCE:
                    if not isinstance(value, W_Variable):
                        NonVariablePassedByReference(context).handle()
                        frame.variables[argument_name] = space.variable(space.null())
                    else:
                        frame.variables[argument_name] = value
                else:
                    frame.set_variable(argument_name, value.deref())

            except IndexError:
                if default is None:
                    MissingArgument(context, index, self).handle()
                    frame.variables[argument_name] = space.variable(space.null())
                else:
                    frame.variables[argument_name] = space.variable(default)

        return frame

    def _get_return_value(self, frame):
        if not frame.stack:
            return space.null()

        return_value = frame.stack.pop()
        if self.return_type == self.VALUE:
            return_value = return_value.deref()

        return return_value

    def __repr__(self):
        # TODO move it from here
        return '%s%s(%s) {\n    %s\n}' % (
            {self.VALUE: '', self.REFERENCE: '&'}[self.return_type],
            self.name,
            ', '.join([
                    '%s$%s%s' % (
                    {self.VALUE: '', self.REFERENCE: '&'}[argument[1]],
                    argument[0],
                    '' if argument[2] is None else ' = %s' % argument[2]
                ) for argument in self.arguments]),
            self.bytecode.__repr__().replace('\n', '\n    ')
        )
