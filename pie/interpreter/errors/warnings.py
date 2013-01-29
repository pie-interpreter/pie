import os.path
from pie.interpreter.errors.base import Warning


class DivisionByZero(Warning):

    def __init__(self, context):
        message = "Division by zero"
        Warning.__init__(self, context, message)


class MissingArgument(Warning):

    def __init__(self, context, arg_position, function):
        self.function = function
        message = "Missing argument %s for %s(), called" \
            % (arg_position, function.name)

        Warning.__init__(self, context, message)

    def get_additional_message(self):
        return "and defined in %s on line %s" % \
            (os.path.abspath(self.function.bytecode.filename),
                self.function.line_declared)


class NotEnoughParameters(Warning):

    def __init__(self, context, given, expected, name):
        message = "%s() expects at least %s parameters, %s given" \
            % (name, expected, given)

        Warning.__init__(self, context, message)


class WrongParameterType(Warning):

    def __init__(self, context, given, expected, position, name):
        message = "%s() expects parameter %s to be %s, %s given" \
            (name, position, expected, given)

        Warning.__init__(self, context, message)


class NoFile(Warning):

    def __init__(self, context, include_function, included_file):
        message = "%s(%s): failed to open stream: "\
                  "No such file or directory" % (include_function, included_file)
        Warning.__init__(self, context, message)


class NoFileInIncludePath(Warning):

    def __init__(self, context, include_function, included_file, include_path):
        message = "%s(): Failed opening '%s' for inclusion " \
            "(include_path='%s')" % (include_function, included_file, include_path)
        Warning.__init__(self, context, message)
