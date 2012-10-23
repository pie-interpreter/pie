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

    def emit(self, opcode_name, arg=-1):
        assert arg < 1<<16
        self.code.append(chr(get_opcode_index(opcode_name)))
        if arg != -1:
            self.code.append(chr(arg))

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
        self.code[position] = chr(self.get_current_position())


class Function(object):

    def __init__(self, arguments, bytecode):
        self.arguments = arguments
        self.bytecode = bytecode
