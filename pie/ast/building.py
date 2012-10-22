" Module, providing ast building tools "

from pypy.rlib.parsing.tree import RPythonVisitor
from pie.ast.nodes import *


def build(parseTree):
    " Build as AST from parse tree "
    return builder.dispatch(parseTree);


class AstBuilder(RPythonVisitor):
    " Class, than transforms parse tree to AST "

    def visit_file(self, node):
        " Visit root node of the parse tree "
        statements = []
        for child in node.children:
            node = self.dispatch(child)
            statements.append(node)

        return StatementsList(statements)

    def visit_construct_echo(self, node):
        return Echo(self.get_construct_value(node))

    def visit_construct_return(self, node):
        return Return(self.get_construct_value(node))

    def visit_function_call(self, node):
        children_count = len(node.children)
        assert children_count == 1 or children_count == 2

        name = self.dispatch(node.children[0])
        if children_count == 2:
            parameters = self.dispatch(node.children[1])
        else:
            parameters = []

        return FunctionCall(name, parameters)

    def visit_function_parameters_list(self, node):
        assert len(node.children) > 0

        parameters = []
        for child in node.children:
            parameters.append(self.dispatch(child))

        return parameters

    def visit_ternary_expression(self, node):
        assert len(node.children) == 3

        condition = self.dispatch(node.children[0])
        expression1 = self.dispatch(node.children[1])
        expression2 = self.dispatch(node.children[2])

        return TernaryOperator(condition, expression1, expression2)

    def visit_compare_expression(self, node):
        return self.get_binary_operator(node)

    def visit_additive_expression(self, node):
        return self.get_binary_operation(node)

    def visit_function_declaration(self, node):
        children_count = len(node.children)
        assert children_count == 2 or children_count == 3

        name = self.dispatch(node.children[0])
        if children_count == 3:
            arguments = self.dispatch(node.children[1])
        else:
            arguments = []
        body = self.dispatch(node.children[-1])

        return FunctionDeclaration(name, StatementsList(arguments), body)

    def visit_function_body(self, node):
        assert len(node.children) > 1

        statements = []
        for child in node.children:
            node = self.dispatch(child)
            statements.append(node)

        return statements

    def visit_T_IDENTIFIER(self, node):
        return node.toke.source;

    def visit_T_LNUMBER(self, node):
        return ConstantInt(node.token.source)

    def visit_T_CONSTANT_ENCAPSED_STRING(self, node):
        return ConstantString(node.toke.source)

    def get_construct_value(self, node):
        assert len(node.children) == 1
        return self.dispatch(node.children[0])

    def get_binary_operator(self, node):
        children_count = len(node.children)
        assert children_count >= 3 and children_count % 2 == 1

        operator = BinaryOperator(node.children[1].token.source,
                                    self.dispatch(node.children[0]),
                                    self.dispatch(node.children[2]))
        i = 3
        while i < children_count:
            tmpOperator = BinaryOperator(node.children[i].token.source,
                                          operator,
                                          self.dispatch(node.children[i+1]))
            operator = tmpOperator
            i += 2

        return operator


builder = AstBuilder()