
__author__ = 'sery0ga'

from pie.opcodes import OPCODE_INDEX_DIVIDER, get_opcode_name

class Bytecode(object):
    """
    Contains data after AST was compiled.
    Contains enough data to run code on interpreter
    """

    def __init__(self):
        self.names = []
        self.consts = []
        self.functions = {}
        self.code = ""

        # trace data
        self.lines_by_positions = []
        self.filename = ""

    def __repr__(self):
        return disassemble(self)
#        return "Code: %s\nConstants number: %s" % (self.code, len(self.consts))

    def get_line(self, position):
        return self.lines_by_positions[position]

    def get_filename(self):
        import os
        return os.path.abspath(self.filename)


def disassemble(bytecode):
    "Function to disassemble code to human-readable form"

    assert isinstance(bytecode, Bytecode)
    result = 'Bytecode object:\n  Functions:\n'
    for name in bytecode.functions:
        result += '      %s()\n' % name

    result += '  Code:\n'

    position = 0

    code = bytecode.code
    code_length = len(code)

    while True:
        if position >= code_length:
            break

        next_instr = ord(code[position])
        position += 1
        if next_instr > OPCODE_INDEX_DIVIDER:
            arg = ord(code[position]) + (ord(code[position + 1]) << 8)
            position += 2
        else:
            arg = 0 # don't make it negative
        assert arg >= 0

        opcode_name = get_opcode_name(next_instr)
        result += '      ' + opcode_name + '\n'

    return result




