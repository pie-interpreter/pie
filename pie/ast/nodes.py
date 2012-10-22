" Module, with all ast nodes "


from pypy.tool.pairtype import extendabletype


class AstNode:
    " Base class for all nodes in ast "
    __metaclass__ = extendabletype

    def repr(self):
        " Pure AstNode objects should not exist "
        raise NotImplementedError

    def __repr__(self):
        return self.repr()

class StackDepthIncreaser(AstNode):
    """
    All nodes, subclassed from this one, when compiled and executed leave one
    new value on the stack
    """


class StatementsList(AstNode):
    " Node, containing list of statement, always root node of the ast "

    def __init__(self, statements):
        self.statements = statements

    def repr(self):
        representations = []
        for statement in self.statements:
            representations.append(statement.repr())

        childrenRepr = ", ".join(representations)
        return "StatementsList(%s)" % childrenRepr


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


class ConstantInt(AstNode):

    def __init__(self, value):
        self.value = value

    def repr(self):
        return "ConstantInt(%s)" % self.value

