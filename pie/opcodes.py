__author__ = 'sery0ga'

# all opcodes with index <= OPCODE_INDEX_DIVIDER have 0 arguments
# all opcodes with index > OPCODE_INDEX_DIVIDER have 1 argument
OPCODE_INDEX_DIVIDER = 127

OPCODE = {
    0: 'ECHO',
    1: 'RETURN',
    2: 'ADD',
    3: 'SUBSTRACT',
    4: 'MULTIPLY',
    5: 'LESS_THAN',
    6: 'MORE_THAN',
    7: 'CONCAT',
    8: 'POP_STACK',
    9: 'DUPLICATE_TOP',
    128: 'LOAD_CONST',
    129: 'LOAD_NAME',
    130: 'LOAD_FAST',
    131: 'STORE_FAST',
    132: 'CALL_FUNCTION',
    133: 'JUMP',
    134: 'JUMP_IF_FALSE',
    135: 'JUMP_IF_TRUE',
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