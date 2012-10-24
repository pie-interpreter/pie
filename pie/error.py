__author__ = 'sery0ga'

class PHPError:
    (FATAL, WARNING, NOTICE) = ["Fatal", "Warning", "Notice"]

    def __init__(self, message = ""):
        self.message = message
        self.level = self.NOTICE

    def __repr__(self):
        message = "PHP %s error: %s\n" % (self.level, self.message)
        return message

class InterpreterError(Exception):
    pass


class CompilerError(Exception):
    pass
