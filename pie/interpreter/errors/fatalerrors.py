import os.path
from pie.interpreter.errors.base import Fatal


class UndefinedFunction(Fatal):

    def __init__(self, context, function_name):
        message = "Call to undefined function %s()" % function_name
        Fatal.__init__(self, context, message)


class RedeclaredFunction(Fatal):

    def __init__(self, context, function):
        self.function = function

        message = "Cannot redeclare %s()" % function.name
        Fatal.__init__(self, context, message)

    def get_line(self):
        return self.function.line_declared


class RedeclaredUserFunction(RedeclaredFunction):

    def __init__(self, context, new_function, old_function):
        self.function = new_function

        message = "Cannot redeclare %s() (previously declared in %s:%s)" % \
            (old_function.name,
                os.path.abspath(old_function.bytecode.filename),
                old_function.line_declared)
        Fatal.__init__(self, context, message)


class NoRequiredFile(Fatal):

    def __init__(self, context, include_function, included_file):
        message = "%s(%s): failed to open stream: "\
                  "No such file or directory" % (include_function, included_file)
        Fatal.__init__(self, context, message)


class NoRequiredFileInIncludePath(Fatal):

    def __init__(self, context, include_function, included_file, include_path):
        message = "%s(): Failed opening required '%s' for inclusion " \
            "(include_path='%s')" % (include_function, included_file, include_path)
        Fatal.__init__(self, context, message)


class NonVariablePassedByReference(Fatal):

    def __init__(self, context):
        message = "Only variables can be passed by reference"
        Fatal.__init__(self, context, message)


class IllegalBreakContinueLevel(Fatal):

    def __init__(self, context, level):
        if level == 1:
            level_string = 'level'
        else:
            level_string = 'levels'
        message = "Cannot break/continue %s levels" % level_string

        Fatal.__init__(self, context, message)
