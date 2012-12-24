from pie.interpreter.errors.base import Parse


class UnrecognizedSymbol(Parse):

    def __init__(self, context, text, line, column):
        self.line = line
        error_line = text.split("\n")[line]
        message = "syntax error, unexpected '%s'" % error_line[column]

        Parse.__init__(self, context, message)

    def get_line(self):
        return self.line


class InvalidSyntax(Parse):

    def __init__(self, context, errorinformation, line):
        self.line = line

        message = "syntax error"

        if errorinformation:
            failure_reasons = errorinformation.failure_reasons
            if len(failure_reasons) > 1:
                all_but_one = failure_reasons[:-1]
                last = failure_reasons[-1]
                expected = "%s or '%s'" % (
                    ", ".join(["'%s'" % e for e in all_but_one]), last)
            else:
                expected = "'%s'" % failure_reasons[0]
            message = ''.join([message, ", expected %s" % (expected, )])

        Parse.__init__(self, context, message)

    def get_line(self):
        return self.line
