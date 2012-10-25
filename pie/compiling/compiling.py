" Module, providing compiling tools "

from pie.compiling.bytecode import Bytecode
from pie.compiling.nodes import *
from pie.error import CompilerError
from pie.objects.int import W_IntObject
from pie.objects.conststring import W_ConstStringObject
from pie.opcodes import get_opcode_index


def compile_ast(ast):
    builder = BytecodeBuilder()
    ast.compile(builder)

    return builder.create_bytecode()

class BytecodeBuilder(object):
    """ Helper class to build bytecode """

    def __init__(self):
        self.code = []
        self.consts = []
        self.names = []
        self.functions = {}

        # caching lists
        self.int_consts_cache = {}
        self.string_consts_cache = {}
        self.names_cache = {}

        # trace data
        self.current_line = 0
        self.lines_by_positions = []
        self.offset = 0

    def emit(self, opcode_name, arg=-1):
        assert arg < 1<<16
        # lines are numbered from 0 so we add +1 to get human-readable results
        line = self.current_line + self.offset + 1
        self.lines_by_positions.append(line)
        self.code.append(chr(get_opcode_index(opcode_name)))
        if arg != -1:
            # writing first byte of the argument
            self.code.append(chr(arg & 0xff))
            # writing second byte of the argument
            self.code.append(chr(arg >> 8))
            self.lines_by_positions.append(line)
            self.lines_by_positions.append(line)

    def set_line(self, line_number):
        self.current_line = line_number

    def create_bytecode(self):
        bytecode = Bytecode()
        bytecode.code = "".join(self.code)
        bytecode.consts = self.consts
        bytecode.names = self.names
        bytecode.functions = self.functions
        bytecode.lines_by_positions = self.lines_by_positions
        return bytecode

    def register_int_const(self, value):
        try:
            return self.int_consts_cache[value]
        except KeyError:
            constants_count = len(self.consts)
            self.consts.append(W_IntObject(value))
            self.int_consts_cache[value] = constants_count
            return constants_count

    def register_string_const(self, value):
        try:
            return self.string_consts_cache[value]
        except KeyError:
            constants_count = len(self.consts)
            self.consts.append(W_ConstStringObject(value))
            self.string_consts_cache[value] = constants_count
            return constants_count

    def register_name(self, name):
        try:
            return self.names_cache[name]
        except KeyError:
            names_count = len(self.names)
            self.names.append(name)
            self.names_cache[name] = names_count
            return names_count

    def register_function(self, name, arguments, bytecode):
        name = name.lower()
        if name in self.functions:
            raise CompilerError("Function %s already declared" % name)

        self.functions[name] = Function(arguments, bytecode)

    def get_current_position(self):
        " Get position, at which next opcode will be placed "
        return len(self.code)

    def update_to_current_position(self, position):
        current_position = self.get_current_position()
        # updating first byte of the argument
        self.code[position] = chr(current_position & 0xff)
        # updating second byte of the argument
        self.code[position + 1] = chr(current_position >> 8)


class Function(object):

    def __init__(self, arguments, bytecode):
        self.arguments = arguments
        self.bytecode = bytecode
