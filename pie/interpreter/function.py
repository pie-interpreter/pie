" Module with objects, representing functions "

import py
from pie.objspace import space
from pie.objects.variable import W_Variable
from pie.interpreter.frame import Frame
from pie.interpreter.interpreter import Interpreter
from pie.interpreter.context import shared_context
from pie.interpreter.errors.fatalerrors import NonVariablePassedByReference
from pie.interpreter.errors.warnings import MissingArgument, NotEnoughParameters, WrongParameterType
from pie.interpreter.errors.base import InternalError


REF_DIVIDER = 10
INT, FLOAT, BOOL, STRING, SCALAR = range(5)
REF_INT, REF_FLOAT, REF_BOOL, REF_STRING, REF_SCALAR =\
    range(REF_DIVIDER, REF_DIVIDER + 5)


class AbstractFunction(object):
    "Interface for all functions"

    def __init__(self, name):
        self.name = name

    def call(self, context, stack_values):
        raise NotImplementedError


class UserFunction(AbstractFunction):
    "Function, defined by user"

    VALUE, REFERENCE = ('value', 'reference')

    def __init__(self, name, return_type, bytecode, arguments, line_declared):
        AbstractFunction.__init__(self, name)

        self.return_type = return_type
        self.bytecode = bytecode
        self.arguments = arguments
        self.line_declared = line_declared

    def call(self, context, stack_values):
        context.trace.append(self.name, self.bytecode.filename)
        frame = self._get_frame(context, stack_values)
        Interpreter(self.bytecode, context, frame).interpret()
        context.trace.pop()

        return self._get_return_value(frame)

    def _get_frame(self, context, stack_values):
        frame = Frame()
        for index, argument in enumerate(self.arguments):
            argument_name, argument_type, default = argument
            try:
                value = stack_values[index]

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
                    MissingArgument(context, index + 1, self).handle()
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


class BuiltinFunction(AbstractFunction):
    "Built-in function, implemented in python"

    def __init__(self, name, inner_function):
        AbstractFunction.__init__(self, name)
        self.inner_function = inner_function

    def call(self, context, stack_values):
        return self.inner_function(context, stack_values)


def builtin_function(args=[], optional_args=[], name=None):
    "Decorator to make function built-in"

    all_args = args + optional_args
    if not all_args:
        def simple_wrapper(function):
            function_name = name or function.func_name
            function_object = BuiltinFunction(function_name, function)
            shared_context.functions[function_name] = function_object

        return simple_wrapper

    else:
        def wrapper(function):
            function_name = name or function.func_name
            body = []
            body.append('def %s(context, params):' % function.func_name)

            if len(args):
                body.append('  if len(params) < %s:' % len(args))
                body.append('    NotEnoughParameters(context, %s, len(params), "%s").handle()'
                    % (len(args), function_name))
                body.append('    return space.null()')

            body.append('  try:')
            for index, arg_type in enumerate(all_args):
                body.append('    position = %s' % index)
                if arg_type > REF_DIVIDER:
                    body.append('    if not isinstance(params[%s], W_Variable):' % index)
                    body.append('      NonVariablePassedByReference(context).handle()')
                    body.append('      return space.null()')
                else:
                    body.append('    params[%s] = params[%s].deref()' % (index, index))

                modded_arg_type = arg_type % REF_DIVIDER
                if modded_arg_type == INT:
                    body.append('    assertInt(params[%s])' % index)
                elif modded_arg_type == FLOAT:
                    body.append('    assertFloat(params[%s])' % index)
                elif modded_arg_type == BOOL:
                    body.append('    assertBool(params[%s])' % index)
                elif modded_arg_type == STRING:
                    body.append('    assertString(params[%s])' % index)
                elif modded_arg_type == SCALAR:
                    body.append('    assertScalar(params[%s])' % index)
                else:
                    raise InternalError(
                        'Invalid argument type in core function %s' % function_name)

            body.append('  except TypeAssertionError as e:')
            body.append('    WrongParameterType('
                'context, e.given, e.expected, position + 1, "%s").handle()' % function_name)
            body.append('    return space.null()')
            body.append('  except IndexError:')
            body.append('    pass')
            body.append('  return wrapped_function(context, params)')

            source = '\n'.join(body)
            compile_context = {
                'wrapped_function': function,
                'space': space,
                'NotEnoughParameters': NotEnoughParameters,
                'NonVariablePassedByReference': NonVariablePassedByReference,
                'WrongParameterType': WrongParameterType,
                'TypeAssertionError': TypeAssertionError,
                'assertInt': assertInt,
                'assertFloat': assertFloat,
                'assertBool': assertBool,
                'assertString': assertString,
                'assertScalar': assertScalar,
            }
            try:
                exec py.code.Source(source).compile() in compile_context
            except:
                print source
                raise InternalError(
                    'Failed to compile core funciton %s' % function_name)

            compile_context[function.func_name]._jit_unroll_safe_ = True

            function_object = BuiltinFunction(
                function_name, compile_context[function.func_name]
            )
            shared_context.functions[function_name] = function_object

        return wrapper


class TypeAssertionError(Exception):

    def __init__(self, expected, given):
        self.expected = expected
        self.given = given


def assertInt(w_value):
    if w_value.type == space.W_INT:
        return

    raise TypeAssertionError(space.W_INT, w_value.type)


def assertFloat(w_value):
    if w_value.type == space.W_FLOAT:
        return

    raise TypeAssertionError(space.W_FLOAT, w_value.type)


def assertBool(w_value):
    if w_value.type == space.W_BOOL:
        return

    raise TypeAssertionError(space.W_BOOL, w_value.type)


def assertString(w_value):
    if w_value.type == space.W_STR:
        return

    raise TypeAssertionError(space.W_STR, w_value.type)


def assertScalar(w_value):
    types = [space.W_INT, space.W_FLOAT, space.W_BOOL, space.W_STR]
    if w_value.type in types:
        return

    raise TypeAssertionError(' or '.join(types), w_value.type)


@builtin_function(args=[SCALAR, SCALAR], name="strpos", optional_args=[STRING, STRING])
def strpos(context, params):
    return space.int(2)
