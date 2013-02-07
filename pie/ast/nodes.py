""" Module, with all ast nodes """

from rpython.tool.pairtype import extendabletype


class AstNode:
    """ Base class for all nodes in ast """
    __metaclass__ = extendabletype

    line = 0

    def __repr__(self):
        return "%s:%s" % (self.repr(), self.line)

    def repr(self):
        """ Pure AstNode objects should not exist """
        raise NotImplementedError

    def get_list_repr(self, items_list):
        representations = []
        for item in items_list:
            if isinstance(item, str):
                representations.append(item)
            else:
                representations.append(item.__repr__())

        return ", ".join(representations)


class AstNodeWithResult(AstNode):
    """
    All nodes, subclassed from this one, when compiled and executed leave one
    new value on the stack
    """


class Item(AstNode):
    """
    Helper node for making ast-building rpythnoic, not really used in ast and
    not compiled. Used as return value of visiting single nodes.

    Value of the item should always be string.

    Nodes, subclassed from this one can be in ast.
    """

    def __init__(self, value):
        self.value = value

    def repr(self):
        return "Item: %s" % self.value


class ItemsList(AstNode):
    """
    Helper node for all constructs, that represent lists of something. Used
    to make ast-building rpythnoic, not really used in ast and not compiled.

    Nodes, subclassed from this one can be in ast.
    """

    def __init__(self, items_list=[]):
        self.list = items_list

    def repr(self):
        return "ItemsList(%s)" % self.get_list_repr(self.list)


class EmptyStatement(AstNode):
    """
    Helper node to represent empty result of visiting parse tree.
    Used to make ast-building rpythnoic.
    """

    def repr(self):
        return "EmptyStatement()"


class StatementsList(ItemsList):
    " Node, containing list of statement, always root node of the ast "

    def repr(self):
        return "StatementsList(%s)" % self.get_list_repr(self.list)


class Print(AstNodeWithResult):

    def __init__(self, value):
        self.value = value

    def repr(self):
        return "Print(%s)" % self.value.repr()


class Echo(ItemsList):

    def repr(self):
        return "Echo(%s)" % self.get_list_repr(self.list)


class Include(AstNodeWithResult):

    def __init__(self, value):
        self.value = value

    def repr(self):
        return "Include(%s)" % self.value.repr()


class IncludeOnce(Include):

    def repr(self):
        return "IncludeOnce(%s)" % self.value.repr()


class Require(Include):

    def repr(self):
        return "Require(%s)" % self.value.repr()


class RequireOnce(Include):

    def repr(self):
        return "RequireOnce(%s)" % self.value.repr()


class Return(AstNode):

    def __init__(self, expression):
        self.expression = expression

    def repr(self):
        return "Return(%s)" % self.expression.repr()


class Break(AstNode):

    def __init__(self, level):
        self.level = level

    def repr(self):
        return "Break(%s)" % self.level


class Continue(AstNode):

    def __init__(self, level):
        self.level = level

    def repr(self):
        return "Continue(%s)" % self.level


class Isset(AstNodeWithResult):

    def __init__(self, items_list=[]):
        self.list = items_list

    def repr(self):
        return "Isset(%s)" % self.get_list_repr(self.list)


class Unset(ItemsList):

    def repr(self):
        return "Unset(%s)" % self.get_list_repr(self.list)


class Empty(AstNodeWithResult):

        def __init__(self, expression):
            self.expression = expression

        def repr(self):
            return "Empty(%s)" % self.expression.repr()


class BinaryOperator(AstNodeWithResult):

    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def repr(self):
        return "BinaryOperator(%s %s %s)" % (self.left.repr(),
                                              self.operation,
                                              self.right.repr())


class Xor(AstNodeWithResult):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def repr(self):
        return "Xor(%s xor %s)" % (self.left.repr(), self.right.repr())


class Or(Xor):

    def repr(self):
        return "Or(%s or %s)" % (self.left.repr(), self.right.repr())


class And(Xor):

    def repr(self):
        return "And(%s or %s)" % (self.left.repr(), self.right.repr())


class Assignment(AstNodeWithResult):

    def __init__(self, variable, operator, value):
        self.variable = variable
        self.operator = operator
        self.value = value

    def repr(self):
        return "Assignment(%s %s %s)" % (self.variable.repr(),
                                         self.operator,
                                         self.value.repr())


class ReferenceAssignment(AstNodeWithResult):

    def __init__(self, target, source):
        self.target = target
        self.source = source

    def repr(self):
        return "ReferenceAssignment(%s =& %s)" & (self.target, self.source)


class TernaryOperator(AstNodeWithResult):

    def __init__(self, condition, left, right):
        self.condition = condition
        self.left = left
        self.right = right

    def repr(self):
        return "TernaryOperator(%s ? %s : %s)" % (self.condition.repr(),
                                                  self.left.repr(),
                                                  self.right.repr())


class Not(AstNodeWithResult):

    def __init__(self, value):
        self.value = value

    def repr(self):
        return "Not(%s)" % self.value


class IncrementDecrement(AstNodeWithResult):

    PRE = 'pre'
    POST = 'post'

    def __init__(self, operation_type, operator, variable):
        self.type = operation_type
        self.operator = operator
        self.variable = variable

    def repr(self):
        if self.type == self.POST:
            values = (self.variable.repr(), self.operator)
        else:
            values = (self.operator, self.variable.repr())
        return "IncrementDecrement(%s%s)" % values


class Cast(AstNodeWithResult):

    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

    def repr(self):
        return "Cast((%s) %s)" % (self.symbol, self.value.repr())


class Variable(AstNodeWithResult):

    def __init__(self, name):
        self.name = name

    def repr(self):
        return "Variable(%s)" % self.name.repr()


class FunctionCall(AstNodeWithResult):

    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

    def repr(self):
        return "FunctionCall(%s(%s))" % (self.name.repr(),
                                         self.get_list_repr(self.parameters))


class FunctionDeclaration(AstNode):

    def __init__(self, name, is_returning_reference, arguments, body):
        self.name = name
        self.is_returning_reference = is_returning_reference
        self.arguments = arguments
        self.body = body
        self.top_level = False

    def repr(self):
        if self.is_returning_reference:
            reference_symbol = '&'
        else:
            reference_symbol = ''

        return "FunctionDeclaration%s(%s(%s){%s})" \
            % (reference_symbol,
                self.name,
                self.get_list_repr(self.arguments),
                self.body.repr())


class Argument(AstNode):
    """
    Helper class for making code more rpythonic,
    defines interface for argument nodes
    """


class ArgumentWithDefaultValue(Argument):
    """
    Helper class for making code more rpythonic,
    defines interface for argument nodes
    """


class ArgumentVariable(Argument):

    def __init__(self, variable):
        self.variable = variable

    def repr(self):
        return "ArgumentVariable(%s)" % self.variable


class ArgumentReference(Argument):

    def __init__(self, variable):
        self.variable = variable

    def repr(self):
        return "ArgumentReference(%s)" % self.variable


class ArgumentVariableWithDefaultValue(ArgumentWithDefaultValue):

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def repr(self):
        return "ArgumentVariableWithDefaultValue(%s, %s)" \
            % (self.variable, self.value)


class ArgumentReferenceWithDefaultValue(ArgumentWithDefaultValue):

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def repr(self):
        return "ArgumentReferenceWithDefaultValue(%s, %s)" \
            % (self.variable, self.value)


class If(AstNode):

    def __init__(self, condition, body, else_branch):
        self.condition = condition
        self.body = body
        self.else_branch = else_branch

    def repr(self):
        return("If(%s) {%s} else {%s}") % (self.condition,
                                           self.body,
                                           self.else_branch)


class While(AstNode):

    def __init__(self, expression, body):
        self.expression = expression
        self.body = body

    def repr(self):
        return "While(%s {%s})" % (self.expression.repr(), self.body.repr())


class DoWhile(AstNode):

    def __init__(self, expression, body):
        self.expression = expression
        self.body = body

    def repr(self):
        return "DoWhile({%s} %s)" % (self.body.repr(), self.expression.repr())


class For(AstNode):

    def __init__(self, init_statements,
                 condition_statements, expression_statements, body):
        self.init_statements = init_statements
        self.condition_statements = condition_statements
        self.expression_statements = expression_statements
        self.body = body

    def repr(self):
        return "For(%s;%s;%s {%s})" \
            % (self.get_list_repr(self.init_statements),
               self.get_list_repr(self.condition_statements),
               self.get_list_repr(self.expression_statements),
               self.body.repr())


class Switch(AstNode):

    def __init__(self, expression, cases_list):
        self.expression = expression
        self.cases_list = cases_list

    def repr(self):
        return "Switch((%s) %s)" % (self.expression.repr(),
                                    self.get_list_repr(self.cases_list))


class SwitchCase(AstNode):

    def __init__(self, expression, body):
        self.expression = expression
        self.body = body

    def repr(self):
        return "SwitchCase(%s: %s)" % (self.expression.repr(), self.body.repr())


class SwitchDefault(AstNode):

    def __init__(self, body):
        self.body = body

    def repr(self):
        return "SwitchDefault(%s)" % (self.body.repr())


class Constant(AstNodeWithResult):
    """
    Helper class for making code more rpythonic,
    defines interface for constants compiling
    """


class ConstantInt(Constant):

    def __init__(self, value):
        self.value = value
        self.sign = '+'


class ConstantIntBin(ConstantInt):

    def repr(self):
        return "ConstantIntBin(%s%s)" % (self.sign, self.value)


class ConstantIntOct(ConstantInt):

    def repr(self):
        return "ConstantIntOct(%s%s)" % (self.sign, self.value)


class ConstantIntDec(ConstantInt):

    def repr(self):
        return "ConstantIntDec(%s%s)" % (self.sign, self.value)


class ConstantIntHex(ConstantInt):

    def repr(self):
        return "ConstantIntHex(%s%s)" % (self.sign, self.value)


class ConstantFloat(Constant):

    def __init__(self, value):
        self.value = value
        self.sign = '+'

    def repr(self):
        return "ConstantFloat(%s%s)" % (self.sign, self.value)


class ConstantString(Constant):

    def __init__(self, value):
        self.value = value

    def repr(self):
        return "ConstantString(\"%s\")" % (self.value)


class ConstantSingleQuotedString(ConstantString):
    " String, that needs to be pre-processed "

    def repr(self):
        return "ConstantSingleQuotedString('%s')" % (self.value)


class ConstantDoubleQuotedString(ConstantString):
    " String, that needs to be pre-processed with more things "

    def repr(self):
        return "ConstantDoubleQuotedString(\"%s\")" % (self.value)


class ConstantBool(Constant):

    def __init__(self, value):
        self.value = value

    def repr(self):
        return "ConstantBool(\"%s\")" % (self.value)


class ConstantNull(Constant):

    def repr(self):
        return "ConstantNull()"


class Identifier(Item):

    def repr(self):
        return "Identifier: %s" % self.value
