from pypy.tool.pairtype import extendabletype

__author__ = 'sery0ga'

class Node(object):
    """
    Represents node in parsing tree
    """
    __metaclass__ = extendabletype

    lineno = 0 # Number of line in file where this node is situated

    def __eq__(self, other):
        return (self.__class__ == other.__class__
                and self.__dict__ == other.__dict__
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return self.repr()

    def repr(self):
        raise NotImplementedError('Abstract node class')

    def compile(self, context):
        raise NotImplementedError('Abstract node class')


class Code(Node):
    """
    Represents a piece of parsed php code

    See 'main' rule in grammar definition file
    """
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return 'Code(' + ','.join([i.repr() for i in self.statements]) +')'


class Statement(Node):
    """ Represents 'statement' rule in grammar definition file """
    def __init__(self, expression, line_number=0):
        self.expression = expression
        self.lineno = line_number

    def repr(self):
        return 'Statement(%s)' % self.expression.repr()

class Echo(Node):
    """ Represents 'ECHO' symbol in grammar definition file
    """
    def __init__(self, expression, lineno=0):
        self.expression = expression
        self.lineno = lineno

    def repr(self):
        return 'Echo(%s)' % self.expression.repr()

class Variable(Node):
    """ Represents '"$" atom' rule in grammar definition file
    """
    def __init__(self, name):
        self.name = name
        self.value = None

    def repr(self):
        return 'Variable (%s)' % self.name.repr()

    def set_value(self, value):
        self.value = value

class Const(Node):
    def is_constant(self):
        return True

class ConstantInt(Const):
    def __init__(self, value):
        self.value = value

    def repr(self):
        return str(self.value)

class ConstantStr(Const):
    def __init__(self, value):
        self.value = value

    def repr(self):
        return '"' + self.value + '"'

class ConstantFloat(Const):
    def __init__(self, value):
        self.value = value

    def repr(self):
        return str(self.value)

class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def repr(self):
        return "%s %s %s" % (self.left.repr(), self.op, self.right.repr())
