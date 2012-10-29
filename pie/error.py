__author__ = 'sery0ga'

class PHPError(Exception):
    (FATAL, WARNING, NOTICE) = ["Fatal", "Warning", "Notice"]

    def __init__(self, message, level, file, line, trace_stack = []):
        self.message = message
        self.level = level
        self.file = file
        self.line = line
        self.trace_stack = trace_stack

    def __repr__(self):
        return self.print_message()

    def __str__(self):
        return self.print_message()

    def print_message(self):
        import os.path

        message = "PHP %s error: %s in %s on line %s\n" \
            % (self.level, self.message, os.path.abspath(self.file), self.line)
        if self.trace_stack:
            message = ''.join([message, "PHP Stack trace:\n"])
            depth = 1
            for (function_name, line_number, filename) in self.trace_stack:
                trace_message = "PHP   %s. %s() %s:%s\n" \
                    % (depth, function_name, os.path.abspath(filename), line_number)
                message = ''.join([message, trace_message])
                depth += 1
        return message

class InterpreterError(Exception):
    pass


class CompilerError(Exception):
    pass
