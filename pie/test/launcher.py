import os
import sys
import tempfile
import unittest

from pie.interpreter.frame import Frame
from pie.interpreter.sourcecode import SourceCode
from pie.interpreter.context import Context
from pie.test.parser import Parser
from pie.interpreter.errors.base import PieError

__author__ = 'sery0ga'


class TestPHPLanguageCoverage(unittest.TestCase):

    parser = Parser()
    output_file = tempfile.TemporaryFile()
    stdout_no = os.dup(sys.stdout.fileno())
    stderr_no = os.dup(sys.stderr.fileno())

    def setUp(self):
        self.current_position = self.output_file.tell()

    def redirect_output(self):
        os.dup2(self.output_file.fileno(), sys.stdout.fileno())
        os.dup2(self.output_file.fileno(), sys.stderr.fileno())

    def restore_output(self):
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(self.stdout_no, sys.stdout.fileno())
        os.dup2(self.stderr_no, sys.stderr.fileno())

    def _check_test_result(self, test, actual_result):
        if test.check_parts_of_result:
            self.assertEqual(len(actual_result), len(test.result))
            list_equals = True
            part_not_found = ''
            for (actual, expected) in zip(actual_result, test.result):
                expected_parts = expected.split('%')
                equal = True
                for part in expected_parts:
                    if part not in actual:
                        part_not_found = "Part >>%s<< not found in %s" \
                            % (part, actual)
                        equal = False
                        break
                if not equal:
                    list_equals = False
                    break
            self.assertTrue(list_equals, part_not_found)
        elif test.is_true:
            self.assertListEqual(actual_result, test.result)
        else:
            self.assertListNotEqual(actual_result, test.result)


def fill_test_class_with_tests(test_to_run=[], with_php_source=False):
    """
    Read all test files create a test method for each
    """

    _fill_test_class_with_tests_from_dir('/coverage/', test_to_run)
    if with_php_source:
        _fill_test_class_with_tests_from_dir('/from_php_source/', test_to_run)


def _fill_test_class_with_tests_from_dir(directory, test_to_run, prefix=''):
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
        # skip files with extension which is different to 'phpt'
        if entry_structure[1] != 'phpt':
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

        source = SourceCode(filename)
        source.content = test.source
        self.redirect_output()

        try:
            if not test.compile_only:
                context = Context(filename)
                source.interpret(context, Frame())
        except PieError as e:
            os.write(2, e.get_message())
        except Exception as e:
            self.restore_output()
            self.fail(e)

        self.restore_output()

        if test.has_result and not test.compile_only:
            # rewind file pointer and read content
            self.output_file.seek(self.current_position)

            actual_result = str.splitlines(self.output_file.read())
            self._check_test_result(test, actual_result)

    test.__name__ = test_name
    setattr(TestPHPLanguageCoverage, test_name, test)
