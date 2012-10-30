__author__ = 'sery0ga'

# all opcodes with index <= OPCODE_INDEX_DIVIDER have 0 arguments
# all opcodes with index > OPCODE_INDEX_DIVIDER have 1 argument
OPCODE_INDEX_DIVIDER = 127

OPCODE = {
    # operations with no arguments, in most cases this means,
    # that they operate solely on values from top of the stack

    # common operations
    0: 'ECHO',
    1: 'RETURN',
    2: 'POP_STACK',
    3: 'DUPLICATE_TOP',
    4: 'INCLUDE',
    5: 'INCLUDE_ONCE',
    6: 'REQUIRE',
    7: 'REQUIRE_ONCE',

    # unary operations
    # operate on variable, retrieved by name from stack
    10: 'NOT', # logical not
    11: 'CAST_TO_ARRAY',
    12: 'CAST_TO_BOOL',
    13: 'CAST_TO_DOUBLE',
    14: 'CAST_TO_INT',
    15: 'CAST_TO_OBJECT',
    16: 'CAST_TO_STRING',
    17: 'CAST_TO_UNSET',
    # increment/decrement
    20: 'PRE_INCREMENT',
    21: 'PRE_DECREMENT',
    22: 'POST_INCREMENT',
    23: 'POST_DECREMENT',

    # binary operations
    # operate on two values on stack
    30: 'ADD',
    31: 'SUBSTRACT',
    32: 'CONCAT',
    33: 'MULTIPLY',
    34: 'DIVIDE',
    35: 'MOD',
    36: 'LESS_THAN',
    37: 'MORE_THAN',
    38: 'LESS_THAN_OR_EQUAL',
    39: 'MORE_THAN_OR_EQUAL',
    40: 'EQUAL',
    41: 'NOT_EQUAL',
    42: 'IDENTICAL',
    43: 'NOT_IDENTICAL',
    44: 'XOR', # logical xor

    # inplace operations (+=, -=, etc)
    # operate on variable, retreived by name from stack and value following it
    50: 'INPLACE_ADD',
    51: 'INPLACE_SUBSTRACT',
    52: 'INPLACE_CONCAT',
    53: 'INPLACE_MULTIPLY',
    54: 'INPLACE_DIVIDE',
    55: 'INPLACE_MOD',

    # loading and storing by name on stack
    60: 'LOAD_VAR',
    61: 'STORE_VAR',

    # from here operations require argument
    # in comment meaning of the argument is provideds

    # loading/storing from bytecode pre-cached values
    128: 'LOAD_CONST', # index of the constant to load
    129: 'LOAD_NAME', # index of the name to load
    130: 'LOAD_VAR_FAST', # index of the name of the variable to load
    131: 'STORE_VAR_FAST', # index of the name of the varibale to store value to

    # function calling by name, which is loaded from stack
    140: 'CALL_FUNCTION', # number of arguments to load from stack

    # moving around the code
    150: 'JUMP', # absolute position
    151: 'JUMP_IF_FALSE', # absolute position
    152: 'JUMP_IF_TRUE', # absolute position
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