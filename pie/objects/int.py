from pie.objects.base import W_Number, DivisionByZeroError
from pie.types import PHPTypes
from pie.objspace import space


class W_Int(W_Number):

    _immutable_fields_ = ['value', 'php_type']
    php_type = PHPTypes.w_int

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "W_Int(%s)" % self.value

    def __eq__(self, other):
        return self.value == other.value

    def copy(self):
        return W_Int(self.value)

    def is_true(self):
        return bool(self.value)

    def int_w(self):
        return self.value

    def as_bool(self):
        return space.bool(bool(self.value))

    def as_float(self):
        return space.float(float(self.value))

    def as_int(self):
        return self

    def as_number(self):
        return self

    def as_string(self):
        return space.string(str(self.value))

    def less_than(self, w_object):
        assert isinstance(w_object, W_Int)
        if self.value < w_object.value:
            return space.bool(True)
        else:
            return space.bool(False)

    def more_than(self, w_object):
        assert isinstance(w_object, W_Int)
        if self.value > w_object.value:
            return space.bool(True)
        else:
            return space.bool(False)

    def equal(self, w_object):
        assert isinstance(w_object, W_Int)
        if self.value == w_object.value:
            return space.bool(True)
        else:
            return space.bool(False)

    def not_equal(self, w_object):
        assert isinstance(w_object, W_Int)
        if self.value != w_object.value:
            return space.bool(True)
        else:
            return space.bool(False)

    def less_than_or_equal(self, w_object):
        assert isinstance(w_object, W_Int)
        if self.value <= w_object.value:
            return space.bool(True)
        else:
            return space.bool(False)

    def more_than_or_equal(self, w_object):
        assert isinstance(w_object, W_Int)
        if self.value >= w_object.value:
            return space.bool(True)
        else:
            return space.bool(False)

    def inc(self):
        return W_Int(self.value + 1)

    def dec(self):
        return W_Int(self.value - 1)

    def plus(self, number):
        return W_Int(self.value + number.value)

    def minus(self, number):
        return W_Int(self.value - number.value)

    def multiply(self, number):
        return W_Int(self.value * number.value)

    def divide(self, number):
        if not number.value:
            raise DivisionByZeroError()
        # if the numbers are evenly divisible, we should return int
        if not self.value % number.value:
            return W_Int(self.value / number.value)
        return space.float(float(self.value) / number.value)

    def mod(self, number):
        if not number.value:
            raise DivisionByZeroError()
        divider = number.value
        if self.value < 0 and divider > 0:
            divider *= -1
        elif self.value > 0 and divider < 0:
            divider *= -1
        return W_Int(self.value % divider)
