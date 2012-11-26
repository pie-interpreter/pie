from pie.error import DivisionByZeroError
from pie.objects.base import W_Number
from pie.objects.int import W_IntObject

class W_FloatObject(W_Number):
    _immutable_fields_ = ['value']

    def __init__(self, value):
        self.value = value
        self.nan = False

    def __repr__(self):
        return "W_FloatObject(%s)" % self.value

    def copy(self):
        return W_FloatObject(self.value)

    def is_true(self):
        return bool(self.value)

    def float_w(self):
        return self.value

    def as_bool(self):
        from pie.objects.bool import W_BoolObject
        return W_BoolObject(bool(self.value))

    def as_float(self):
        return self

    def as_int(self):
        return W_IntObject(int(self.value))

    def as_number(self):
        return self

    def as_string(self):
        # simple check to remove trailing 0 in float values
        intvalue = int(self.value)
        if intvalue == self.value:
            value = intvalue
        else:
            value = self.value
        from pie.objects.string import W_StringObject

        return W_StringObject(str(value))

    def less_than(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_FloatObject)
        if self.value < object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more_than(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_FloatObject)
        if self.value > object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_FloatObject)
        if self.value == object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def not_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_FloatObject)
        if self.value != object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def less_than_or_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_FloatObject)
        if self.value <= object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more_than_or_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_FloatObject)
        if self.value >= object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def inc(self):
        return W_FloatObject(self.value + 1)

    def dec(self):
        return W_FloatObject(self.value - 1)


    def plus(self, number):
        return W_FloatObject(self.value + number.value)

    def minus(self, number):
        return W_FloatObject(self.value - number.value)

    def multiply(self, number):
        return W_FloatObject(self.value * number.value)

    def divide(self, number):
        if not number.value:
            raise DivisionByZeroError
        return W_FloatObject(self.value / number.value)

    def mod(self, number):
        if not number.value:
            raise DivisionByZeroError
        divider = number.value
        if self.value < 0 and divider:
            divider *= -1
        elif self.value and divider < 0:
            divider *= -1
        return W_FloatObject(self.value % divider)

