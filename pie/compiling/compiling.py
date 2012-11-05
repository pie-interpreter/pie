" Module, providing compiling tools "

from pie.ast import ast
from pie.compiling.bytecode import Bytecode
from pie.compiling.nodes import *
from pie.error import CompilerError
from pie.opcodes import get_opcode_index
from pie.objspace import space


def compile_source(source):
    astree = ast.build(source)
    return compile_ast(astree, source)


def compile_ast(astree, source):
    builder = BytecodeBuilder()
    builder.filename = source.filename
    astree.compile(builder)

    return builder.create_bytecode()

class BytecodeBuilder(object):
    " Helper class to build byte-code "

    def __init__(self):
        self.code = []
        self.consts = []
        self.names = []
        self.functions = {}

        # caching lists
        self.int_consts_cache = {}
        self.string_consts_cache = {}
        self.bool_consts_cache = {}
        self.names_cache = {}
        self.null_const_index = None

        # lists to keep stack of loops
        self.break_positions = []
        self.continue_positions = []

        # trace data
        self.filename = ""
        self.line = 0
        self.opcode_lines = {}

    def set_line(self, line):
        self.line = line

    def emit(self, opcode_name, arg=-1):
        current_position = self.get_current_position()

        assert arg < 1<<16
        self.opcode_lines[current_position] = self.line
        self.code.append(chr(get_opcode_index(opcode_name)))
        if arg != -1:
            # writing first byte of the argument
            self.code.append(chr(arg & 0xff))
            # writing second byte of the argument
            self.code.append(chr(arg >> 8))

        return current_position

    def get_child_builder(self):
        " Create builder, based on this one to compile inner entities "
        builder = BytecodeBuilder()
        builder.filename = self.filename
        builder.line = self.line

        return builder

    def create_bytecode(self):
        bytecode = Bytecode()
        bytecode.code = "".join(self.code)
        bytecode.consts = self.consts
        bytecode.names = self.names
        bytecode.functions = self.functions

        bytecode.filename = self.filename
        bytecode.opcode_lines = self.opcode_lines

        return bytecode

    def register_int_const(self, value):
        try:
            return self.int_consts_cache[value]
        except KeyError:
            constants_count = len(self.consts)
            self.consts.append(space.int(value))
            self.int_consts_cache[value] = constants_count
            return constants_count

    def register_bool_const(self, value):
        try:
            return self.bool_consts_cache[value]
        except KeyError:
            constants_count = len(self.consts)
            self.consts.append(space.bool(value))
            self.bool_consts_cache[value] = constants_count
            return constants_count

    def register_string_const(self, value):
        try:
            return self.string_consts_cache[value]
        except KeyError:
            constants_count = len(self.consts)
            self.consts.append(space.str(value))
            self.string_consts_cache[value] = constants_count
            return constants_count

    def register_null_const(self):
        if self.null_const_index is None:
            constants_count = len(self.consts)
            self.consts.append(space.null())
            self.null_const_index = constants_count

        return self.null_const_index

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
