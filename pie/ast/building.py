" Module, providing ast building tools "

from pie.ast.nodes import *
from pypy.rlib.parsing.tree import RPythonVisitor


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
            parametersList = self.dispatch(node.children[1])
        else:
            parametersList = ParametersList()

        return FunctionCall(name, parametersList.parameters)

    def visit_function_parameters_list(self, node):
        assert len(node.children) > 0

        parameters = []
        for child in node.children:
            parameters.append(self.dispatch(child))

        return ParametersList(parameters)

    def visit_ternary_expression(self, node):
        assert len(node.children) == 3

        condition = self.dispatch(node.children[0])
        left = self.dispatch(node.children[1])
        right = self.dispatch(node.children[2])

        return TernaryOperator(condition, left, right)

    def visit_compare_expression(self, node):
        return self.get_binary_operator(node)

    def visit_additive_expression(self, node):
        return self.get_binary_operator(node)

    def visit_variable_identifier(self, node):
        assert len(node.children) == 1
        return Variable(self.dispatch(node.children[0]))

    def visit_function_declaration(self, node):
        children_count = len(node.children)
        assert children_count == 2 or children_count == 3

        name = self.dispatch(node.children[0])
        if children_count == 3:
            argumentsList = self.dispatch(node.children[1])
        else:
            argumentsList = ArgumentsList()
        body = self.dispatch(node.children[-1])

        return FunctionDeclaration(name,
                                   argumentsList.arguments,
                                   body)

    def visit_function_arguments_list(self, node):
        assert len(node.children) > 0

        arguments = []
        for child in node.children:
            arguments.append(self.dispatch(child))

        return ArgumentsList(arguments)

    def visit_function_body(self, node):
        assert len(node.children) > 0

        statements = []
        for child in node.children:
            node = self.dispatch(child)
            statements.append(node)

        return StatementsList(statements)

    def visit_T_LNUMBER(self, node):
        return ConstantInt(int(node.token.source))

    def visit_T_CONSTANT_ENCAPSED_STRING(self, node):
        return ConstantString(node.token.source[1:-1])

    def visit_IDENTIFIER(self, node):
        return Identifier(node.token.source);

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