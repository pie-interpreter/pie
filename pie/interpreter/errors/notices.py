from pie.interpreter.errors.base import Notice


class UndefinedVariable(Notice):

    def __init__(self, context, name):
        message = "Undefined variable: %s" % name
        Notice.__init__(self, context, message)


class NonVariableReturnedByReference(Notice):

    def __init__(self, context):
        message = "Only variable references should be returned by reference"
        Notice.__init__(self, context, message)
