from pypy.rlib.parsing.tree import RPythonVisitor, Nonterminal, Node


class AstBuilder(RPythonVisitor):
    ''' Class, than transforms parse tree to AST '''

    def visit_file(self, node):
        root = Code()
        for child in node.children:
            root.children.append(child.visit(self))
            
        return root

    def general_visit(self, node):
        node = AstNode()
        node.children = self.visit_children(node)

        return node
    
    def visit_children(self, node):
        children = []
        if isinstance(node, Nonterminal):
            for child in node.children:
                children.append(self.dispatch(child))

        return children;

class AstNode(Node):

    def __init__(self):
        self.children = []

    def dot(self):
        yield ("%s" % self.__class__.__name__)

class Code(AstNode):
    pass

class OtherSymbol(AstNode):
    pass