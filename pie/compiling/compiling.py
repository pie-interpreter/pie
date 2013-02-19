" Module, providing compiling tools "

from pie.ast import ast
from pie.compiling.bytecode import Bytecode
from pie.opcodes import get_opcode_index
from pie.interpreter.errors.fatalerrors import IllegalBreakContinueLevel
import pie.compiling.nodes


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
        self.functions = []
        self.declared_functions = []

        # caching lists
        self.consts_cache = {
            'int': {}, 'string': {}, 'float': {},
            'bool': {}, 'null': {}, 'array': {}, 'undefined': {}
        }
        self.names_cache = {}

        # lists to keep stack of loops
        self.break_positions = []
        self.continue_positions = []

        # trace data
        self.filename = ""
        self.line = 0
        self.opcode_lines = {}

    def emit(self, opcode_name, arg=-1):
        current_position = self.get_current_position()

        assert arg < (1 << 16)
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
        bytecode.declared_functions = self.declared_functions

        bytecode.filename = self.filename
        bytecode.opcode_lines = self.opcode_lines

        return bytecode

    def register_const(self, const_object):
        type_name = const_object.type_name
        str_value = const_object.get_str_value()
        try:
            return self.consts_cache[type_name][str_value]
        except KeyError:
            consts_count = len(self.consts)
            self.consts.append(const_object.get_compiled_value())
            self.consts_cache[type_name][str_value] = consts_count
            return consts_count

    def register_name(self, name):
        try:
            return self.names_cache[name]
        except KeyError:
            names_count = len(self.names)
            self.names.append(name)
            self.names_cache[name] = names_count
            return names_count

    def register_function(self, function):
        functions_count = len(self.functions)
        self.functions.append(function)
        return functions_count

    def register_declared_function(self, function):
        self.declared_functions.append(function)

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
            raise IllegalBreakContinueLevel(None, level)

        self.break_positions[-level].append(position)

    def add_continue_position_to_patch(self, level, position):
        if len(self.continue_positions) < level:
            raise IllegalBreakContinueLevel(None, level)

        self.continue_positions[-level].append(position)
