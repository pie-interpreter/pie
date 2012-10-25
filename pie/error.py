__author__ = 'sery0ga'

class PHPError(Exception):
    (FATAL, WARNING, NOTICE) = ["Fatal", "Warning", "Notice"]

    def __init__(self, message, level, file, line):
        self.message = message
        self.level = level
        self.file = file
        self.line = line

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        message = "PHP %s error: %s in %s on line %s\n" \
            % (self.level, self.message, self.file, self.line)
        return message

class InterpreterError(Exception):
    pass


class CompilerError(Exception):
    pass
