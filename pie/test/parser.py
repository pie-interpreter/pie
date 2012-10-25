from sys import argv

__author__ = 'sery0ga'

class Test(object):

    def __init__(self):
        self.result = ''
        self.file = ''
        self.doc = ''

    def __str__(self):
        return "Result: %s\n File: %s\n Doc: %s\n" \
            % (self.result, self.file, self.doc)

class Parser(object):

    (initial, doc, file, result) = range(4)

    def parse(self, filename):
        test = Test()
        mode = self.initial
        for line in open(filename, 'r'):
            line = line.strip('\n')
            current_mode = mode
            if line == "--TEST--":
                mode = self.doc
                continue
            elif line == "--FILE--":
                mode = self.file
                continue
            elif line == "--EXPECTF--":
                mode = self.result
                continue
            if current_mode == self.doc:
                test.doc = "\n".join([test.doc, line])
                continue
            elif current_mode == self.result:
                test.result = "\n".join([test.result, line])
                continue
            elif current_mode == self.file:
                test.file = "\n".join([test.file, line])
                continue

        return test


if __name__ == "__main__":
    if len(argv) < 2:
        print 'No input file provided'
        exit()
    print Parser().parse(argv[1])