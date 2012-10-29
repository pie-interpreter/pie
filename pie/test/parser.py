from sys import argv

__author__ = 'sery0ga'

class Test(object):

    def __init__(self):
        self.result = ''
        self.data = ''
        self.doc = ''
        self.is_true = True

    def __str__(self):
        return "Result: %s\n File: %s\n Doc: %s\n" \
            % (self.result, self.data, self.doc)

class Parser(object):

    (initial, doc, file, result, skip) = range(5)

    def parse(self, filename):
        test = Test()
        mode = self.initial
        file = open(filename, 'r')
        for line in file:
            line = line.strip('\n')
            current_mode = mode
            if line == "--TEST--":
                mode = self.doc
                continue
            elif line == "--FILE--":
                mode = self.file
                continue
            elif line == "--SKIPIF--":
                mode = self.skip
                continue
            elif line == "--EXPECTF--" or line == "--EXPECT--":
                mode = self.result
                if line == "--EXPECTF--":
                    test.is_true = False
                continue
            if current_mode == self.doc:
                if not test.doc:
                    test.doc = line
                else:
                    test.doc = "\n".join([test.doc, line])
                continue
            elif current_mode == self.result:
                if not test.result:
                    test.result = line
                else:
                    test.result = "\n".join([test.result, line])
                continue
            elif current_mode == self.file:
                if not test.data:
                    test.data = line
                else:
                    test.data = "\n".join([test.data, line])
                continue
            elif current_mode == self.skip:
                continue
        file.close()
        return test


if __name__ == "__main__":
    if len(argv) < 2:
        print 'No input file provided'
        exit()
    print Parser().parse(argv[1])