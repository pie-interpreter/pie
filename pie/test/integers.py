import unittest
from pypy.rlib.streamio import open_file_as_stream

__author__ = 'sery0ga'

class TestIntegers(unittest.TestCase):

    FOLDER_NAME = 'integers'

    def _read_test_file(self, name):
        filename = ''.join(['data/', self.FOLDER_NAME, '/', name, '.php'])
        input_file = open_file_as_stream(filename)
        data = input_file.readall()
        input_file.close()
        return data

if __name__ == "__main__":
    unittest.main()