" Module with objects, representing functions "
from pie.error import InterpreterError, PieError
from pie.interpreter.interpreter import Interpreter
from pie.objspace import space
from pie.interpreter.frame import Frame


class AbstractFunction(object):
    "Interface for all functions"

    def call(self, context, parent_frame, arguments_number):
        raise InterpreterError("Not implemented")


class BuiltinFunction(AbstractFunction):
    "Built-in function, implemented in python"

    def call(self, context, parent_frame, arguments_number):
        pass


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

        context.trace.append(self.name, self.bytecode)
        interpreter = Interpreter(self.bytecode, context, frame)
        interpreter.interpret()
        context.trace.pop()

        return self._get_return_value(frame)

    def _get_frame(self, context, stack_values):
        frame = Frame()
        for argument_name, argument_type, default in self.arguments:
            if stack_values:
                if argument_type == self.REFERENCE:
                    frame.variables[argument_name] = stack_values
            else:
                pass

        return frame

    def _get_return_value(self, frame):
        if not frame.stack:
            return space.null()

        return_value = frame.stack.pop()
        if self.return_type == self.VALUE:
            return_value = return_value.deref()

        return return_value
