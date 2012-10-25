import unittest
import os
from parser import Parser

__author__ = 'sery0ga'

class TestPHPLanguageCoverage(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

def _fillTestClassWithTests():
    """ Read directory contains test files and create a test method for each
    test file
    """
    path = os.path.dirname(__file__) + '/coverage/'
    listing = os.listdir(path)
    for infile in listing:
        test_name = 'test_' + infile.split('.')[0]
        def test(self):
            test = self.parser.parse(path + infile)
            assert False
        setattr(TestPHPLanguageCoverage, test_name, test)

_fillTestClassWithTests()

if __name__ == "__main__":
    unittest.main()
