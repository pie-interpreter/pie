from pie.objects.base import W_Number, DivisionByZeroError
from pie.objspace import space
from pie.types import PHPTypes


class W_Float(W_Number):

    _immutable_fields_ = ['value', 'php_type']
    php_type = PHPTypes.w_float

    def __init__(self, value):
        self.value = value
        self.nan = False

    def __repr__(self):
        return "W_Float(%s)" % self.value

    def copy(self):
        return W_Float(self.value)

    def is_true(self):
        return bool(self.value)

    def float_w(self):
        return self.value

    def as_array(self):
        array = space.array()
        return array.set(0, self.value)

    def as_bool(self):
        return space.bool(bool(self.value))

    def as_float(self):
        return self

    def as_int(self):
        return space.int(int(self.value))

    def as_number(self):
        return self

    def as_string(self):
        # simple check to remove trailing 0 in float values
        intvalue = int(self.value)
        if intvalue == self.value:
            value = intvalue
        else:
            value = self.value
        from pie.objects.string import W_String

        return W_String(str(value))

    def less_than(self, w_object):
        assert isinstance(w_object, W_Float)
        if self.value < w_object.value:
            return space.bool(True)
        else:
            return space.bool(False)

    def more_than(self, w_object):
        assert isinstance(w_object, W_Float)
        if self.value > w_object.value:
            return space.bool(True)
        else:
            return space.bool(False)

    def equal(self, w_object):
        assert isinstance(w_object, W_Float)
        if self.value == w_object.value:
            return space.bool(True)
        else:
            return space.bool(False)

    def not_equal(self, w_object):
        assert isinstance(w_object, W_Float)
        if self.value != w_object.value:
            return space.bool(True)
        else:
            return space.bool(False)

    def less_than_or_equal(self, w_object):
        assert isinstance(w_object, W_Float)
        if self.value <= w_object.value:
            return space.bool(True)
        else:
            return space.bool(False)

    def more_than_or_equal(self, w_object):
        assert isinstance(w_object, W_Float)
        if self.value >= w_object.value:
            return space.bool(True)
        else:
            return space.bool(False)

    def inc(self):
        return W_Float(self.value + 1)

    def dec(self):
        return W_Float(self.value - 1)

    def plus(self, number):
        return W_Float(self.value + number.value)

    def minus(self, number):
        return W_Float(self.value - number.value)

    def multiply(self, number):
        return W_Float(self.value * number.value)

    def divide(self, number):
        if not number.value:
            raise DivisionByZeroError()

        return W_Float(self.value / number.value)

    def mod(self, number):
        if not number.value:
            raise DivisionByZeroError()

        divider = number.value
        if self.value < 0 and divider:
            divider *= -1
        elif self.value and divider < 0:
            divider *= -1

        return W_Float(self.value % divider)
