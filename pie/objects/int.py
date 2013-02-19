from pie.objects.base import W_Number, DivisionByZeroError
from pie.types import PHPTypes


class W_IntObject(W_Number):

    _immutable_fields_ = ['value', 'type']
    type = PHPTypes.w_int

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "W_IntObject(%s)" % self.value

    def __eq__(self, other):
        return self.value == other.value

    def copy(self):
        return W_IntObject(self.value)

    def is_true(self):
        return bool(self.value)

    def int_w(self):
        return self.value

    def as_bool(self):
        from pie.objects.bool import W_BoolObject
        return W_BoolObject(bool(self.value))

    def as_float(self):
        from pie.objects.float import W_FloatObject
        return W_FloatObject(float(self.value))

    def as_int(self):
        return self

    def as_number(self):
        return self

    def as_string(self):
        from pie.objects.string import W_StringObject
        return W_StringObject(str(self.value))

    def less_than(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_IntObject)
        if self.value < object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more_than(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_IntObject)
        if self.value > object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_IntObject)
        if self.value == object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def not_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_IntObject)
        if self.value != object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def less_than_or_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_IntObject)
        if self.value <= object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more_than_or_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_IntObject)
        if self.value >= object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def inc(self):
        return W_IntObject(self.value + 1)

    def dec(self):
        return W_IntObject(self.value - 1)

    def plus(self, number):
        return W_IntObject(self.value + number.value)

    def minus(self, number):
        return W_IntObject(self.value - number.value)

    def multiply(self, number):
        return W_IntObject(self.value * number.value)

    def divide(self, number):
        if not number.value:
            raise DivisionByZeroError()
        # if the numbers are evenly divisible, we should return int
        if not self.value % number.value:
            return W_IntObject(self.value / number.value)
        from pie.objects.float import W_FloatObject
        return W_FloatObject(float(self.value) / number.value)

    def mod(self, number):
        if not number.value:
            raise DivisionByZeroError()
        divider = number.value
        if self.value < 0 and divider > 0:
            divider *= -1
        elif self.value > 0 and divider < 0:
            divider *= -1
        return W_IntObject(self.value % divider)
