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
from pie.types import PHPTypes
from pie.interpreter.functions.builtin import SCALAR, MIXED
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
    php_type = params[0].deref().get_type()
    type_name = 'unknown type'
    if php_type == PHPTypes.w_int:
        type_name = 'integer'
    elif php_type == PHPTypes.w_float:
        type_name = 'double'
    elif php_type == PHPTypes.w_string:
        type_name = 'string'
    elif php_type == PHPTypes.w_bool:
        type_name = 'boolean'
    elif php_type == PHPTypes.w_null:
        type_name = 'NULL'
    elif php_type == PHPTypes.w_array:
        type_name = 'array'
    elif php_type == PHPTypes.w_object:
        type_name = 'object'
    elif php_type == PHPTypes.w_resource:
        type_name = 'resource'
    return space.str(type_name)

#TODO: is_callable
#TODO: intval

@builtin_function()
def is_array(context, params):
    result = (params[0].deref().get_type() == PHPTypes.w_array)
    return space.bool(result)

@builtin_function()
def is_bool(context, params):
    result = (params[0].deref().get_type() == PHPTypes.w_bool)
    return space.bool(result)

@builtin_function()
def is_double(context, params):
    result = (params[0].deref().get_type() == PHPTypes.w_float)
    return space.bool(result)

@builtin_function()
def is_float(context, params):
    result = (params[0].deref().get_type() == PHPTypes.w_float)
    return space.bool(result)

@builtin_function()
def is_int(context, params):
    result = (params[0].deref().get_type() == PHPTypes.w_int)
    return space.bool(result)

@builtin_function()
def is_integer(context, params):
    result = (params[0].deref().get_type() == PHPTypes.w_int)
    return space.bool(result)

@builtin_function()
def is_long(context, params):
    result = (params[0].deref().get_type() == PHPTypes.w_int)
    return space.bool(result)

@builtin_function()
def is_null(context, params):
    result = (params[0].deref().get_type() == PHPTypes.w_null)
    return space.bool(result)

@builtin_function()
def is_numeric(context, params):
    php_type = params[0].deref().get_type()
    if php_type == PHPTypes.w_int or php_type == PHPTypes.w_float:
        return space.bool(True)
    if php_type == PHPTypes.w_string:
        return params[0].deref().is_convertible_to_number_strict()
    return space.bool(False)

@builtin_function()
def is_object(context, params):
    result = (params[0].deref().get_type() == PHPTypes.w_object)
    return space.bool(result)

@builtin_function()
def is_real(context, params):
    result = (params[0].deref().get_type() == PHPTypes.w_float)
    return space.bool(result)

@builtin_function()
def is_resource(context, params):
    result = (params[0].deref().get_type() == PHPTypes.w_resource)
    return space.bool(result)

@builtin_function()
def is_scalar(context, params):
    php_type = params[0].deref().get_type()
    if (php_type == PHPTypes.w_string or php_type == PHPTypes.w_int or
        php_type == PHPTypes.w_float or php_type == PHPTypes.w_bool):
        return space.bool(True)
    return space.bool(False)

@builtin_function()
def is_string(context, params):
    result = (params[0].deref().get_type() == PHPTypes.w_string)
    return space.bool(result)


@builtin_function(args=[MIXED], optional_args=[SCALAR])
def print_r(context, params):
    #TODO: array
    #TODO: object
    #TODO: resource
    w_expression = params[0].deref()
    if len(params) > 1:
        to_variable = params[1].deref().is_true()
    else:
        to_variable = False
    if w_expression.get_type() == PHPTypes.w_string:
        return _handle_output(context, w_expression, to_variable)
    elif (w_expression.get_type() == PHPTypes.w_int
          or w_expression.get_type() == PHPTypes.w_float
          or w_expression.get_type() == PHPTypes.w_bool
          or w_expression.get_type() == PHPTypes.w_null):
        return _handle_output(context, w_expression.as_string(), to_variable)
    return space.bool(True)


def _handle_output(context, w_value, to_variable):
    if not to_variable:
        context.print_output(w_value.str_w())
        return space.bool(True)
    return w_value

#TODO: serialize
#TODO: settype
#TODO: strval
#TODO: unserialize


@builtin_function()
def var_dump(context, params):
    for param in params:
        var_dump_one_parameter(context, param.deref())


def var_dump_one_parameter(context, param, to_context=True, indent_level=""):
    #FIXME: correct float var_dump for 1.0e+4 < value < 1.0e+14. Uncomment in test
    #TODO: resource
    #TODO: object
    #TODO: unknown type (?)
    #TODO: add JIT support
    output = ""
    if param.get_type() == PHPTypes.w_string:
        output = "string(%d) \"%s\"\n" % (param.strlen(), param.str_w())
    elif param.get_type() == PHPTypes.w_int:
        output = "int(%d)\n" % param.int_w()
    elif param.get_type() == PHPTypes.w_float:
        output = "float(%s)\n" % param.float_w()
    elif param.get_type() == PHPTypes.w_bool:
        if param.is_true():
            output = "bool(true)\n"
        else:
            output = "bool(false)\n"
    elif param.get_type() == PHPTypes.w_null:
        output = "NULL\n"
    elif param.get_type() == PHPTypes.w_array:
        array_indent_level = indent_level + "  "
        output = 'array(%d) {\n' % param.len()
        for key, value in sorted(param.storage.iteritems()):
            try:
                int(key)
                printable_key = key
            except ValueError:
                printable_key = '"%s"' % key
            output += "%s[%s]=>\n%s%s" % (array_indent_level,
                                          printable_key,
                                          array_indent_level,
                                          var_dump_one_parameter(context, value, False, array_indent_level))
        output += "%s}\n" % indent_level
    if to_context:
        context.print_output(output)
    return output

#TODO: var_export
