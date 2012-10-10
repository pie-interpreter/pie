from parser import *

__author__ = 'sery0ga'

class Visitor(object):

    def visit_main(self, node):
        """
        :param self:
        :param Nonterminal node:
        :return: Code
        """
        statements = []
        statement = node.children[0]
        while True:
            statements.append(self.visit_statement(statement.children[0]))
            if len(statement.children) == 1:
                break
            statement = statement.children[1]
        return Code(statements)

    def visit_statement(self, node):
        """
        :param self:
        :param Nonterminal node:
        :return: Statement or Echo
        """
        lineno = node.getsourcepos().lineno
        firstChild = node.children[0]
        if firstChild.symbol == 'expr':
            return Statement(self.visit_expression(firstChild), lineno)
        elif firstChild.symbol == 'ECHO':
            secondChild = node.children[1]
            return Echo(self.visit_expression(secondChild), lineno)
        raise NotImplementedError

    def visit_expression(self, node):
        """
        Rule ==> expr: or;

        :param self:
        :param Nonterminal:
        """
        firstChild = node.children[0]
        if firstChild.symbol == 'or':
            return self.visit_or(firstChild)
        raise NotImplementedError

    def visit_or(self, node):
        """
        Rule ==> or: assignment | comparison;

        :param self:
        :param Nonterminal:
        """
        firstChild = node.children[0]
        if firstChild.symbol == 'assignment':
            return self.visit_assignment(firstChild)
        elif firstChild.symbol == 'comparison':
            return self.visit_comparison(firstChild)

    def visit_assignment(self, node):
        """
        Rule ==> assignment: "$" atom ASSIGN_OPER expr;
        """
        if len(node.children) != 4:
            raise NotImplementedError
        atom = Variable(self.visit_atom(node.children[1]))
        operator = node.children[2].additional_info
        if operator == '=':
            atom.set_value(self.visit_expression(node.children[3]))

        return atom

    def visit_atom(self, node):
        symbolName = node.children[0].symbol
        value = node.children[0].additional_info
        if symbolName == 'DECIMAL':
            return ConstantInt(int(value))
        if symbolName == 'STR':
            end = len(value) - 1
            assert end >= 0
            return ConstantStr(value[1:end])
        if symbolName == 'FLOAT':
            return ConstantFloat(float(value))
        elif symbolName == 'NAME':
            return ConstantStr(value)
        elif '$' in symbolName:
            if len(node.children) == 2:
                return Variable(self.visit_atom(node.children[1]))
            return Variable(self.visit_expression(node.children[2]))
        raise NotImplementedError


    def visit_comparison(self, node):
        """
        Rule ==> additive COMP_OPER comparison | additive;
        """
        if len(node.children) == 1:
            return self.visit_additive(node.children[0])
        return BinOp(node.children[1].additional_info,
            self.visit_additive(node.children[0]),
            self.visit_comparison(node.children[2]))

    def visit_additive(self, node):
        """
        Rule ==> multitive ADD_OPER additive | multitive
        """
        if len(node.children) == 1:
            return self.visit_multitive(node.children[0])
        return BinOp(node.children[1].additional_info,
            self.visit_multitive(node.children[0]),
            self.visit_additive(node.children[2]))

    def visit_multitive(self, node):
        """
        Rule ==> primary MULT_OPER multitive | primary
        """
        if len(node.children) == 1:
            return self.visit_primary(node.children[0])
        return BinOp(node.children[1].additional_info,
            self.visit_primary(node.children[0]),
            self.visit_multitive(node.children[2]))

    def visit_primary(self, node):
        """
        Rule ==> NAME | atom | ADD_OPER primary
        """
        return self.visit_atom(node.children[0])