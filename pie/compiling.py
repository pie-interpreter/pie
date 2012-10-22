" Module, providing compiling tools "

from pie.ast.nodes import Source, Echo, BinaryOperation, ConstantInt, InlineHtml
from pie.bytecode import Bytecode
from pie.objects.intobject import W_IntObject
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

        # caching lists
        self.int_consts_cache = {}

    def emit(self, opcode_name, arg=-1):
        assert arg < 1<<16
        self.code.append(chr(get_opcode_index(opcode_name)))
        if arg != -1:
            self.code.append(chr(arg))

    def create_bytecode(self):
        bytecode = Bytecode()
        bytecode.code = "".join(self.code)
        bytecode.consts = self.consts

        return bytecode

    def register_int_const(self, value):
        try:
            return self.int_consts_cache[value]
        except KeyError:
            constants_count = len(self.consts)
            self.consts.append(W_IntObject(value))
            self.int_consts_cache[value] = constants_count
            return constants_count


class __extend__(Source):

    def compile(self, builder):
        for statement in self.statements:
            statement.compile(builder)


class __extend__(Echo):

    def compile(self, builder):
        self.value.compile(builder)
        builder.emit('ECHO')


class __extend__(BinaryOperation):

    def compile(self, builder):
        self.left.compile(builder)
        self.right.compile(builder)
        builder.emit('ADD')


class __extend__(ConstantInt):

    def compile(self, builder):
        index = builder.register_int_const(self.value)
        builder.emit('LOAD_CONST', index)

class __extend__(InlineHtml):

    def compile(self, builder):
        pass
