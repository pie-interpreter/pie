from pie.error import InterpreterError

__author__ = 'sery0ga'

class W_Root(object):
    """ The base class for everything that can be represented as a first-class
    object at applevel
    """
    def copy(self):
        raise InterpreterError("Not implemented")

    def deref(self):
        raise InterpreterError("Not implemented")

    def is_true(self):
        raise InterpreterError("Not implemented")


class W_Type(W_Root):
    """ Base type class representing each type in PHP and common operations
    """
    def as_bool(self):
        raise InterpreterError("Not implemented")

    def as_float(self):
        raise InterpreterError("Not implemented")

    def as_int(self):
        raise InterpreterError("Not implemented")

    def as_string(self):
        raise InterpreterError("Not implemented")

    def as_number(self):
        raise InterpreterError("Not implemented")

    def as_number_strict(self):
        raise InterpreterError("Not implemented")

    def deref(self):
        return self

    def is_null(self):
        return False

    def less_than(self, object):
        raise InterpreterError("Not implemented")

    def more_than(self, object):
        raise InterpreterError("Not implemented")

    def equal(self, object):
        raise InterpreterError("Not implemented")

    def not_equal(self, object):
        raise InterpreterError("Not implemented")

    def less_than_or_equal(self, object):
        raise InterpreterError("Not implemented")

    def more_than_or_equal(self, object):
        raise InterpreterError("Not implemented")

    def inc(self):
        raise InterpreterError("Not implemented")

    def dec(self):
        raise InterpreterError("Not implemented")


class W_Number(W_Type):

    def plus(self, number):
        raise InterpreterError("Not implemented")

    def minus(self, number):
        raise InterpreterError("Not implemented")

    def multiply(self, number):
        raise InterpreterError("Not implemented")

    def divide(self, number):
        raise InterpreterError("Not implemented")

    def mod(self, number):
        raise InterpreterError("Not implemented")
