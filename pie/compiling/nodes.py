" Module, defining how each node of ast is compiled "

from pie.ast.nodes import *

class __extend__(StatementsList):

    def compile(self, builder):
        for statement in self.statements:
            statement.compile(builder)


class __extend__(Echo):

    def compile(self, builder):
        self.expression.compile(builder)
        builder.emit('ECHO')


class __extend__(Return):

    def compile(self, builder):
        self.expression.compile(builder)
        builder.emit('RETURN')


class __extend__(FunctionCall):

    def compile(self, builder):
        for i in range(0, len(self.parameters)):
            self.parameters[-1 * i].compile(builder)

        identifier = self.name
        if isinstance(identifier, Identifier):
            index = builder.register_name(identifier.value)
            builder.emit("LOAD_NAME", index)
        else:
            self.name.compile(builder)

        builder.emit("CALL_FUNCTION", len(self.parameters))


class __extend__(BinaryOperator):

    def compile(self, builder):
        self.left.compile(builder)
        self.right.compile(builder)
        opcode = self.get_binary_opcode()
        builder.emit(opcode)

    def get_binary_opcode(self):
        operations = {
            '+': 'ADD',
            '-': 'SUBSTRACT',
            '*': 'MULTIPLY',
            '<': 'LESS_THAN',
            '>': 'MORE_THAN',
        }

        return operations[self.operation]


class __extend__(TernaryOperator):

    def compile(self, builder):
        # evaluating condition
        self.condition.compile(builder)
        builder.emit('JUMP_IF_FALSE', 0)
        # adding jump opcode and saving position of it's parameter
        # to patch it later to second branch's position
        jump_if_false_position = builder.get_current_position() - 2

        self.left.compile(builder)
        builder.emit('JUMP', 0)
        # adding jump opcode and saving position of it's parameter
        # to patch it later to end of statement's position
        jump_position = builder.get_current_position() - 2
        builder.update_to_current_position(jump_if_false_position)

        self.right.compile(builder)
        builder.update_to_current_position(jump_position)


class __extend__(Variable):

    def compile(self, builder):
        identifier = self.name
        assert isinstance(identifier, Identifier)
        index = builder.register_name(identifier.value)
        builder.emit('LOAD_FAST', index)


class __extend__(ConstantInt):

    def compile(self, builder):
        index = builder.register_int_const(self.value)
        builder.emit('LOAD_CONST', index)


class __extend__(ConstantString):

    def compile(self, builder):
        index = builder.register_string_const(self.value)
        builder.emit('LOAD_CONST', index)


class __extend__(FunctionDeclaration):

    def compile(self, builder):
        from pie.compiling.compiling import BytecodeBuilder

        # creating context to compile function's body
        function_bytecode_builder = BytecodeBuilder()
        # compiling
        self.body.compile(function_bytecode_builder)
        bytecode = function_bytecode_builder.create_bytecode()

        # preparing arguments
        arguments = []
        for argument in self.arguments:
            assert isinstance(argument, Variable)
            name = argument.name
            assert isinstance(name, Identifier)
            arguments.append(name.value)

        # registering function in current builder, so it will be added to
        # bytecode
        name = self.name
        assert isinstance(name, Identifier)
        builder.register_function(name.value, arguments, bytecode)
