from sys import argv


class Test(object):

    def __init__(self):
        self.doc = ''
        self.source = ''
        self.has_result = False
        self.result = []
        self.is_true = True
        self.skip = False
        self.skip_reason = ''
        self.compile_only = False
        self.check_parts_of_result = False

    def __str__(self):
        return "Doc:\n%s\nFILE:\n%s\nRESULT:\n%s" \
            % (self.doc, self.source, self.result)


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
            elif line == "--EXPECTF--" or line == "--EXPECT--" or line == "--EXPECT_ERROR--":
                mode = self.RESULT
                test.has_result = True
                if line == "--EXPECTF--":
                    test.is_true = False
                elif line == "--EXPECT_ERROR--":
                    test.check_parts_of_result = True
                continue
            elif line == "--COMPILEONLY--":
                test.compile_only = True

            if current_mode == self.DOC:
                if test.doc:
                    test.doc += "\n" + line
                else:
                    test.doc = line
            elif current_mode == self.RESULT:
                test.result.append(line)
            elif current_mode == self.FILE:
                if test.source:
                    test.source += "\n" + line
                else:
                    test.source = line
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
