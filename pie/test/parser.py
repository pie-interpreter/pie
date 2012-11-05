from sys import argv

__author__ = 'sery0ga'

class Test(object):

    def __init__(self):
        self.doc = ''
        self.data = ''
        self.has_result = False
        self.result = ''
        self.is_true = True
        self.skip = False
        self.skip_reason = ''
        self.compile_only = False

    def __str__(self):
        return "Doc:\n%s\nFILE:\n%s\nRESULT:\n%s" \
            % (self.doc, self.data, self.result)

class Parser(object):

    (INITIAL, DOC, FILE, RESULT, SKIP, SKIPIF) = range(6)

    def parse(self, filename):
        test = Test()
        mode = self.INITIAL
        file_handler = open(filename, 'r')
        for line in file_handler:
            line = line.strip('\n')
            current_mode = mode

            if line == "--TEST--":
                mode = self.DOC
                continue
            elif line == "--FILE--":
                mode = self.FILE
                continue
            elif line == "--SKIP--":
                mode = self.SKIP
                test.skip = True
                continue
            elif line == "--SKIPIF--":
                # TODO
                mode = self.SKIPIF
                continue
            elif line == "--EXPECTF--" or line == "--EXPECT--":
                mode = self.RESULT
                test.has_result = True
                if line == "--EXPECTF--":
                    test.is_true = False
                continue
            elif line == "--COMPILEONLY--":
                test.compile_only = True

            if current_mode == self.DOC:
                if test.doc:
                    test.doc += "\n" + line
                else:
                    test.doc = line
            elif current_mode == self.RESULT:
                if test.result:
                    test.result += "\n" + line
                else:
                    test.result = line
            elif current_mode == self.FILE:
                if test.data:
                    test.data += "\n" + line
                else:
                    test.data = line
            elif current_mode == self.SKIP:
                if test.skip_reason:
                    test.skip_reason += "\n" + line
                else:
                    test.skip_reason = line

        file_handler.close()
        return test


if __name__ == "__main__":
    if len(argv) < 2:
        print 'No input FILE provided'
        exit()

    print Parser().parse(argv[1])
