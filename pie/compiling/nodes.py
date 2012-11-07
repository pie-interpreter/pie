" Module, defining how each node of ast is compiled "

from pie.ast.nodes import *
from pie.compiling import util


class __extend__(AstNode):

    def compile(self, builder):
        builder.line = self.line
        self.compile_node(builder)


class __extend__(EmptyStatement):

    def compile_node(self, builder):
        # it is really empty
        pass


class __extend__(StatementsList):

    def compile_node(self, builder):
        for statement in self.list:
            statement.compile(builder)
            # for statements, that have results, we need to remove it from the
            # stack, because it won't be used anyway
            if isinstance(statement, AstNodeWithResult):
                builder.emit('POP_STACK')


class __extend__(Print):

    def compile_node(self, builder):
        self.value.compile(builder)
        builder.emit('PRINT')


class __extend__(Echo):

    def compile_node(self, builder):
        # echoing expressions one by one
        for expression in self.list:
            expression.compile(builder)
            builder.emit('ECHO')


class __extend__(Include):

    def compile_node(self, builder):
        self.value.compile(builder)
        builder.emit('INCLUDE')


class __extend__(IncludeOnce):

    def compile_node(self, builder):
        self.value.compile(builder)
        builder.emit('INCLUDE_ONCE')


class __extend__(Require):

    def compile_node(self, builder):
        self.value.compile(builder)
        builder.emit('REQUIRE')


class __extend__(RequireOnce):

    def compile_node(self, builder):
        self.value.compile(builder)
        builder.emit('REQUIRE_ONCE')


class __extend__(Return):

    def compile_node(self, builder):
        if isinstance(self.expression, EmptyStatement):
            index = builder.register_null_const()
            builder.emit('LOAD_CONST', index)
        else:
            self.expression.compile(builder)

        builder.emit('RETURN')


class __extend__(Break):

    def compile_node(self, builder):
        jump_position = builder.emit('JUMP', 0) + 1
        builder.add_break_position_to_patch(self.level, jump_position)


class __extend__(Continue):

    def compile_node(self, builder):
        jump_position = builder.emit('JUMP', 0) + 1
        builder.add_continue_position_to_patch(self.level, jump_position)


class __extend__(Isset):

    def compile_node(self, builder):
        for statement in self.list:
            index = builder.register_name(_get_variable_name(statement))
            builder.emit('LOAD_NAME', index)

        builder.emit('ISSET', len(self.list))


class __extend__(Unset):

    def compile_node(self, builder):
        for statement in self.list:
            index = builder.register_name(_get_variable_name(statement))
            builder.emit('LOAD_NAME', index)

        builder.emit('UNSET', len(self.list))


class __extend__(Empty):

    def compile_node(self, builder):
        if isinstance(self.expression, Variable):
            index = builder.register_name(_get_variable_name(self.expression))
            builder.emit('LOAD_NAME', index)
            builder.emit('EMPTY_VAR')
        else:
            self.expression.compile(builder)
            builder.emit('EMPTY_RESULT')


class __extend__(BinaryOperator):

    def compile_node(self, builder):
        self.left.compile(builder)
        self.right.compile(builder)
        opcode = self.get_binary_opcode()
        builder.emit(opcode)

    def get_binary_opcode(self):
        operations = {
            '+': 'ADD',
            '-': 'SUBSTRACT',
            '.': 'CONCAT',
            '*': 'MULTIPLY',
            '/': 'DIVIDE',
            '%': 'MOD',
            '<': 'LESS_THAN',
            '>': 'MORE_THAN',
            '<=': 'LESS_THAN_OR_EQUAL',
            '>=': 'MORE_THAN_OR_EQUAL',
            '==': 'EQUAL',
            '!=': 'NOT_EQUAL',
            '<>': 'NOT_EQUAL',
            '===': 'IDENTICAL',
            '!==': 'NOT_IDENTICAL',
        }

        return operations[self.operation]


class __extend__(Xor):

    def compile_node(self, builder):
        self.left.compile(builder)
        self.right.compile(builder)
        builder.emit('XOR')


class __extend__(Or):

    def compile_node(self, builder):
        self.left.compile(builder)
        jump_if_false_position = builder.emit('JUMP_IF_TRUE') + 1
        builder.emit('POP_STACK')
        self.right.compile(builder)
        builder.update_to_current_position(jump_if_false_position)
        builder.emit('CAST_TO_BOOL')


class __extend__(And):

    def compile_node(self, builder):
        self.left.compile(builder)
        jump_if_false_position = builder.emit('JUMP_IF_FALSE') + 1
        builder.emit('POP_STACK')
        self.right.compile(builder)
        builder.update_to_current_position(jump_if_false_position)
        builder.emit('CAST_TO_BOOL')


class __extend__(Assignment):

    def compile_node(self, builder):
        # compiling value first, so result would be on the stack for us
        self.value.compile(builder)
        index = builder.register_name(_get_variable_name(self.variable))

        operation = self.get_modification_operation()
        if operation:  # inplace operation
            builder.emit('LOAD_NAME', index)
            builder.emit(operation)
        else:  # simple assign
            builder.emit('STORE_VAR_FAST', index)

    def get_modification_operation(self):
        operations = {
            '=': '',
            '+=': 'INPLACE_ADD',
            '-=': 'INPLACE_SUBSTRACT',
            '.=': 'INPLACE_CONCAT',
            '*=': 'INPLACE_MULTIPLY',
            '/=': 'INPLACE_DIVIDE',
            '%=': 'INPLACE_MOD',
        }

        return operations[self.operator]


class __extend__(TernaryOperator):

    def compile_node(self, builder):
        leftempty = isinstance(self.left, EmptyStatement)

        self.condition.compile(builder)

        # if first expression is empty, we need to use result of condition instead
        if leftempty:
            builder.emit("DUPLICATE_TOP")
            jump_if_true_position = builder.emit('JUMP_IF_TRUE', 0) + 1
            builder.emit('POP_STACK')
            self.right.compile(builder)
            builder.update_to_current_position(jump_if_true_position)
        else:
            jump_if_false_position = builder.emit('JUMP_IF_FALSE', 0) + 1
            self.left.compile(builder)
            jump_position = builder.emit('JUMP', 0) + 1
            builder.update_to_current_position(jump_if_false_position)
            self.right.compile(builder)
            builder.update_to_current_position(jump_position)


class __extend__(Not):

    def compile_node(self, builder):
        self.value.compile(builder)
        builder.emit('NOT')


class __extend__(IncrementDecrement):

    def compile_node(self, builder):
        # registering var name in builder
        index = builder.register_name(_get_variable_name(self.variable))

        builder.emit('LOAD_NAME', index)
        builder.emit(self.get_operation())

    def get_operation(self):
        operations = {
            self.PRE: {
                '++': 'PRE_INCREMENT',
                '--': 'PRE_DECREMENT',
            },
            self.POST: {
                '++': 'POST_INCREMENT',
                '--': 'POST_DECREMENT',
            },
        }

        return operations[self.type][self.operator]


class __extend__(Cast):

    def compile_node(self, builder):
        self.value.compile(builder)
        builder.emit(self.get_operation())

    def get_operation(self):
        operations = {
            'T_ARRAY_CAST': 'CAST_TO_ARRAY',
            'T_BOOL_CAST': 'CAST_TO_BOOL',
            'T_DOUBLE_CAST': 'CAST_TO_DOUBLE',
            'T_INT_CAST': 'CAST_TO_INT',
            'T_OBJECT_CAST': 'CAST_TO_OBJECT',
            'T_STRING_CAST': 'CAST_TO_STRING',
            'T_UNSET_CAST': 'CAST_TO_UNSET'
        }

        return operations[self.symbol]


class __extend__(Variable):

    def compile_node(self, builder):
        index = builder.register_name(_get_variable_name(self))
        builder.emit('LOAD_VAR_FAST', index)


class __extend__(FunctionCall):

    def compile_node(self, builder):
        for i in range(0, len(self.parameters)):
            self.parameters[-1 * i].compile(builder)

        name = self.name
        if isinstance(name, Identifier):
            index = builder.register_name(name.value)
            builder.emit("LOAD_NAME", index)
        else:
            name.compile(builder)

        builder.emit("CALL_FUNCTION", len(self.parameters))


class __extend__(FunctionDeclaration):

    def compile_node(self, builder):
        # creating context to compile function's body
        function_bytecode_builder = builder.get_child_builder()
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

    def compile_node(self, builder):
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

    def compile_node(self, builder):
        builder.register_loop()

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

        builder.patch_continue_positions(start_position)
        builder.patch_break_positions(builder.get_current_position())


class __extend__(DoWhile):

    def compile_node(self, builder):
        builder.register_loop()

        start_position = builder.get_current_position()
        self.body.compile(builder)
        condition_position = builder.get_current_position()
        self.expression.compile(builder)
        builder.emit('JUMP_IF_TRUE', start_position)

        builder.patch_continue_positions(condition_position)
        builder.patch_break_positions(builder.get_current_position())


class __extend__(For):

    def compile_node(self, builder):
        builder.register_loop()

        # init statements are compiled only once, before loop
        for statement in self.init_statements:
            statement.compile(builder)
            builder.emit('POP_STACK')

        # saving starting position to return here after one iteration ends
        start_position = builder.get_current_position()
        jump_if_false_position = 0
        if self.condition_statements:
            # all conditinal statements should be executed every time
            # but only the last one is considered condition
            for index in range(0, len(self.condition_statements) - 1):
                self.condition_statements[index].compile(builder)
                builder.emit('POP_STACK')
            self.condition_statements[-1].compile(builder)
            # now we can check if condition is false and jump out
            jump_if_false_position = builder.emit('JUMP_IF_FALSE', 0) + 1

        # compiling body
        self.body.compile(builder)

        # compiling loop expressions
        for statement in self.expression_statements:
            statement.compile(builder)
            builder.emit('POP_STACK')

        # jumping back to the start
        builder.emit('JUMP', start_position)

        if self.condition_statements:
            builder.update_to_current_position(jump_if_false_position)

        builder.patch_continue_positions(start_position)
        builder.patch_break_positions(builder.get_current_position())


class __extend__(ConstantIntBin):

    def compile_node(self, builder):
        value = int(self.value[2:], 2)
        if self.sign == '-':
            value = -value
        index = builder.register_int_const(value)
        builder.emit('LOAD_CONST', index)


class __extend__(ConstantIntOct):

    def compile_node(self, builder):
        value = int(util.validate_oct(self.value), 8)
        if self.sign == '-':
            value = -value
        index = builder.register_int_const(value)
        builder.emit('LOAD_CONST', index)


class __extend__(ConstantIntDec):

    def compile_node(self, builder):
        value = int(self.value)
        if self.sign == '-':
            value = -value
        index = builder.register_int_const(value)
        builder.emit('LOAD_CONST', index)


class __extend__(ConstantIntHex):

    def compile_node(self, builder):
        value = int(self.value[2:], 16)
        if self.sign == '-':
            value = -value
        index = builder.register_int_const(value)
        builder.emit('LOAD_CONST', index)


class __extend__(ConstantBool):

    def compile_node(self, builder):
        index = builder.register_bool_const(self.value)
        builder.emit('LOAD_CONST', index)


class __extend__(ConstantNull):

    def compile_node(self, builder):
        index = builder.register_null_const()
        builder.emit('LOAD_CONST', index)


class __extend__(ConstantString):

    def compile_node(self, builder):
        index = builder.register_string_const(self.value)
        builder.emit('LOAD_CONST', index)


class __extend__(ConstantSingleQuotedString):

    def compile_node(self, builder):
        value = util.process_single_quoted_string(self.value)
        index = builder.register_string_const(value)
        builder.emit('LOAD_CONST', index)


class __extend__(ConstantDoubleQuotedString):

    def compile_node(self, builder):
        value = util.process_double_quoted_string(self.value)
        index = builder.register_string_const(value)
        builder.emit('LOAD_CONST', index)


def _get_variable_name(var):
    assert isinstance(var, Variable)
    identifier = var.name
    assert isinstance(identifier, Identifier)

    return identifier.value
