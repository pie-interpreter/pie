""" Module, providing ast building tools """
from rpython.rlib.parsing.tree import RPythonVisitor

from pie.ast.nodes import *
from pie.parsing import parsing


def build(source):
    parse_tree = parsing.parse(source)
    astree = build_ast(parse_tree)

    return astree


def build_ast(parse_tree):
    """ Build as AST from parse tree """
    return builder.transform(parse_tree)


class AstBuilder(RPythonVisitor):
    """ Class, than transforms parse tree to AST """

    def transform(self, node):
        ast_node = self.dispatch(node)
        ast_node.line = node.getsourcepos().lineno + 1

        return ast_node

    def visit_file(self, node):
        """ Visit root node of the parse tree """
        if len(node.children) == 1 and node.children[0].symbol == 'EOF':
            return EmptyStatement()

        return self.visit_statements_block(node)

    def visit_statements_block(self, node):
        return StatementsList(self.get_children_as_list(node))

    def visit_construct_print(self, node):
        return Print(self.get_second_child(node))

    def visit_construct_echo(self, node):
        statments_list = self.get_children_as_list(node)
        # first item in the list is "echo" token
        return Echo(statments_list[1:])

    def visit_construct_include(self, node):
        return Include(self.get_second_child(node))

    def visit_construct_include_once(self, node):
        return IncludeOnce(self.get_second_child(node))

    def visit_construct_require(self, node):
        return Require(self.get_second_child(node))

    def visit_construct_require_once(self, node):
        return RequireOnce(self.get_second_child(node))

    def visit_construct_return(self, node):
        return Return(self.get_second_child_if_exists(node))

    def visit_construct_break(self, node):
        children_count = len(node.children)
        assert children_count in [1, 2]

        level = 1
        if children_count == 2:
            level = int(node.children[1].token.source)

        return Break(level)

    def visit_construct_continue(self, node):
        children_count = len(node.children)
        assert children_count in [1, 2]

        level = 1
        if children_count == 2:
            level = int(node.children[1].token.source)

        return Continue(level)

    def visit_construct_isset(self, node):
        assert len(node.children) == 2

        expressions = self.transform(node.children[1])
        return Isset(expressions.list)

    def visit_construct_unset(self, node):
        assert len(node.children) == 2

        expressions = self.transform(node.children[1])
        return Unset(expressions.list)

    def visit_construct_empty(self, node):
        return Empty(self.get_second_child(node))

    def visit_construct_array(self, node):
        children_count = len(node.children)
        assert children_count > 0

        values = []
        for index in range(1, children_count):
            values.append(self.transform(node.children[index]))

        return ArrayDeclaration(values)

    def visit_construct_array_value(self, node):
        children_count = len(node.children)
        assert children_count in [1, 2]

        if children_count == 1:
            return ArrayValue(
                ConstantUndefined(),
                self.transform(node.children[0]))
        else:
            return ArrayValue(
                self.transform(node.children[0]),
                self.transform(node.children[1]))

    def visit_logical_xor_expression(self, node):
        children_count = len(node.children)
        assert children_count >= 2

        left = self.transform(node.children[0])
        right = self.transform(node.children[1])
        operator = Xor(left, right)
        for index in range(2, children_count):
            operator = Xor(operator, self.transform(node.children[index]))

        return operator

    def visit_logical_or_expression(self, node):
        children_count = len(node.children)
        assert children_count >= 2

        left = self.transform(node.children[0])
        right = self.transform(node.children[1])
        operator = Or(left, right)
        for index in range(2, children_count):
            operator = Or(operator, self.transform(node.children[index]))

        return operator

    def visit_logical_and_expression(self, node):
        children_count = len(node.children)
        assert children_count >= 2

        left = self.transform(node.children[0])
        right = self.transform(node.children[1])
        operator = And(left, right)
        for index in range(2, children_count):
            operator = And(operator, self.transform(node.children[index]))

        return operator

    def visit_assign_expression(self, node):
        assert len(node.children) == 3

        variable = self.transform(node.children[0])
        operator = node.children[1].token.source
        value = self.transform(node.children[2])

        return Assignment(variable, operator, value)

    def visit_reference_assignment(self, node):
        assert len(node.children) == 2

        target = self.transform(node.children[0])
        source = self.transform(node.children[1])

        return ReferenceAssignment(target, source)

    def visit_ternary_expression(self, node):
        children_count = len(node.children)
        assert children_count in [2, 3]

        condition = self.transform(node.children[0])
        left = EmptyStatement()
        if children_count == 3:
            left = self.transform(node.children[1])

        right = self.transform(node.children[-1])

        return TernaryOperator(condition, left, right)

    def visit_boolean_or_expression(self, node):
        return self.visit_logical_or_expression(node)

    def visit_boolean_and_expression(self, node):
        return self.visit_logical_and_expression(node)

    def visit_equality_expression(self, node):
        return self.get_binary_operator(node)

    def visit_compare_expression(self, node):
        return self.get_binary_operator(node)

    def visit_additive_expression(self, node):
        return self.get_binary_operator(node)

    def visit_multitive_expression(self, node):
        return self.get_binary_operator(node)

    def visit_logical_not_expression(self, node):
        return Not(self.get_single_child(node))

    def visit_incdec_expression(self, node):
        assert len(node.children) == 2
        if node.children[0].symbol == "variable_expression":
            operation_type = IncrementDecrement.POST
            operator = node.children[1].token.source
            variable = self.transform(node.children[0])
        else:
            operation_type = IncrementDecrement.PRE
            operator = node.children[0].token.source
            variable = self.transform(node.children[1])

        return IncrementDecrement(operation_type, operator, variable)

    def visit_cast_expression(self, node):
        assert len(node.children) == 2
        symbol = node.children[0].symbol
        value = self.transform(node.children[1])

        return Cast(symbol, value)

    def visit_variable_expression(self, node):
        return VariableExpression(self.get_single_child(node))

    def visit_variable_value_expression(self, node):
        node = VariableExpression(self.get_single_child(node))
        node.compile_mode = VariableExpression.LOAD
        return node

    def visit_array_dereferencing_expression(self, node):
        return self.visit_array_dereferencing(node)

    def visit_array_dereferencing(self, node):
        children_count = len(node.children)
        assert children_count >= 2

        variable = self.transform(node.children[0])

        indexes = []
        for index in range(1, children_count):
            indexes.append(self.transform(node.children[index]))

        return ArrayDereferencing(variable, indexes)

    def visit_array_index(self, node):
        if len(node.children) == 1:
            return ConstantUndefined()

        return self.get_second_child(node)

    def visit_variable_dynamic_expression(self, node):
        return DynamicVariable(self.get_second_child(node))

    def visit_function_call(self, node):
        children_count = len(node.children)
        assert children_count in [1, 2]

        name = self.transform(node.children[0])
        if children_count == 2:
            parameters = self.transform(node.children[1])
        else:
            parameters = ItemsList()

        return FunctionCall(name, parameters.list)

    def visit_top_level_function_declaration(self, node):
        function = self.visit_function_declaration(node)
        function.top_level = True
        return function

    def visit_function_declaration(self, node):
        children_count = len(node.children)
        assert children_count in [2, 3, 4, 5]

        parts_index = 1  # index 0 is "function" token
        is_returning_reference = False
        if node.children[1].token.source == '&':
            is_returning_reference = True
            parts_index += 1

        name = self.transform(node.children[parts_index])
        arguments = ItemsList()
        body = EmptyStatement()

        for index in range(parts_index + 1, children_count):
            child = node.children[index]
            if child.symbol == 'function_arguments_list':
                arguments = self.transform(child)
            elif child.symbol == 'statements_block':
                body = self.transform(child)

        return FunctionDeclaration(
            name, is_returning_reference,
            arguments.list, body
        )

    def visit_function_argument_variable(self, node):
        return ArgumentVariable(self.get_single_child(node))

    def visit_function_argument_reference(self, node):
        return ArgumentReference(self.get_single_child(node))

    def visit_function_argument_variable_with_default_value(self, node):
        assert len(node.children) == 2
        return ArgumentVariableWithDefaultValue(
            self.transform(node.children[0]),
            self.transform(node.children[1]))

    def visit_function_argument_reference_with_default_value(self, node):
        assert len(node.children) == 2
        return ArgumentReferenceWithDefaultValue(
            self.transform(node.children[0]),
            self.transform(node.children[1]))

    def visit_if(self, node):
        children_count = len(node.children)
        assert children_count in [2, 3, 4]

        # condition always present
        condition = self.transform(node.children[1])
        body = EmptyStatement()
        else_branch = EmptyStatement()

        for index in range(2, children_count):
            child = node.children[index]
            if child.symbol in ['else', 'else_alt', 'elseif', 'elseif_alt']:
                else_branch = self.transform(child)
            else:
                body = self.transform(child)

        return If(condition, body, else_branch)

    def visit_else(self, node):
        return self.get_second_child_if_exists(node)

    def visit_elseif(self, node):
        return self.visit_if(node)

    def visit_else_alt(self, node):
        return self.get_second_child_if_exists(node)

    def visit_elseif_alt(self, node):
        return self.visit_if(node)

    def visit_while(self, node):
        children_count = len(node.children)
        assert children_count in [2, 3]

        expression = self.transform(node.children[1])
        body = EmptyStatement()
        if children_count > 2:
            body = self.transform(node.children[2])

        return While(expression, body)

    def visit_dowhile(self, node):
        children_count = len(node.children)
        assert children_count in [2, 3]

        expression = self.transform(node.children[-1])
        body = EmptyStatement()
        if children_count > 2:
            body = self.transform(node.children[1])

        return DoWhile(expression, body)

    def visit_for(self, node):
        children_count = len(node.children)
        assert children_count in [1, 2, 3, 4, 5]

        init_statements = []
        condition_statements = []
        expression_statements = []
        body = EmptyStatement()

        for index in range(1, children_count):
            child = node.children[index]
            if child.symbol == 'for_init':
                init_statements = self.transform(child).list
            elif child.symbol == 'for_condition':
                condition_statements = self.transform(child).list
            elif child.symbol == 'for_expression':
                expression_statements = self.transform(child).list
            else:
                body = self.transform(child)

        return For(init_statements,
                   condition_statements,
                   expression_statements,
                   body)

    def visit_foreach(self, node):
        children_count = len(node.children)
        assert children_count in [2, 3]

        inner_statement = self.transform(node.children[1])
        if children_count == 3:
            body = self.transform(node.children[2])
        else:
            body = EmptyStatement()

        return Foreach(inner_statement, body)

    def visit_foreach_inner(self, node):
        children_count = len(node.children)
        assert children_count in [2, 3, 4]

        array_expression = self.transform(node.children[0])
        is_reference = False

        if children_count == 2:
            key_expression = ConstantUndefined()
            value_expression = self.transform(node.children[1])
        elif children_count == 3 \
            and node.children[1].symbol == 'variable_expression':
            key_expression = self.transform(node.children[1])
            value_expression = self.transform(node.children[2])
        elif children_count == 3:
            is_reference = True
            key_expression = ConstantUndefined()
            value_expression = self.transform(node.children[2])
        else:
            is_reference = True
            key_expression = self.transform(node.children[1])
            value_expression = self.transform(node.children[3])

        is_constant = isinstance(value_expression.variable_value, Variable)

        return ForeachInner(
            array_expression,
            key_expression, value_expression,
            is_constant, is_reference)

    def visit_switch(self, node):
        children_count = len(node.children)
        assert children_count >= 2

        expression = self.transform(node.children[1])
        cases_list = []
        for index in range(2, children_count):
            cases_list.append(self.transform(node.children[index]))

        return Switch(expression, cases_list)

    def visit_switch_case(self, node):
        children_count = len(node.children)
        assert children_count in [2, 3]
        expression = self.transform(node.children[1])
        if children_count == 3:
            body = self.transform(node.children[2])
        else:
            body = EmptyStatement()

        return SwitchCase(expression, body)

    def visit_switch_default(self, node):
        children_count = len(node.children)
        assert children_count in [1, 2]
        if children_count == 2:
            body = self.transform(node.children[1])
        else:
            body = EmptyStatement()

        return SwitchDefault(body)

    def visit_int_type(self, node):
        assert len(node.children) == 2
        sign = node.children[0].token.source

        int_constant = self.transform(node.children[1])
        assert isinstance(int_constant, ConstantInt)
        int_constant.sign = sign

        return int_constant

    def visit_float_type(self, node):
        assert len(node.children) == 2
        sign = node.children[0].token.source

        float_constant = self.transform(node.children[1])
        assert isinstance(float_constant, ConstantFloat)
        float_constant.sign = sign

        return float_constant

    def visit_array_type(self, node):
        children_count = len(node.children)
        assert children_count > 0

        values = []
        for index in range(1, children_count):
            values.append(self.transform(node.children[index]))

        return ConstantArray(values)

    def visit_array_type_value(self, node):
        return self.visit_construct_array_value(node)

    def visit_INT_BIN(self, node):
        return ConstantIntBin(node.token.source)

    def visit_INT_OCT(self, node):
        return ConstantIntOct(node.token.source)

    def visit_INT_DEC(self, node):
        return ConstantIntDec(node.token.source)

    def visit_INT_HEX(self, node):
        return ConstantIntHex(node.token.source)

    def visit_FLOAT(self, node):
        return ConstantFloat(node.token.source)

    def visit_SINGLE_QUOTED_STRING(self, node):
        end = len(node.token.source) - 1
        assert end >= 0

        return ConstantSingleQuotedString(node.token.source[1:end])

    def visit_DOUBLE_QUOTED_STRING(self, node):
        end = len(node.token.source) - 1
        assert end >= 0

        return ConstantDoubleQuotedString(node.token.source[1:end])

    def visit_TRUE(self, node):
        return ConstantBool(True)

    def visit_FALSE(self, node):
        return ConstantBool(False)

    def visit_NULL(self, node):
        return ConstantNull()

    def visit_VARIABLE_IDENTIFIER(self, node):
        return Variable(Identifier(node.token.source[1:]))

    def visit_IDENTIFIER(self, node):
        return Identifier(node.token.source)

    def visit_T_INLINE_HTML(self, node):
        return Echo([ConstantString(node.token.source)])

    def general_nonterminal_visit(self, node):
        return ItemsList(self.get_children_as_list(node))

    def general_symbol_visit(self, node):
        return Item(node.token.source)

    def get_single_child(self, node):
        assert len(node.children) == 1
        return self.transform(node.children[0])

    def get_second_child(self, node):
        assert len(node.children) >= 2
        return self.transform(node.children[1])

    def get_second_child_if_exists(self, node):
        children_count = len(node.children)
        assert children_count in [1, 2]

        if children_count == 1:
            return EmptyStatement()

        return self.transform(node.children[1])

    def get_binary_operator(self, node):
        children_count = len(node.children)
        assert children_count >= 3 and children_count % 2 == 1

        left = self.transform(node.children[0])
        right = self.transform(node.children[2])
        operator = BinaryOperator(node.children[1].token.source, left, right)
        for index in range(3, children_count, 2):
            operator = BinaryOperator(node.children[index].token.source,
                                      operator,
                                      self.transform(node.children[index + 1]))

        return operator

    def get_children_as_list(self, node):
        assert len(node.children) > 0

        children_list = []
        for child in node.children:
            children_list.append(self.transform(child))

        return children_list

# Cached AstBuilder instance
builder = AstBuilder()

