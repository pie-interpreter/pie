import sys

__author__ = 'sery0ga'


class PieError(Exception):
    pass


class InterpreterError(PieError):
    pass

class DivisionByZeroError(InterpreterError):
    pass

class PHPError(InterpreterError):
    (FATAL, WARNING, NOTICE) = ["Fatal", "Warning", "Notice"]

    def __init__(self, context, message, level, show_trace=True):
        self.message = message
        self.level = level
        self.context = context
        self.show_trace = show_trace
        self.prefix = ''

    def __repr__(self):
        return self.print_message()

    def __str__(self):
        return self.print_message()

    def print_message(self):
        import os.path

        execution_block = self.context.trace.current_execution_block
        message = "PHP %s:  %s in %s on line %s %s"\
            % (self.level, self.message,
                os.path.abspath(execution_block.get_filename()), execution_block.get_line(),
                self.prefix)
        if self.show_trace:
            message = ''.join([message, self.context.trace.to_string()])
        return message
    def handle(self):
        if self.context.config.display_error(self):
            if self.context.config.display_to_stderr:
                sys.stderr.write(self.print_message() + "\n")
            else:
                print self.print_message()


class PHPFatal(PHPError):
    def __init__(self, context, message, show_trace=True, prefix=''):
        PHPError.__init__(self, context, message, PHPError.FATAL, show_trace)
        self.prefix = prefix


class PHPWarning(PHPError):
    def __init__(self, context, message, show_trace=True, prefix=''):
        PHPError.__init__(self, context, message, PHPError.WARNING, show_trace)
        self.prefix = prefix


class PHPNotice(PHPError):
    def __init__(self, context, message, show_trace=True, prefix=''):
        PHPError.__init__(self, context, message, PHPError.NOTICE, show_trace)
        self.prefix = prefix


class UndefinedFunction(PHPFatal):
    def __init__(self, context, function_name):
        message = "Call to undefined function %s()" % function_name

        PHPFatal.__init__(self, context, message)


class RedeclaredFunction(PHPFatal):
    def __init__(self, context, function_name, function_object):
        import os.path
        message = "Cannot redeclare %s() (previously declared in %s:%s)" % \
            (function_name, os.path.abspath(function_object.bytecode.filename),
                function_object.line_declared)

        PHPFatal.__init__(self, context, message, False)


class NoRequiredFile(PHPFatal):
    def __init__(self, context, include_function, included_file):
        message = "%s(%s): failed to open stream: "\
                  "No such file or directory" % (include_function, included_file)

        PHPFatal.__init__(self, context, message, False)


class NoRequiredFileInIncludePath(PHPFatal):
    def __init__(self, context, include_function, included_file, include_path):
        message = "%s(): Failed opening required '%s' for inclusion " \
            "(include_path='%s')" % (include_function, included_file, include_path)

        PHPFatal.__init__(self, context, message, False)


class DivisionByZero(PHPWarning):
    def __init__(self, context):
        message = "Division by zero"

        PHPWarning.__init__(self, context, message)


class MissingArgument(PHPWarning):
    def __init__(self, context, arg_position, function_name, function_object):
        import os.path
        message = "Missing argument %s for %s(), called" \
            % (arg_position, function_name)
        prefix = "and defined in %s on line %s" % \
            (os.path.abspath(function_object.bytecode.filename), function_object.line_declared)

        PHPWarning.__init__(self, context, message, False, prefix)


class NoFile(PHPWarning):
    def __init__(self, context, include_function, included_file):
        message = "%s(%s): failed to open stream: "\
                  "No such file or directory" % (include_function, included_file)

        PHPWarning.__init__(self, context, message, False)


class NoFileInIncludePath(PHPWarning):
    def __init__(self, context, include_function, included_file, include_path):
        message = "%s(): Failed opening '%s' for inclusion " \
            "(include_path='%s')" % (include_function, included_file, include_path)

        PHPWarning.__init__(self, context, message, False)


class UndefinedVariable(PHPNotice):
    def __init__(self, context, name):
        message = "Undefined variable: %s" % name

        PHPNotice.__init__(self, context, message, False)


class CompilerError(Exception):
    pass


class LexerError(Exception):

    def __init__(self, error, text):
        self.lexer_error = error
        self.text = text

    def nice_error_message(self, filename="<unknown>"):
        import os.path
        error_line = self.text.split("\n")[self.lexer_error.source_pos.lineno]

        result = ["PHP Lexing error in %s, line %s" %
                  (os.path.abspath(filename), self.lexer_error.source_pos.lineno + 1)]
        result.append(error_line)
        result.append(" " * self.lexer_error.source_pos.columnno + "^")
        result.append("Unexpected '%s'" % error_line[self.lexer_error.source_pos.columnno])

        return "\n".join(result)
