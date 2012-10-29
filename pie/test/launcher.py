import unittest
import os
import sys
import tempfile
from parser import Parser
from pie.interpreter.context import Context
from pie.interpreter.frame import Frame
from pie.objspace import ObjSpace
from pie.parsing.parsing import interpret_file, InterpretedFile

__author__ = 'sery0ga'

class TestPHPLanguageCoverage(unittest.TestCase):

    context = Context()
    objspace = ObjSpace()
    frame = Frame()
    parser = Parser()
    output_file = tempfile.TemporaryFile()

    def setUp(self):
        self.current_position = self.output_file.tell()

def fill_test_class_with_tests(test_to_run = [], with_php_source = False):
    """ Read directory contains test files and create a test method for each
    test file
    """
    _fill_test_class_with_tests_from_directory('/coverage/', test_to_run)
    if with_php_source:
        _fill_test_class_with_tests_from_directory('/from_php_source/', test_to_run)

def _fill_test_class_with_tests_from_directory(directory, test_to_run):
    """ Read directory contains test files and create a test method for each
    test file
    """
    path = os.path.dirname(__file__) + directory
    listing = os.listdir(path)
    for infile in listing:
        filename = infile.split('.')[0]
        test_name = 'test_' + filename
        if test_to_run and test_name not in test_to_run:
            continue
        full_filename = path + infile
        _add_test(full_filename, test_name)

def _add_test(filename, test_name):
    def test(self):
        test = self.parser.parse(filename)
        # initialization
        self.context.initialize_function_trace_stack(filename)
        file = InterpretedFile(filename, test.data)

        # create temporary file and redirect output to it
        old_fileno = os.dup(sys.stdout.fileno())
        os.dup2(self.output_file.fileno(), 1)
        interpret_file(file, self.context, self.objspace, self.frame)
        os.dup2(old_fileno, 1)
        # rewind file pointer and read content
        self.output_file.seek(self.current_position)

        actual_result = self.output_file.read()
        if test.is_true:
            self.assertEqual(actual_result, test.result)
        else:
            self.assertNotEqual(actual_result, test.result)
    test.__name__ = test_name
    setattr(TestPHPLanguageCoverage, test_name, test)
