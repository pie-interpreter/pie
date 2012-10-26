import unittest
import os
from parser import Parser
from pie.interpreter.context import Context
from pie.interpreter.frame import Frame
from pie.objspace import ObjSpace
from pie.parsing.parsing import interpretFile

__author__ = 'sery0ga'

class TestPHPLanguageCoverage(unittest.TestCase):

    context = Context()
    objspace = ObjSpace()
    frame = Frame()
    parser = Parser()

def _fillTestClassWithTests():
    """ Read directory contains test files and create a test method for each
    test file
    """
    path = os.path.dirname(__file__) + '/coverage/'
    listing = os.listdir(path)
    for infile in listing:
        test_name = 'test_' + infile.split('.')[0]
        def test(self):
            filename = path + infile
            test = self.parser.parse(filename)
            self.context.initialize_function_trace_stack(filename)
            interpretFile(filename, test.file, self.context, self.objspace, self.frame)
        setattr(TestPHPLanguageCoverage, test_name, test)

_fillTestClassWithTests()