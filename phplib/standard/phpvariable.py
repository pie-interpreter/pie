""" This module represents php variable handling functions.

You can find full description here: http://www.php.net/manual/en/ref.var.php

Important: Functions empty(), isset() and unset() are a part of the
interpreter core and not implemented here
"""
from pie.interpreter.functions.builtin import builtin_function
from pie.objspace import space

#TODO: boolval
#TODO: debug_zval_dump (?)
#TODO: doubleval
#TODO: floatval
#TODO: get_defined_vars
#TODO: get_resource_type
#TODO: gettype
#TODO: import_request_variables
#TODO: intval
#TODO: is_array
#TODO: is_bool
#TODO: is_callable
#TODO: is_double
#TODO: is_float
#TODO: is_int
#TODO: is_integer
#TODO: is_long
#TODO: is_null
#TODO: is_numeric
#TODO: is_object
#TODO: is_real
#TODO: is_resource
#TODO: is_scalar
#TODO: is_string
#TODO: print_r
#TODO: serialize
#TODO: settype
#TODO: strval
#TODO: unserialize

@builtin_function()
def var_dump(context, params):
    for param in params:
        var_dump_one_parameter(context, param)

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
        context.print_output("float(%G)\n" % param.float_w())
    elif param.type == space.W_BOOL:
        if param.is_true():
            context.print_output("bool(true)\n")
        else:
            context.print_output("bool(false)\n")
    elif param.type == space.W_NULL:
        context.print_output("NULL\n")

#TODO: var_export