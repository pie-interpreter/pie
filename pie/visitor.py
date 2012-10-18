from astnodes import *

__author__ = 'sery0ga'

class Visitor(object):

    def visit_main(self, node):
        """
        :param self:
        :param Nonterminal node:
        :return: Code
        """
        blocks = []
        contents = node.children[0]
        if len(contents.children) == 1: # in case onf EOF
            return File(blocks)
        while True:
            block = contents.children[0]
            if block.symbol == 'content_block':
                blocks.append(self.visit_block(block))
            elif block.symbol == 'EOF':
                break
            else:
                raise NotImplementedError
            contents = contents.children[1]
        return File(blocks)

    def visit_block(self, node):
        """
        :param self:
        :param Nonterminal node:
        :return: Statement or Echo
        """
        lineno = node.getsourcepos().lineno
        child = node.children[0]
        if child.symbol == 'code':
            statements = []
            # skip T_OPEN_TAG and go directly to statements
            statementsNode = child.children[1]
            statementsNumber = len(statementsNode.children)
            if statementsNumber != 3:
                raise NotImplementedError
            # check which type of statements structure we have
            lastPartSymbol = statementsNode.children[2].symbol
            if lastPartSymbol == 'T_CLOSE_TAG':
                return Statement(self.visit_statement(statementsNode.children[0]), lineno)
            else:
                raise NotImplementedError
        elif child.symbol == 'T_INLINE_HTML':
            return InlineHtml()
        raise NotImplementedError

    def visit_statement(self, node):
        """
        :param self:
        :param Nonterminal node:
        :return: Statement or Echo
        """
        lineno = node.getsourcepos().lineno
        child = node.children[0]
        if child.symbol == 'construct':
            construct = child.children[0]
            if construct.symbol == 'construct_echo':
                # skip T_ECHO and go directly to expression
                return Echo(self.visit_expression(construct.children[1]), lineno)
            else:
                raise NotImplementedError
        elif child.symbol == 'assignment':
            raise NotImplementedError
        raise NotImplementedError

    def visit_expression(self, node):
        """
        Rule ==> expr: or;

        :param self:
        :param Nonterminal:
        """
        child = node.children[0]
        if child.symbol == 'arithmetic_expression':
            return self.visit_additive(child)
        raise NotImplementedError

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
        return self.visit_atom(node)

    def visit_atom(self, node):
        childrenNumber = len(node.children)
        if childrenNumber == 1:
            child = node.children[0]
            if child.symbol == 'T_LNUMBER':
                return ConstantInt(int(child.additional_info))
            raise NotImplementedError
        raise NotImplementedError
