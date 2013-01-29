import unittest
from pie.launcher.config import config
from pie.utils.ini import raw_parse_ini_file
from pypy.rlib.parsing.parsing import ParseError


class TestParseIniFile(unittest.TestCase):
    def setUp(self):
        # We need this to block annoying PHP behaviour
        # of printing warnings if there's some ini file parsing errors.
        config.display_errors = False

    def test_parse_non_existed_file(self):
        filename = "non_existed.ini"
        self.assertRaises(IOError, raw_parse_ini_file, filename)

    def test_parse_file_with_wrong_section(self):
        filename = "pie/launcher/test/wrong_section.ini"
        self.assertRaisesRegexp(ParseError, "Section should have a closing bracket",
            raw_parse_ini_file, filename)

    def test_parse_file_with_no_value(self):
        filename = "pie/launcher/test/no_value.ini"
        self.assertRaisesRegexp(ParseError, "Each option should have name and value",
            raw_parse_ini_file, filename)

    def test_parse_file_with_wrong_string(self):
        filename = "pie/launcher/test/wrong_string.ini"
        self.assertRaisesRegexp(ParseError, "String should have a closing bracket",
            raw_parse_ini_file, filename)

    def test_parse_normal_file(self):
        filename = "pie/launcher/test/normal.ini"
        result = raw_parse_ini_file(filename)
        self.assertEqual(result['PHP']['display_errors'], 'on')
        self.assertEqual(result['PHP']['string_value'], 'OK. It works')
        self.assertEqual(result['PHP']['int_value'], '55')
        self.assertEqual(result['next_section']['any_value'], '57')
        self.assertEqual(result['next_section']['string_value'], 'No, it doesn\'t work')

