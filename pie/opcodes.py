__author__ = 'sery0ga'

# all opcodes with index <= OPCODE_INDEX_DIVIDER have 0 arguments
# all opcodes with index > OPCODE_INDEX_DIVIDER have 1 argument
OPCODE_INDEX_DIVIDER = 127

OPCODE = {
    0: 'ECHO',
    1: 'ADD',
    128: 'LOAD_CONST'
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