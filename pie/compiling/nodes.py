" Module, defining how each node of ast is compiled "

from pie.ast.nodes import *

class __extend__(EmptyStatement):

    def compile(self, builder):
        # it is really empty
        pass


class __extend__(StatementsList):

    def compile(self, builder):
        for statement in self.list:
            statement.compile(builder)
            # for statements, that have results, we need to remove it from the
            # stack, because it won't be used anyway
            if isinstance(statement, AstNodeWithResult):
                builder.emit('POP_STACK');


class __extend__(Echo):

    def compile(self, builder):
        # echoing expressions one by one
        for expression in self.list:
            expression.compile(builder)
            builder.emit('ECHO')


class __extend__(Return):

    def compile(self, builder):
        self.expression.compile(builder)
        builder.emit('RETURN')


class __extend__(FunctionCall):

    def compile(self, builder):
        for i in range(0, len(self.parameters)):
            self.parameters[-1 * i].compile(builder)

        name = self.name
        if isinstance(name, Identifier):
            index = builder.register_name(name.value)
            builder.emit("LOAD_NAME", index)
        else:
            name.compile(builder)

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
            '.': 'CONCAT',
        }

        return operations[self.operation]


class __extend__(Assignment):

    def compile(self, builder):
        # compiling value first, so result would be on the stack for us
        self.value.compile(builder)
        # registering var name in builder
        assert isinstance(self.variable, Variable)
        identifier = self.variable.name
        assert isinstance(identifier, Identifier)
        index = builder.register_name(identifier.value)

        operation = self.get_modification_operation()
        if operation:
            builder.emit('LOAD_FAST', index)
            builder.emit(operation)

        builder.emit('STORE_FAST', index)

    def get_modification_operation(self):
        operations = {
            '=': '',
            '+=': 'ADD',
            '-=': 'SUBSTRACT',
            '*=': 'MULTIPLY',
            '/=': 'DIVIDE',
            '.=': 'CONCAT',
            '%=': 'MOD',
        }

        return operations[self.operator]


class __extend__(TernaryOperator):

    def compile(self, builder):
        # evaluating condition
        self.condition.compile(builder)
        jump_if_false_position = builder.emit('JUMP_IF_FALSE', 0) + 1

        self.left.compile(builder)
        builder.emit('JUMP', 0)
        # adding jump opcode and saving position of it's parameter
        # to patch it later to end of statement's position
        jump_position = builder.get_current_position() - 2
        builder.update_to_current_position(jump_if_false_position)

        self.right.compile(builder)
        builder.update_to_current_position(jump_position)


class __extend__(IncremenetDecrement):

    def get_operation(self):
        operations = {
            '++': 'ADD',
            '--': 'SUBSTRACT',
        }

        return operations[self.operator]


class __extend__(PreIncremenetDecrement):

    def compile(self, builder):
        # registering var name in builder
        assert isinstance(self.variable, Variable)
        identifier = self.variable.name
        assert isinstance(identifier, Identifier)
        index = builder.register_name(identifier.value)

        builder.emit('LOAD_FAST', index)
        self.constant.compile(builder)
        builder.emit(self.get_operation())

        builder.emit('STORE_FAST', index)


class __extend__(PostIncremenetDecrement):

    def compile(self, builder):
        # registering var name in builder
        assert isinstance(self.variable, Variable)
        identifier = self.variable.name
        assert isinstance(identifier, Identifier)
        index = builder.register_name(identifier.value)

        builder.emit('LOAD_FAST', index)
        builder.emit('DUPLICATE_TOP')
        self.constant.compile(builder)
        builder.emit(self.get_operation())
        builder.emit('STORE_FAST', index)
        builder.emit('POP_STACK')


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
            identifier = argument.name
            assert isinstance(identifier, Identifier)
            arguments.append(identifier.value)

        # registering function in current builder, so it will be added to
        # bytecode
        identifier = self.name
        assert isinstance(identifier, Identifier)
        builder.register_function(identifier.value, arguments, bytecode)


class __extend__(If):

    def compile(self, builder):
        self.condition.compile(builder)
        # in case body or else branch is empty, we don't need some jumps
        bodyempty = isinstance(self.body, EmptyStatement)
        elseempty = isinstance(self.else_branch, EmptyStatement)

        if bodyempty and elseempty:
            builder.emit('POP_STACK')
            return

        if bodyempty:
            jump_if_true_position = builder.emit('JUMP_IF_TRUE', 0) + 1
            self.else_branch.compile(builder)
            builder.update_to_current_position(jump_if_true_position)
            return

        jump_if_false_position = builder.emit('JUMP_IF_FALSE', 0) + 1
        self.body.compile(builder)

        if elseempty:
            builder.update_to_current_position(jump_if_false_position)
            return

        jump_position = builder.emit('JUMP', 0) + 1
        builder.update_to_current_position(jump_if_false_position)
        self.else_branch.compile(builder)
        builder.update_to_current_position(jump_position)


class __extend__(While):

    def compile(self, builder):
        # first we need to save position, so we can get back here after block
        start_position = builder.get_current_position()
        # now we can compile expression, that will leave it's result on stack
        self.expression.compile(builder)
        if isinstance(self.body, EmptyStatement):
            builder.emit('JUMP_IF_TRUE', start_position)
            return

        # now we can check if condition is false and jump out
        jump_if_false_position = builder.emit('JUMP_IF_FALSE', 0) + 1
        # compiling body
        self.body.compile(builder)
        # jumping back to the start
        builder.emit('JUMP', start_position)
        builder.update_to_current_position(jump_if_false_position)


class __extend__(DoWhile):

    def compile(self, builder):
        start_position = builder.get_current_position()
        self.body.compile(builder)
        self.expression.compile(builder)
        builder.emit('JUMP_IF_TRUE', start_position)


class __extend__(For):

    def compile(self, builder):
        # init statements are compiled only once, before loop
        for statement in self.init_statements:
            statement.compile(builder)
            builder.emit('POP_STACK');

        # saving starting position to return here after one iteration ends
        start_position = builder.get_current_position()
        # all conditinal statements should be executed every time
        # but only the last one is considered condition
        for index in range(0, len(self.condition_statements) - 1):
            self.condition_statements[index].compile(builder)
            builder.emit('POP_STACK');
        self.condition_statements[-1].compile(builder)
        # now we can check if condition is false and jump out
        jump_if_false_position = builder.emit('JUMP_IF_FALSE', 0) + 1
        # compiling body
        self.body.compile(builder)

        # compiling loop expressions
        for statement in self.expression_statements:
            statement.compile(builder)
            builder.emit('POP_STACK');

        # jumping back to the start
        builder.emit('JUMP', start_position)
        builder.update_to_current_position(jump_if_false_position)
