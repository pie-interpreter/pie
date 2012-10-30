import getopt
from sys import argv
from pie.test.launcher import *

__author__ = 'sery0ga'

def print_help():
    print """
Runner for PHP coverage tests"

Usage: python run_tests.py [OPTIONS] [TEST_NAMES]
    --help             Display this usage message
    --with-php-source  Include coverage tests from original php

TEST_NAMES should have 'test_' as prefix
"""

if __name__ == "__main__":
    with_php_source = False
    try:
        opts, args = getopt.getopt(argv[1:], "", ["with-php-source", "help"])
    except getopt.GetoptError, e:
        print e
        exit(1)
    for opt, arg in opts:
        if opt == "--with-php-source":
            with_php_source = True
        elif opt == "--help":
            print_help()
            exit(1)
    test_to_run = args
    fill_test_class_with_tests(test_to_run, with_php_source)
    unittest.main(argv=argv[0:1])