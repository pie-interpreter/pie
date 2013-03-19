" Module, defining how each node of ast is compiled "

import pie.ast.nodes as nodes
from pie.compiling import util
from pie.objspace import space
from pie.interpreter.functions.user import UserFunction


class __extend__(nodes.AstNode):

    def compile(self, builder):
        builder.line = self.line
        self.compile_node(builder)

    def compile_name(self, builder):
        raise NotImplementedError


class __extend__(nodes.EmptyStatement):

    def compile_node(self, builder):
        # it is really empty
        pass


class __extend__(nodes.StatementsList):

    def compile_node(self, builder):
        for statement in self.list:
            statement.compile(builder)
            # for statements, that have results, we need to remove it from the
            # stack, because it won't be used anyway
            if isinstance(statement, nodes.AstNodeWithResult):
                builder.emit('POP_STACK')


class __extend__(nodes.Print):

    def compile_node(self, builder):
        self.value.compile(builder)
        builder.emit('PRINT')


class __extend__(nodes.Echo):

    def compile_node(self, builder):
        # echoing expressions one by one
        for expression in self.list:
            expression.compile(builder)
            builder.emit('ECHO')


class __extend__(nodes.Include):

    def compile_node(self, builder):
        self.value.compile(builder)
        builder.emit('INCLUDE')


class __extend__(nodes.IncludeOnce):

    def compile_node(self, builder):
        self.value.compile(builder)
        builder.emit('INCLUDE_ONCE')


class __extend__(nodes.Require):

    def compile_node(self, builder):
        self.value.compile(builder)
        builder.emit('REQUIRE')


class __extend__(nodes.RequireOnce):

    def compile_node(self, builder):
        self.value.compile(builder)
        builder.emit('REQUIRE_ONCE')


class __extend__(nodes.Return):

    def compile_node(self, builder):
        if isinstance(self.expression, nodes.EmptyStatement):
            index = builder.register_const(nodes.ConstantNull())
            builder.emit('LOAD_CONST', index)
        else:
            self.expression.compile(builder)

        builder.emit('RETURN')


class __extend__(nodes.Break):

    def compile_node(self, builder):
        jump_position = builder.emit('JUMP', 0) + 1
        builder.add_break_position_to_patch(self.level, jump_position)


class __extend__(nodes.Continue):

    def compile_node(self, builder):
        jump_position = builder.emit('JUMP', 0) + 1
        builder.add_continue_position_to_patch(self.level, jump_position)


class __extend__(nodes.Isset):

    def compile_node(self, builder):
        for statement in self.list:
            statement.compile(builder)

        builder.emit('ISSET', len(self.list))


class __extend__(nodes.Unset):

    def compile_node(self, builder):
        for statement in self.list:
            statement.compile(builder)

        builder.emit('UNSET', len(self.list))


class __extend__(nodes.Empty):

    def compile_node(self, builder):
        self.expression.compile(builder)
        if isinstance(self.expression, nodes.VariableExpression):
            builder.emit('EMPTY_VAR')
        else:
            builder.emit('EMPTY_RESULT')


class __extend__(nodes.ArrayDeclaration):

    def compile_node(self, builder):
        for value in self.values:
            value.key.compile_node(builder)
            value.array_value.compile_node(builder)

        builder.emit('MAKE_ARRAY', len(self.values) * 2)


class __extend__(nodes.BinaryOperator):

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


class __extend__(nodes.Xor):

    def compile_node(self, builder):
        self.left.compile(builder)
        self.right.compile(builder)
        builder.emit('XOR')


class __extend__(nodes.Or):

    def compile_node(self, builder):
        self.left.compile(builder)
        jump_if_false_position = builder.emit('JUMP_IF_TRUE') + 1
        builder.emit('POP_STACK')
        self.right.compile(builder)
        builder.update_to_current_position(jump_if_false_position)
        builder.emit('CAST_TO_BOOL')


class __extend__(nodes.And):

    def compile_node(self, builder):
        self.left.compile(builder)
        jump_if_false_position = builder.emit('JUMP_IF_FALSE') + 1
        builder.emit('POP_STACK')
        self.right.compile(builder)
        builder.update_to_current_position(jump_if_false_position)
        builder.emit('CAST_TO_BOOL')


class __extend__(nodes.Assignment):

    def compile_node(self, builder):
        # compiling value first, so result would be on the stack for us
        self.value.compile(builder)

        operation = self.get_modification_operation()
        if not operation:
            self.variable.compile_mode = nodes.VariableExpression.STORE
            self.variable.compile_node(builder)
        else:
            self.variable.compile(builder)
            builder.emit(operation)

    def get_modification_operation(self):
        operations = {
            '=': 'STORE_VAR',
            '+=': 'INPLACE_ADD',
            '-=': 'INPLACE_SUBSTRACT',
            '.=': 'INPLACE_CONCAT',
            '*=': 'INPLACE_MULTIPLY',
            '/=': 'INPLACE_DIVIDE',
            '%=': 'INPLACE_MOD',
        }

        return operations[self.operator]


class __extend__(nodes.ReferenceAssignment):

    def compile_node(self, builder):
        self.source.compile(builder)
        self.target.compile(builder)
        builder.emit('MAKE_REFERENCE')


class __extend__(nodes.TernaryOperator):

    def compile_node(self, builder):
        leftempty = isinstance(self.left, nodes.EmptyStatement)

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


class __extend__(nodes.Not):

    def compile_node(self, builder):
        self.value.compile(builder)
        builder.emit('NOT')


class __extend__(nodes.IncrementDecrement):

    def compile_node(self, builder):
        self.variable.compile(builder)
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


class __extend__(nodes.Cast):

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


class __extend__(nodes.VariableExpression):

    def compile_node(self, builder):
        self.variable_value.compile_mode = self.compile_mode
        self.variable_value.compile(builder)


class __extend__(nodes.ArrayDereferencing):

    def compile_node(self, builder):
        "Array dereferencing behaves the same for all operations"
        indexes_len = len(self.indexes)
        for index in self.indexes:
            index.compile(builder)

        self.variable.compile_mode = nodes.VariableExpression.NAME
        self.variable.compile(builder)
        if indexes_len == 1:
            builder.emit('GET_INDEX')
        else:
            builder.emit('GET_INDEXES', indexes_len)

        if self.compile_mode == nodes.VariableExpression.STORE:
            builder.emit('STORE_VAR')


class __extend__(nodes.DynamicVariable):

    def compile_node(self, builder):
        self.expression.compile(builder)
        if self.compile_mode == nodes.VariableExpression.STORE:
            builder.emit('STORE_VAR')
        elif self.compile_mode == nodes.VariableExpression.LOAD:
            builder.emit('LOAD_VAR')


class __extend__(nodes.Variable):

    def compile_node(self, builder):
        if self.compile_mode == nodes.VariableExpression.STORE:
            builder.emit('STORE_VAR_FAST', self._register_self(builder))
        elif self.compile_mode == nodes.VariableExpression.LOAD:
            builder.emit('LOAD_VAR_FAST', self._register_self(builder))
        else:
            builder.emit('LOAD_NAME', self._register_self(builder))

    def _register_self(self, builder):
        return builder.register_name(self.name.str_value)


class __extend__(nodes.FunctionCall):

    def compile_node(self, builder):
        for parameter in self.parameters:
            parameter.compile(builder)

        name = self.name
        if isinstance(name, nodes.Identifier):
            index = builder.register_name(name.str_value)
            builder.emit("LOAD_NAME", index)
        else:
            name.compile(builder)

        builder.emit("CALL_FUNCTION", len(self.parameters))


class __extend__(nodes.FunctionDeclaration):

    def compile_node(self, builder):
        function_builder = builder.get_child_builder()
        self.body.compile(function_builder)
        bytecode = function_builder.create_bytecode()

        # preparing arguments
        arguments = []
        for argument in self.arguments:
            assert isinstance(argument, nodes.Argument)
            arguments.append(argument.get_argument_tuple())

        return_type = UserFunction.VALUE
        if self.is_returning_reference:
            return_type = UserFunction.REFERENCE

        identifier = self.name
        function = UserFunction(
            identifier.str_value, return_type, bytecode, arguments, self.line)

        if self.top_level:
            builder.register_declared_function(function)
        else:
            index = builder.register_function(function)
            builder.emit('DECLARE_FUNCTION', index)


class __extend__(nodes.Argument):

    def get_argument_tuple(self):
        return (
            self._get_argument_name(),
            self._get_argument_type(),
            self._get_argument_default_value())

    def _get_argument_name(self):
        identifier = self.variable.name
        return identifier.str_value

    def _get_argument_type(self):
        return UserFunction.VALUE

    def _get_argument_default_value(self):
        return None


class __extend__(nodes.ArgumentWithDefaultValue):

    def _get_argument_default_value(self):
        assert isinstance(self.value, nodes.Constant)
        self.value.calculate_const_value()
        return self.value.get_compiled_value()


class __extend__(nodes.ArgumentReference):

    def _get_argument_type(self):
        return UserFunction.REFERENCE


class __extend__(nodes.ArgumentReferenceWithDefaultValue):

    def _get_argument_type(self):
        return UserFunction.REFERENCE


class __extend__(nodes.If):

    def compile_node(self, builder):
        self.condition.compile(builder)
        # in case body or else branch is empty, we don't need some jumps
        bodyempty = isinstance(self.body, nodes.EmptyStatement)
        elseempty = isinstance(self.else_branch, nodes.EmptyStatement)

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


class __extend__(nodes.While):

    def compile_node(self, builder):
        builder.register_loop()

        # first we need to save position, so we can get back here after block
        start_position = builder.get_current_position()
        # now we can compile expression, that will leave it's result on stack
        self.expression.compile(builder)
        if isinstance(self.body, nodes.EmptyStatement):
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


class __extend__(nodes.DoWhile):

    def compile_node(self, builder):
        builder.register_loop()

        start_position = builder.get_current_position()
        self.body.compile(builder)
        condition_position = builder.get_current_position()
        self.expression.compile(builder)
        builder.emit('JUMP_IF_TRUE', start_position)

        builder.patch_continue_positions(condition_position)
        builder.patch_break_positions(builder.get_current_position())


class __extend__(nodes.For):

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


class __extend__(nodes.Foreach):

    def compile_node(self, builder):
        builder.register_loop()

        self.inner.compile_init(builder)
        start_position = builder.get_current_position()

        self.inner.compile_next(builder)
        self.body.compile(builder)
        self.inner.compile_validate(builder, start_position)

        builder.patch_continue_positions(start_position)
        builder.patch_break_positions(builder.get_current_position())


class __extend__(nodes.ForeachInner):

    def compile_init(self, builder):
        if self.is_constant:
            self.key.compile(builder)
            self.value.compile(builder)
            self.array.compile(builder)
            if self.is_reference:
                builder.emit('ITERATOR_CREATE')
            else:
                builder.emit('ITERATOR_CREATE_REF')
        else:
            builder.emit('ITERATOR_RESET')

    def compile_next(self, builder):
        if self.is_constant:
            builder.emit('ITERATOR_NEXT')
        else:
            builder.emit('ITERATOR_GET_NEXT_KEY')
            self.key.compile(builder)
            builder.emit('STORE_VAR')

            builder.emit('ITERATOR_GET_NEXT_VALUE')
            self.value.compile(builder)
            if self.is_reference:
                builder.emit('MAKE_REFERENCE')
            else:
                builder.emit('STORE_VAR')

    def compile_validate(self, builder, start_position):
        builder.emit('ITERATOR_JUMP_IF_NOT_VALID', start_position)


class __extend__(nodes.Switch):

    def compile_node(self, builder):
        builder.register_loop()  # even though it's not a loop :)

        self.expression.compile(builder)

        # building conditions first
        positions = []
        default_position_index = -1
        for case in self.cases_list:
            if isinstance(case, nodes.SwitchDefault):
                default_position_index = len(positions)
                positions.append(-1)
                continue

            builder.emit('DUPLICATE_TOP')
            case.expression.compile(builder)
            builder.emit('EQUAL')

            positions.append(builder.emit('JUMP_IF_TRUE', 0) + 1)

        last_position = builder.emit('JUMP', 0) + 1
        if default_position_index >= 0:
            positions[default_position_index] = last_position

        index = 0
        for case in self.cases_list:
            builder.update_to_current_position(positions[index])
            case.body.compile(builder)
            index += 1

        builder.emit('POP_STACK')

        if default_position_index < 0:
            builder.update_to_current_position(last_position)

        builder.patch_continue_positions(builder.get_current_position())
        builder.patch_break_positions(builder.get_current_position())


class __extend__(nodes.Constant):

    def compile_node(self, builder):
        self.calculate_const_value()  # needed for calculations
        index = builder.register_const(self)
        builder.emit('LOAD_CONST', index)

    def get_str_value(self):
        " Used for caching in builder "
        raise NotImplementedError

    def get_compiled_value(self):
        raise NotImplementedError

    def calculate_const_value(self):
        " Some types of constants need pre-calculation of values"


class __extend__(nodes.ConstantInt):

    type_name = 'int'

    def get_str_value(self):
        return str(self.const_value)

    def get_compiled_value(self):
        return space.int(self.const_value)


class __extend__(nodes.ConstantIntBin):

    def calculate_const_value(self):
        self.const_value = int(self.value[2:], 2)
        if self.sign == '-':
            self.const_value = -self.const_value


class __extend__(nodes.ConstantIntOct):

    def calculate_const_value(self):
        self.const_value = int(self.value, 8)
        if self.sign == '-':
            self.const_value = -self.const_value


class __extend__(nodes.ConstantIntDec):

    def calculate_const_value(self):
        self.const_value = int(self.value)
        if self.sign == '-':
            self.const_value = -self.const_value


class __extend__(nodes.ConstantIntHex):

    def calculate_const_value(self):
        self.const_value = int(self.value[2:], 16)
        if self.sign == '-':
            self.const_value = -self.const_value


class __extend__(nodes.ConstantFloat):

    type_name = 'float'

    def get_str_value(self):
        return str(self.const_value)

    def get_compiled_value(self):
        return space.float(self.const_value)

    def calculate_const_value(self):
        self.const_value = float(self.value)
        if self.sign == '-':
            self.const_value = -self.const_value


class __extend__(nodes.ConstantBool):

    type_name = 'bool'

    def get_str_value(self):
        return str(self.value)

    def get_compiled_value(self):
        return space.bool(self.value)


class __extend__(nodes.ConstantArray):

    type_name = 'array'

    def get_str_value(self):
        string_values = []
        for value in self.all_values:
            value.calculate_const_value()
            string_values.append(value.get_str_value())

        return ''.join(['[', ''.join(string_values), ']'])

    def get_compiled_value(self):
        array_values = []
        for value in self.all_values:
            array_values.append(value.get_compiled_value())

        return space.array(array_values)

    def calculate_const_value(self):
        self.all_values = []
        for value in self.values:
            value.key.calculate_const_value()
            value.array_value.calculate_const_value()
            self.all_values.append(value.key)
            self.all_values.append(value.array_value)


class __extend__(nodes.ConstantNull):

    type_name = 'null'

    def get_str_value(self):
        return 'null'

    def get_compiled_value(self):
        return space.null()


class __extend__(nodes.ConstantUndefined):

    type_name = 'undefined'

    def get_str_value(self):
        return 'undefined'

    def get_compiled_value(self):
        return space.undefined()


class __extend__(nodes.ConstantString):

    type_name = 'string'

    def calculate_const_value(self):
        self.const_value = self.value

    def get_str_value(self):
        return self.const_value

    def get_compiled_value(self):
        return space.str(self.const_value)


class __extend__(nodes.ConstantSingleQuotedString):

    def calculate_const_value(self):
        self.const_value = util.process_single_quoted_string(self.value)


class __extend__(nodes.ConstantDoubleQuotedString):

    def calculate_const_value(self):
        self.const_value = util.process_double_quoted_string(self.value)
