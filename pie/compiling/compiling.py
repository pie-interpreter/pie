" Module, providing compiling tools "

from pie.compiling.bytecode import Bytecode
from pie.compiling.nodes import *
from pie.error import CompilerError
from pie.objects.int import W_IntObject
from pie.objects.conststring import W_ConstStringObject
from pie.opcodes import get_opcode_index


def compile_ast(ast):
    builder = BytecodeBuilder()
    builder.filename = filename
    ast.compile(builder)

    return builder.create_bytecode()

class BytecodeBuilder(object):
    " Helper class to build bycode "

    def __init__(self):
        self.code = []
        self.consts = []
        self.names = []
        self.functions = {}

        # caching lists
        self.int_consts_cache = {}
        self.string_consts_cache = {}
        self.names_cache = {}

        # lists to keep stack of loops
        self.break_positions = []
        self.continue_positions = []

        # trace data
        self.current_line = 0
        self.lines_by_positions = []
        self.offset = 0
        self.filename = ""

    def emit(self, opcode_name, arg=-1):
        current_position = self.get_current_position()

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

        return current_position

    def create_bytecode(self):
        bytecode = Bytecode()
        bytecode.code = "".join(self.code)
        bytecode.consts = self.consts
        bytecode.names = self.names
        bytecode.functions = self.functions

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
        self.update_value(position, self.get_current_position())

    def update_value(self, position, new_value):
        # updating first byte of the argument
        self.code[position] = chr(new_value & 0xff)
        # updating second byte of the argument
        self.code[position + 1] = chr(new_value >> 8)

    def register_loop(self):
        self.break_positions.append([])
        self.continue_positions.append([])

    def patch_break_positions(self, position):
        assert len(self.break_positions) > 0

        last_break_positions = self.break_positions.pop()
        for break_position in last_break_positions:
            self.update_value(break_position, position)

    def patch_continue_positions(self, position):
        assert len(self.continue_positions) > 0

        last_continue_positions = self.continue_positions.pop()
        for continue_position in last_continue_positions:
            self.update_value(continue_position, position)

    def add_break_position_to_patch(self, level, position):
        if len(self.break_positions) < level:
            raise CompilerError, "Cannot break %s levels" % level

        self.break_positions[-1 * level].append(position)

    def add_continue_position_to_patch(self, level, position):
        if len(self.continue_positions) < level:
            raise CompilerError, "Cannot continue %s levels" % level

        self.continue_positions[-1 * level].append(position)


class Function(object):

    def __init__(self, arguments, bytecode):
        self.arguments = arguments
        self.bytecode = bytecode
