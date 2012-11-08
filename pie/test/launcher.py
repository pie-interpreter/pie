from pie.compiling import compiling
from pie.error import PHPError, InterpreterError, LexerError
from pie.interpreter import interpreter
from pie.interpreter.main import InterpretedSource
from pie.test.parser import Parser
from pypy.rlib.parsing.parsing import ParseError
import os
import sys
import tempfile
import unittest

__author__ = 'sery0ga'


class TestPHPLanguageCoverage(unittest.TestCase):

    parser = Parser()
    output_file = tempfile.TemporaryFile()
    stdout_no = os.dup(sys.stdout.fileno())

    def setUp(self):
        self.current_position = self.output_file.tell()
        self.context.function_trace_stack = []

    def redirect_output(self):
        os.dup2(self.output_file.fileno(), sys.stdout.fileno())

    def restore_output(self):
        os.dup2(self.stdout_no, sys.stdout.fileno())


def fill_test_class_with_tests(test_to_run = [], with_php_source = False):
    """
    Read all test files create a test method for each
    """

    _fill_test_class_with_tests_from_dir('/coverage/', test_to_run, 'coverage_')
    _fill_test_class_with_tests_from_dir('/parsing/', test_to_run, 'parsing_')
    if with_php_source:
        _fill_test_class_with_tests_from_dir('/from_php_source/', test_to_run)


def _fill_test_class_with_tests_from_dir(directory, test_to_run, prefix = ''):
    """
    Read directory that contains test files and create
    a test method for each test file
    """

    path = os.path.dirname(__file__) + directory
    listing = os.listdir(path)
    for entry in listing:
        # here we suppose that all files except directories contain '.'
        #  in their name
        entry_structure = entry.split('.')
        if len(entry_structure) == 1:
            if not os.path.isdir(path + entry):
                continue

            sub_dir = directory + entry + '/'
            _fill_test_class_with_tests_from_dir(sub_dir,
                                                 test_to_run,
                                                 prefix + entry + '_')
            continue
        filename = entry_structure[0]
        test_name = 'test_' + prefix + filename
        if test_to_run and test_name not in test_to_run:
            continue
        full_filename = path + entry
        _add_test(full_filename, test_name)


def _add_test(filename, test_name):

    def test(self):
        test = self.parser.parse(filename)

        if test.skip:
            if test.skip_reason:
                self.skipTest(test.skip_reason)
            else:
                self.skipTest("Mark as skipped")
            return

        source = InterpretedSource(test.data, filename)
        self.redirect_output()

        try:
            if test.compile_only:
                compiling.compile_source(source)
            else:
                interpreter.interpret(source)
            self.restore_output()
        except PHPError as e:
            self.restore_output()
            self.fail("PHPError\n\n" + e.print_message())
        except InterpreterError as e:
            self.restore_output()
            self.fail("InterpreterError\n\n" + e.__str__())
        except LexerError as e:
            self.restore_output()
            self.fail("LexerError\n\n" + e.nice_error_message(source.filename))
        except ParseError as e:
            self.restore_output()
            self.fail("ParseError\n\n" + e.nice_error_message(source.filename,
                                                              source.data))

        if test.has_result:
            # rewind file pointer and read content
            self.output_file.seek(self.current_position)

            actual_result = self.output_file.read()
            if test.is_true:
                self.assertEqual(actual_result, test.result)
            else:
                self.assertNotEqual(actual_result, test.result)

    test.__name__ = test_name
    setattr(TestPHPLanguageCoverage, test_name, test)
