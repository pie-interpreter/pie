" Module with objects, representing functions "

import py
from pie.objspace import space
from pie.interpreter.context import shared_context
from pie.interpreter.errors.fatalerrors import NonVariablePassedByReference
from pie.interpreter.errors.warnings import NotEnoughParameters, WrongParameterType
from pie.interpreter.errors.base import InternalError
from pie.interpreter.functions.base import AbstractFunction


REF_DIVIDER = 10
INT, FLOAT, BOOL, STRING, SCALAR, MIXED = range(6)
REF_INT, REF_FLOAT, REF_BOOL, REF_STRING, REF_SCALAR, REF_MIXED =\
    range(REF_DIVIDER, REF_DIVIDER + 6)


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
                elif modded_arg_type == MIXED:
                    pass  # mixed does not require type validation
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
