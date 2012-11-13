from pie.error import DivisionByZero
from pie.objects.base import W_Root
from pie.objects.int import W_IntObject


class W_FloatObject(W_Root):
    _immutable_fields_ = ['value']

    def __init__(self, value):
        self.value = value
        self.nan = False

    def __repr__(self):
        return "W_FloatObject(%s)" % self.value

    def float_w(self):
        return self.value

    def as_bool(self):
        from pie.objects.bool import W_BoolObject
        return W_BoolObject(bool(self.value))

    def as_float(self):
        return self

    def as_int(self):
        return W_IntObject(int(self.value))

    def as_string(self):
        #TODO: make better float print support: not 11.0 but 11
        from pie.objects.string import W_StringObject
        return W_StringObject(str(self.value))

    def copy(self):
        return W_FloatObject(self.value)

    def hard_copy(self):
        return self.copy()

    def is_true(self):
        return bool(self.value)

    def plus(self, number):
        return W_FloatObject(self.value + number.value)

    def minus(self, number):
        return W_FloatObject(self.value - number.value)

    def multiply(self, number):
        return W_FloatObject(self.value * number.value)

    def inc(self):
        return W_FloatObject(self.value + 1)

    def dec(self):
        return W_FloatObject(self.value - 1)

    def mod(self, number):
        if not number.value:
            raise DivisionByZero
        divider = number.value
        if self.value < 0 and divider:
            divider *= -1
        elif self.value and divider < 0:
            divider *= -1
        return W_FloatObject(self.value % divider)

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
