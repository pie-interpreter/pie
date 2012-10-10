
from pie.parsing import parse
from pypy.rlib.parsing.parsing import ParseError
from pypy.rlib.streamio import open_file_as_stream
import sys

def run(argv):
    if len(argv) < 2:
        print 'No input file provided'
        return 1

    input_file = open_file_as_stream(argv[1])
    data = input_file.readall()
    input_file.close()

    try:
        result = parse(data)
        result.view()
    except ParseError as e:
        print e.nice_error_message(argv[1], data)
        return 1

    return 0

if __name__ == '__main__':
    run(sys.argv)