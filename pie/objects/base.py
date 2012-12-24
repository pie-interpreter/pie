

class W_Root(object):
    """ The base class for everything that can be represented as a first-class
    object at applevel
    """
    def copy(self):
        assert False, "Should not be reached"

    def deref(self):
        assert False, "Should not be reached"

    def is_true(self):
        assert False, "Should not be reached"


class W_Type(W_Root):
    """ Base type class representing each type in PHP and common operations
    """

    def as_bool(self):
        assert False, "Should not be reached"

    def as_float(self):
        assert False, "Should not be reached"

    def as_int(self):
        assert False, "Should not be reached"

    def as_string(self):
        assert False, "Should not be reached"

    def as_number(self):
        assert False, "Should not be reached"

    def as_number_strict(self):
        assert False, "Should not be reached"

    def deref(self):
        return self

    def is_null(self):
        return False

    def less_than(self, object):
        assert False, "Should not be reached"

    def more_than(self, object):
        assert False, "Should not be reached"

    def equal(self, object):
        assert False, "Should not be reached"

    def not_equal(self, object):
        assert False, "Should not be reached"

    def less_than_or_equal(self, object):
        assert False, "Should not be reached"

    def more_than_or_equal(self, object):
        assert False, "Should not be reached"

    def inc(self):
        assert False, "Should not be reached"

    def dec(self):
        assert False, "Should not be reached"


class W_Number(W_Type):

    def plus(self, number):
        assert False, "Should not be reached"

    def minus(self, number):
        assert False, "Should not be reached"

    def multiply(self, number):
        assert False, "Should not be reached"

    def divide(self, number):
        assert False, "Should not be reached"

    def mod(self, number):
        assert False, "Should not be reached"


class DivisionByZeroError(Exception):
    pass
