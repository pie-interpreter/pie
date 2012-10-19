" Module, providing ast building tools "

from pypy.rlib.parsing.tree import RPythonVisitor
from pypy.tool.pairtype import extendabletype

def build(parseTree):
    " Build as AST from parse tree "
    return builder.dispatch(parseTree);

class AstBuilder(RPythonVisitor):
    ''' Class, than transforms parse tree to AST '''

    def visit_file(self, node):
        statements = []
        for child in node.children:
            node = self.dispatch(child)
            statements.append(node)

        return Source(statements)

    def visit_construct_echo(self, node):
        # first child is T_ECHO token, second is expression, that is echoed
        value = self.dispatch(node.children[1])
        return Echo(value)

    def visit_expression(self, node):
        # expression always has one child and nothing else
        return self.dispatch(node.children[0])

    def visit_arithmetic_expression(self, node):
        # arithmetic expression can have only odd number of children
        # in case of one child, we need to skip this one
        length = len(node.children)
        if length == 1:
            return self.dispatch(node.children[0])

        operation = BinaryOperation(node.children[1].token.source,
                                    self.dispatch(node.children[0]),
                                    self.dispatch(node.children[2]))
        i = 3
        while i < length:
            tmpOperation = BinaryOperation(node.children[i].token.source,
                                           operation,
                                           self.dispatch(node.children[i+1]))
            operation = tmpOperation
            i += 2

        return operation

    def visit_multitive_expression(self, node):
        # multitive expressions are the same as arithmetic ones
        return self.visit_arithmetic_expression(node)

    def visit_T_LNUMBER(self, node):
        return ConstantInt(node.token.source)

    def visit_T_INLINE_HTML(self, node):
        return InlineHtml()


class AstNode:
    __metaclass__ = extendabletype

    def __repr__(self):
        return self.repr()

    def repr(self):
        return "AstNode()"


class Source(AstNode):

    def __init__(self, statements):
        self.statements = statements

    def repr(self):
        representations = []
        for statement in self.statements:
            representations.append(statement.repr())

        childrenRepr = ", ".join(representations)
        return "Source(%s)" % childrenRepr


class Echo(AstNode):

    def __init__(self, value):
        self.value = value

    def repr(self):
        return "Echo(%s)" % self.value.repr()


class BinaryOperation(AstNode):

    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right= right

    def repr(self):
        return "BinaryOperation(%s %s %s)" % (self.left.repr(),
                                              self.operation,
                                              self.right.repr())

class InlineHtml(AstNode):

    def repr(self):
        return "InlineHtml()"


class ConstantInt(AstNode):

    def __init__(self, value):
        self.value = int(value)

    def repr(self):
        return "ConstantInt(%s)" % str(self.value)


builder = AstBuilder()