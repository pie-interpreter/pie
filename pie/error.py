__author__ = 'sery0ga'

class PHPError(Exception):
    (FATAL, WARNING, NOTICE) = ["Fatal", "Warning", "Notice"]

    def __init__(self, message, level = ""):
        self.message = message
        if len(level):
            self.level = level
        else:
            self.level = self.NOTICE

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        message = "PHP %s error: %s\n" % (self.level, self.message)
        return message

class InterpreterError(Exception):
    pass


class CompilerError(Exception):
    pass
