import os

from pie.interpreter.functions.builtin import builtin_function
from pie.objspace import space

#TODO: boolval
#TODO: debug_zval_dump (?)
#TODO: doubleval
# empty() -- already implemented as part of interpreter
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
#isset() -- already implemented as part of interpreter
#TODO: print_r
#TODO: serialize
#TODO: settype
#TODO: strval
#TODO: unserialize
#unset() -- already implemented as part of interpreter

@builtin_function()
def var_dump(context, params):
    #FIXME: correct float var_dump for 1.0e+4 < value < 1.0e+14. Uncomment in test
    #TODO: array
    #TODO: resource
    #TODO: object
    #TODO: unknown type (?)
    for param in params:
        if param.type == space.W_STR:
            os.write(1, "string(%d) \"%s\"\n" % (param.strlen(), param.str_w()))
        elif param.type == space.W_INT:
            os.write(1, "int(%d)\n" % param.int_w())
        elif param.type == space.W_FLOAT:
            os.write(1, "float(%G)\n" % param.float_w())
        elif param.type == space.W_BOOL:
            if param.is_true():
                os.write(1, "bool(true)\n")
            else:
                os.write(1, "bool(false)\n")
        elif param.type == space.W_NULL:
            os.write(1, "NULL\n")

#TODO: var_export