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
        for block in node.children:
            blocks.append(self.visit_block(block))
        return File(blocks)

    def visit_block(self, node):
        """
        :param self:
        :param Nonterminal node:
        :return: Statement or Echo
        """
        lineno = node.getsourcepos().lineno
        if node.symbol == 'construct_echo':
            return Echo(self.visit_expression(node.children[1]), lineno)
        elif node.symbol == 'assignment':
            raise NotImplementedError
        elif node.symbol == 'T_INLINE_HTML':
            return InlineHtml()
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
        if len(node.children) == 1:
            return self.visit_multitive(node.children[0])
        return BinOp(node.children[1].additional_info,
            self.visit_multitive(node.children[0]),
            self.visit_additive(node.children[2]))

    def visit_multitive(self, node):
        if node.symbol == 'T_LNUMBER':
            return self.visit_atom(node)
        if len(node.children) == 1:
            return self.visit_primary(node.children[0])
        return BinOp(node.children[1].additional_info,
            self.visit_primary(node.children[0]),
            self.visit_multitive(node.children[2]))

    def visit_primary(self, node):
        return self.visit_atom(node)

    def visit_atom(self, node):
        if node.symbol == 'T_LNUMBER':
            return ConstantInt(int(node.additional_info))
        raise NotImplementedError
