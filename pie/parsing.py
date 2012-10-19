from pie.visitor import Visitor
from parser import parse, transformer

def buildAst(data):
    """ Parse php code """
    parseTree = parse(data)
    parseTree = transformer.transform(parseTree)
    astBuilder = Visitor()

    return astBuilder.visit_main(parseTree)
