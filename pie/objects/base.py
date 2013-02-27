from pie.types import PHPTypes


class W_Root(object):
    """ The base class for everything that can be represented as a first-class
    object at applevel
    """
    def copy(self):
        raise NotImplementedError

    def deref(self):
        raise NotImplementedError

    def is_true(self):
        raise NotImplementedError


class W_Type(W_Root):
    """ Base type class representing each type in PHP and common operations
    """
    php_type = -1

    def as_bool(self):
        raise NotImplementedError

    def as_float(self):
        raise NotImplementedError

    def as_int(self):
        raise NotImplementedError

    def as_string(self):
        raise NotImplementedError

    def as_number(self):
        raise NotImplementedError

    def as_number_strict(self):
        raise NotImplementedError

    def deref(self):
        return self

    def get_type(self):
        return self.php_type

    def is_null(self):
        return False

    def less_than(self, w_object):
        raise NotImplementedError

    def more_than(self, w_object):
        raise NotImplementedError

    def equal(self, w_object):
        raise NotImplementedError

    def not_equal(self, w_object):
        raise NotImplementedError

    def less_than_or_equal(self, w_object):
        raise NotImplementedError

    def more_than_or_equal(self, w_object):
        raise NotImplementedError

    def inc(self):
        raise NotImplementedError

    def dec(self):
        raise NotImplementedError


class W_Number(W_Type):

    def plus(self, number):
        raise NotImplementedError

    def minus(self, number):
        raise NotImplementedError

    def multiply(self, number):
        raise NotImplementedError

    def divide(self, number):
        raise NotImplementedError

    def mod(self, number):
        raise NotImplementedError


class DivisionByZeroError(Exception):
    pass


class W_Undefined(W_Type):

    php_type = PHPTypes.w_undefined

    def __repr__(self):
        return "W_Undefined()"

    def copy(self):
        return self
