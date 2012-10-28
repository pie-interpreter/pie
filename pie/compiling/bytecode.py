
__author__ = 'sery0ga'

from pie.opcodes import OPCODE_INDEX_DIVIDER, get_opcode_name
from pypy.rlib.objectmodel import compute_unique_id

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

    def get_line(self, position):
        return self.lines_by_positions[position]

def disassemble(bytecode):
    """Function to disassemble code to human-readable form"""

    assert isinstance(bytecode, Bytecode)
    result = 'Bytecode object: <' + str(compute_unique_id(bytecode)) + '>\n'

    if bytecode.consts:
        result +=  '\n  Consts:\n'
        for const in enumerate(bytecode.consts):
            result += '      %s: %s\n' % const

    if bytecode.names:
        result +=  '\n  Names:\n'
        for name in enumerate(bytecode.names):
            result += '      %s: %s\n' % name

    result += '\n  Code:\n'
    position = 0
    code = bytecode.code
    code_length = len(code)
    while True:
        if position >= code_length:
            break

        next_instr = ord(code[position])
        position += 1

        opcode_name = get_opcode_name(next_instr)
        result += '      ' + opcode_name

        if next_instr > OPCODE_INDEX_DIVIDER:
            arg = ord(code[position]) + (ord(code[position + 1]) << 8)
            position += 2
            result += ' ' + str(arg)

        result += '\n'

    if bytecode.functions:
        result += '\nFunctions:\n'
        for name in bytecode.functions:
            function = bytecode.functions[name]
            result += '%s(%s)\n' % (name, ", ".join(function.arguments))
            result += function.bytecode.__repr__()


    return result
