from parser import Parser
from pie.error import PHPError, InterpreterError
from pie.interpreter.context import Context
from pie.interpreter.frame import Frame
from pie.parsing.parsing import interpret_file, InterpretedFile
from pprint import pprint
from pypy.rlib.parsing.deterministic import LexerError
from pypy.rlib.parsing.parsing import ParseError
import os
import sys
import tempfile
import unittest

__author__ = 'sery0ga'


class TestPHPLanguageCoverage(unittest.TestCase):

    context = Context()
    frame = Frame()
    parser = Parser()
    output_file = tempfile.TemporaryFile()

    def setUp(self):
        self.current_position = self.output_file.tell()


def fill_test_class_with_tests(test_to_run = [], with_php_source = False):
    """ Read directory contains test files and create a test method for each
    test file
    """
    _fill_test_class_with_tests_from_dir('/coverage/', test_to_run, 'coverage_')
    _fill_test_class_with_tests_from_dir('/grammar/', test_to_run, 'grammar_')
    if with_php_source:
        _fill_test_class_with_tests_from_dir('/from_php_source/', test_to_run)


def _fill_test_class_with_tests_from_dir(directory, test_to_run, prefix = ''):
    """ Read directory contains test files and create a test method for each
    test file
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

        # initialization
        self.context.initialize_function_trace_stack(filename)
        interpreted_file = InterpretedFile(filename, test.data)

        # create temporary interpreted_file and redirect output to it
        old_fileno = os.dup(sys.stdout.fileno())
        os.dup2(self.output_file.fileno(), 1)

#        try:
        interpret_file(interpreted_file, self.context, self.frame)
        os.dup2(old_fileno, 1)
#        except PHPError as e:
#            os.dup2(old_fileno, 1)
#            print e.print_message()
#        except InterpreterError as e:
#            os.dup2(old_fileno, 1)
#            print e
#        except LexerError as e:
#            print e.nice_error_message(file.filename)
#            sys.exit(1)
#        except ParseError as e:
#            os.dup2(sys.stdout.fileno(), 1)
#            pprint(e.nice_error_message(interpreted_file.filename,
#                                        interpreted_file.data))

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
