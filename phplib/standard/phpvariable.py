""" This module represents php variable handling functions.

You can find full description here: http://www.php.net/manual/en/ref.var.php

Important: Functions empty(), isset() and unset() are a part of the
interpreter core and not implemented here

import_request_variables() function is not implemented and we have no plan
of doing it, because using this function is extremely bad practice.

debug_zval_dump() function is not implemented because it returns ZendEngine
related stuff. We don't use ZendEngine so there's no reason to have such
function.
"""
from pie.interpreter.functions.builtin import builtin_function
from pie.objspace import space

@builtin_function()
def boolval(context, params):
    return params[0].deref().as_bool()

@builtin_function()
def doubleval(context, params):
    return params[0].deref().as_float()

@builtin_function()
def floatval(context, params):
    return params[0].deref().as_float()

#TODO: get_defined_vars
#TODO: get_resource_type

@builtin_function()
def gettype(context, params):
    type = params[0].deref().get_type()
    type_name = 'unknown type'
    if type == space.W_INT:
        type_name = 'integer'
    elif type == space.W_FLOAT:
        type_name = 'double'
    elif type == space.W_STR:
        type_name = 'string'
    elif type == space.W_BOOL:
        type_name = 'boolean'
    elif type == space.W_NULL:
        type_name = 'NULL'
    return space.str(type_name)

#TODO: is_callable
#TODO: intval

@builtin_function()
def is_array(context, params):
    result = (params[0].deref().get_type() == space.W_ARRAY)
    return space.bool(result)

@builtin_function()
def is_bool(context, params):
    result = (params[0].deref().get_type() == space.W_BOOL)
    return space.bool(result)

@builtin_function()
def is_double(context, params):
    result = (params[0].deref().get_type() == space.W_FLOAT)
    return space.bool(result)

@builtin_function()
def is_float(context, params):
    result = (params[0].deref().get_type() == space.W_FLOAT)
    return space.bool(result)

@builtin_function()
def is_int(context, params):
    result = (params[0].deref().get_type() == space.W_INT)
    return space.bool(result)

@builtin_function()
def is_integer(context, params):
    result = (params[0].deref().get_type() == space.W_INT)
    return space.bool(result)

@builtin_function()
def is_long(context, params):
    result = (params[0].deref().get_type() == space.W_INT)
    return space.bool(result)

@builtin_function()
def is_null(context, params):
    result = (params[0].deref().get_type() == space.W_NULL)
    return space.bool(result)

#TODO: is_numeric
#TODO: is_object

@builtin_function()
def is_real(context, params):
    result = (params[0].deref().get_type() == space.W_FLOAT)
    return space.bool(result)

#TODO: is_resource

@builtin_function()
def is_scalar(context, params):
    type = params[0].deref().get_type()
    if type == space.W_STR or type == space.W_INT or type == space.W_FLOAT \
        or type == space.W_BOOL:
        return space.bool(True)
    return space.bool(False)


@builtin_function()
def is_string(context, params):
    result = (params[0].deref().get_type() == space.W_STR)
    return space.bool(result)

#TODO: print_r
#TODO: serialize
#TODO: settype
#TODO: strval
#TODO: unserialize

@builtin_function()
def var_dump(context, params):
    for param in params:
        var_dump_one_parameter(context, param.deref())

def var_dump_one_parameter(context, param):
    #FIXME: correct float var_dump for 1.0e+4 < value < 1.0e+14. Uncomment in test
    #TODO: array
    #TODO: resource
    #TODO: object
    #TODO: unknown type (?)
    #TODO: add JIT support
    if param.type == space.W_STR:
        context.print_output("string(%d) \"%s\"\n" %
            (param.strlen(), param.str_w()))
    elif param.type == space.W_INT:
        context.print_output("int(%d)\n" % param.int_w())
    elif param.type == space.W_FLOAT:
        context.print_output("float(%s)\n" % param.float_w())
    elif param.type == space.W_BOOL:
        if param.is_true():
            context.print_output("bool(true)\n")
        else:
            context.print_output("bool(false)\n")
    elif param.type == space.W_NULL:
        context.print_output("NULL\n")

#TODO: var_export