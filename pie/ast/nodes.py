""" Module, with all ast nodes """

from pypy.tool.pairtype import extendabletype


class AstNode:
    """ Base class for all nodes in ast """
    __metaclass__ = extendabletype

    line_number = 0

    def repr(self):
        """ Pure AstNode objects should not exist """
        raise NotImplementedError

    def __repr__(self):
        return self.repr()

    def get_line(self):
        return self.line_number

class AstNodeWithResult(AstNode):
    """
    All nodes, subclassed from this one, when compiled and executed leave one
    new value on the stack
    """


class Constant(AstNodeWithResult):
    """
    Node for constants, they all share compilation process
    """


class Identifier(AstNode):

    def __init__(self, value, line_number = 0):
        self.value = value
        self.line_number = line_number

    def repr(self):
        return "Identifier: %s" % self.value


class ParametersList(AstNode):

    def __init__(self, parameters = [], line_number = 0):
        self.parameters = parameters
        self.line_number = line_number

    def repr(self):
        return "ParametersList()"


class ArgumentsList(AstNode):

    def __init__(self, arguments = [], line_number = 0):
        self.arguments = arguments
        self.line_number = line_number

    def repr(self):
        return "ArgumentsList()"


class StatementsList(AstNode):
    " Node, containing list of statement, always root node of the ast "

    def __init__(self, statements = [], line_number = 0):
        self.statements = statements
        self.line_number = line_number

    def repr(self):
        representations = []
        for statement in self.statements:
            representations.append(statement.repr())

        childrenRepr = ", ".join(representations)
        return "StatementsList(%s)" % childrenRepr


class Echo(AstNode):

    def __init__(self, expression, line_number = 0):
        self.expression = expression
        self.line_number = line_number

    def repr(self):
        return "Echo(%s)" % self.expression.repr()


class Return(AstNode):

    def __init__(self, expression, line_number = 0):
        self.expression = expression
        self.line_number = line_number

    def repr(self):
        return "Return(%s)" % self.expression.repr()


class FunctionCall(AstNodeWithResult):

    def __init__(self, name, parameters, line_number = 0):
        self.name = name
        self.parameters = parameters
        self.line_number = line_number

    def repr(self):
        representations = []
        for parameter in self.parameters:
            representations.append(parameter.repr())

        parametersRepr = ", ".join(representations)
        return "FunctionCall(%s(%s))" % (self.name.repr(), parametersRepr)


class Assignment(AstNodeWithResult):

    def __init__(self, variable, value, line_number = 0):
        self.variable = variable
        self.value = value
        self.line_number = line_number

    def repr(self):
        return "Assignment(%s = %s)" % (self.variable.repr(),
                                        self.value.repr())


class TernaryOperator(AstNodeWithResult):

    def __init__(self, condition, left, right, line_number = 0):
        self.condition = condition
        self.left = left
        self.right = right
        self.line_number = line_number

    def repr(self):
        return "TernaryOperator(%s ? %s : %s)" % (self.condition.repr(),
                                                  self.left.repr(),
                                                  self.right.repr())


class BinaryOperator(AstNodeWithResult):

    def __init__(self, operation, left, right, line_number = 0):
        self.operation = operation
        self.left = left
        self.right = right
        self.line_number = line_number

    def repr(self):
        return "BinaryOperator(%s %s %s)" % (self.left.repr(),
                                              self.operation,
                                              self.right.repr())


class Variable(AstNodeWithResult):

    def __init__(self, name, line_number = 0):
        self.name = name
        self.line_number = line_number

    def repr(self):
        return "Variable(%s)" % self.name.repr()


class ConstantInt(Constant):

    def __init__(self, value, line_number = 0):
        self.value = value
        self.line_number = line_number

    def repr(self):
        return "ConstantInt(%s)" % self.value


class ConstantString(Constant):

    def __init__(self, value, line_number = 0):
        self.value = value
        self.line_number = line_number

    def repr(self):
        return "ConstantString(%s)" % self.value


class FunctionDeclaration(AstNode):

    def __init__(self, name, arguments, body, line_number = 0):
        self.name = name
        self.arguments = arguments
        self.body = body
        self.line_number = line_number

    def repr(self):
        representations = []
        for statement in self.arguments:
            representations.append(statement.repr())

        argumentsRepr = ", ".join(representations)
        return "FunctionDeclaration(%s(%s){%s})" % (self.name,
                                                    argumentsRepr,
                                                    self.body.repr())


class While(AstNode):

    def __init__(self, expression, body, line_number = 0):
        self.expression = expression
        self.body = body
        self.line_number = line_number

    def repr(self):
        return "While(%s {%s})" % (self.expression.repr(), self.body.repr())

