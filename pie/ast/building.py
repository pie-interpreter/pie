" Module, providing ast building tools "

from pie.ast.nodes import *
from pypy.rlib.parsing.tree import RPythonVisitor


def build(parseTree):
    """ Build as AST from parse tree """
    return builder.transform(parseTree);


class AstBuilder(RPythonVisitor):
    """ Class, than transforms parse tree to AST """

    def transform(self, node):
        ast_node = self.dispatch(node)
        ast_node.line = node.getsourcepos().lineno + 1

        return ast_node

    def visit_file(self, node):
        """ Visit root node of the parse tree """
        return self.visit_statements_block(node)

    def visit_statements_block(self, node):
        return StatementsList(self.get_children_as_list(node))

    def visit_construct_echo(self, node):
        return Echo(self.get_children_as_list(node))

    def visit_construct_include(self, node):
        return Include(self.get_single_child(node))

    def visit_construct_include_once(self, node):
        return IncludeOnce(self.get_single_child(node))

    def visit_construct_require(self, node):
        return Require(self.get_single_child(node))

    def visit_construct_include_once(self, node):
        return RequireOnce(self.get_single_child(node))

    def visit_construct_return(self, node):
        return Return(self.get_single_child(node))

    def visit_construct_break(self, node):
        children_count = len(node.children)
        assert children_count == 0 or children_count == 1

        level = 1
        if children_count == 1:
            level = int(node.children[0].token.source)

        return Break(level)

    def visit_construct_continue(self, node):
        children_count = len(node.children)
        assert children_count == 0 or children_count == 1

        level = 1
        if children_count == 1:
            level = int(node.children[0].token.source)

        return Continue(level)

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

    def visit_ternary_expression(self, node):
        assert len(node.children) == 3

        condition = self.transform(node.children[0])
        left = self.transform(node.children[1])
        right = self.transform(node.children[2])

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
        if node.children[0].symbol == "variable_identifier":
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

    def visit_variable_identifier(self, node):
        return Variable(self.get_single_child(node))

    def visit_constant_int_expression(self, node):
        assert len(node.children) == 2
        sign = node.children[0].token.source
        value = node.children[1].token.source

        return ConstantInt(int(sign + value))

    def visit_function_call(self, node):
        children_count = len(node.children)
        assert children_count == 1 or children_count == 2

        name = self.transform(node.children[0])
        if children_count == 2:
            parameters = self.transform(node.children[1])
        else:
            parameters = ItemsList()

        return FunctionCall(name, parameters.list)

    def visit_function_declaration(self, node):
        children_count = len(node.children)
        assert children_count >= 1 or children_count <= 3

        name = self.transform(node.children[0])
        # function declaration can have arguments list or/and function body
        # missing, we need to check which is which
        if children_count > 1 \
                and node.children[1].symbol == "function_arguments_list" :
            arguments = self.transform(node.children[1])
        else:
            arguments = ItemsList()

        if children_count > 2 \
                or node.children[1].symbol == "statements_block" :
            body = self.transform(node.children[-1])
        else:
            body = EmptyStatement()

        return FunctionDeclaration(name, arguments.list, body)

    def visit_if(self, node):
        children_count = len(node.children)
        assert children_count > 0 and children_count < 4

        condition = self.transform(node.children[0])
        body = EmptyStatement()
        else_branch = EmptyStatement()
        for index in range(1, children_count):
            child = node.children[index]
            if child.symbol == 'else' or child.symbol == 'elseif':
                else_branch = self.transform(child)
            else:
                body = self.transform(child)

        return If(condition, body, else_branch)

    def visit_else(self, node):
        return self.get_single_child(node)

    def visit_elseif(self, node):
        return self.visit_if(node)

    def visit_while(self, node):
        children_count = len(node.children)
        assert children_count == 1 or children_count == 2

        expression = self.transform(node.children[0])
        if children_count > 1:
            body = self.transform(node.children[1])
        else:
            body = EmptyStatement()

        return While(expression, body)

    def visit_dowhile(self, node):
        children_count = len(node.children)
        assert children_count == 1 or children_count == 2

        expression = self.transform(node.children[-1])
        if children_count > 1:
            body = self.transform(node.children[0])
        else:
            body = EmptyStatement()

        return DoWhile(expression, body)

    def visit_for(self, node):
        children_count = len(node.children)
        assert children_count > 0 or children_count < 4

        init_statements = []
        condition_statements = []
        expression_statements = []
        body = EmptyStatement()

        for child in node.children:
            if child.symbol == 'for_init':
                init_statements = self.transform(child).list
            elif child.symbol == 'for_condition':
                condition_statements = self.transform(child).list
            elif child.symbol == 'for_expression':
                expression_statements = self.transform(child).list
            elif child.symbol == 'statements_block':
                body = self.transform(child)

        return For(init_statements,
                   condition_statements,
                   expression_statements,
                   body)

    def visit_INTEGER_DECIMAL(self, node):
        return ConstantInt(int(node.token.source))

    def visit_T_CONSTANT_ENCAPSED_STRING(self, node):
        end = len(node.token.source) - 1
        assert end >= 0

        return ConstantString(node.token.source[1:end])

    def visit_TRUE(self, node):
        return ConstantInt(1)

    def visit_FALSE(self, node):
        return ConstantInt(0)

    def visit_IDENTIFIER(self, node):
        return Identifier(node.token.source);

    def visit_T_INLINE_HTML(self, node):
        return Echo([ConstantString(node.token.source)])

    def general_nonterminal_visit(self, node):
        return ItemsList(self.get_children_as_list(node))

    def general_symbol_visit(self, node):
        return Item(node.token.source)

    def get_single_child(self, node):
        assert len(node.children) == 1
        return self.transform(node.children[0])

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


builder = AstBuilder()