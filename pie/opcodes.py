__author__ = 'sery0ga'

# all opcodes with index <= OPCODE_INDEX_DIVIDER have 0 arguments
# all opcodes with index > OPCODE_INDEX_DIVIDER have 1 argument
OPCODE_INDEX_DIVIDER = 127

OPCODE = {
    # operations with no arguments, in most cases this means,
    # that they operate solely on values from top of the stack

    # common operations
    0: 'ECHO',
    1: 'PRINT',
    2: 'RETURN',
    3: 'POP_STACK',
    4: 'DUPLICATE_TOP',
    5: 'INCLUDE',
    6: 'INCLUDE_ONCE',
    7: 'REQUIRE',
    8: 'REQUIRE_ONCE',
    9: 'EMPTY_VAR',  # check if var with name from the stack is empty
    10: 'EMPTY_RESULT',  # check if value on the stack is empty
    11: 'MAKE_REFERENCE',  # make a reference for variable on stack
    12: 'GET_INDEX', # dereference one array value

    # unary operations
    # operate on variable, retrieved by name from stack
    20: 'NOT',  # logical not
    21: 'CAST_TO_ARRAY',
    22: 'CAST_TO_BOOL',
    23: 'CAST_TO_DOUBLE',
    24: 'CAST_TO_INT',
    25: 'CAST_TO_OBJECT',
    26: 'CAST_TO_STRING',
    27: 'CAST_TO_UNSET',
    # increment/decrement
    30: 'PRE_INCREMENT',
    31: 'PRE_DECREMENT',
    32: 'POST_INCREMENT',
    33: 'POST_DECREMENT',

    # binary operations
    # operate on two values on stack
    40: 'ADD',
    41: 'SUBSTRACT',
    42: 'CONCAT',
    43: 'MULTIPLY',
    44: 'DIVIDE',
    45: 'MOD',
    46: 'LESS_THAN',
    47: 'MORE_THAN',
    48: 'LESS_THAN_OR_EQUAL',
    49: 'MORE_THAN_OR_EQUAL',
    50: 'EQUAL',
    51: 'NOT_EQUAL',
    52: 'IDENTICAL',
    53: 'NOT_IDENTICAL',
    54: 'XOR',  # logical xor

    # inplace operations (+=, -=, etc)
    # operate on variable, retreived by name from stack and value following it
    60: 'INPLACE_ADD',
    61: 'INPLACE_SUBSTRACT',
    62: 'INPLACE_CONCAT',
    63: 'INPLACE_MULTIPLY',
    64: 'INPLACE_DIVIDE',
    65: 'INPLACE_MOD',

    # loading and storing by name on stack
    70: 'LOAD_VAR',
    71: 'STORE_VAR',

    # from here operations require argument
    # meaning of the argument is provided in comment

    # loading/storing from bytecode pre-cached values
    128: 'LOAD_CONST',  # index of the constant to load
    129: 'LOAD_NAME',  # index of the name to load
    130: 'LOAD_VAR_FAST',  # index of the name of the variable to load
    131: 'STORE_VAR_FAST',  # index of the name of the varibale to store value to
    132: 'DECLARE_FUNCTION',  # index of the function to declare

    # function calling by name, which is loaded from stack
    140: 'CALL_FUNCTION',  # number of arguments to load from stack

    # moving around the code
    150: 'JUMP',  # absolute position
    151: 'JUMP_IF_FALSE',  # absolute position
    152: 'JUMP_IF_TRUE',  # absolute position

    # other common operations
    160: 'ISSET',  # number of var names on the stack to check set status
    161: 'UNSET',  # number of var names on the stack to unset
    162: 'MAKE_ARRAY',  # number of values to read from the stack
    163: 'GET_INDEXES', # number of indexes to read from the stack
}

OPCODE_INDEXES = {}


def get_opcode_name(index):
    try:
        return OPCODE[index]
    except KeyError:
        return ""


def get_opcode_index(name):
    try:
        return OPCODE_INDEXES[name]
    except KeyError:
        return -1


def _initialize():
    for (key, value) in OPCODE.items():
        OPCODE_INDEXES[value] = key

_initialize()

if __name__ == "__main__":
    print OPCODE
    print OPCODE_INDEXES
