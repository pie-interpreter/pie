__author__ = 'sery0ga'

from pie.error import InterpreterError


class W_Root(object):
    """ The base class for everything that can be represented as a first-class
    object at applevel
    """
    def deref(self):
        return self # anything but a reference

    def int_w(self, space):
        raise InterpreterError("TypeError: casting to int of wrong type")

    def str_w(self, space):
        raise InterpreterError("TypeError: casting to string of wrong type")

    def conststr_w(self, space):
        raise InterpreterError("TypeError: casting to string of wrong type")