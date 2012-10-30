from pie.objects.base import W_Root
from pie.objects.int import W_IntObject

class W_BoolObject(W_Root):

    _immutable_fields_ = ['value']

    def __init__(self, value):
        self.value = bool(value)

    def __repr__(self):
        return "W_BoolObject(%s)" % self.value

    def as_int(self):
        return W_IntObject(int(self.value))

    def as_string(self):
        from pie.objects.conststring import W_ConstStringObject
        if self.value:
            return W_ConstStringObject('1')
        return W_ConstStringObject('')

    def as_bool(self):
        return self

    def is_true(self):
        return self.value

    def plus(self, number):
        return W_IntObject(int(self.value + number.value))

    def minus(self, number):
        return W_IntObject(int(self.value - number.value))

    def multiply(self, number):
        return W_IntObject(int(self.value * number.value))

    def mod(self, number):
        raise NotImplemented

    def less_than(self, object):
        assert isinstance(object, W_BoolObject)
        if self.value < object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more_than(self, object):
        assert isinstance(object, W_BoolObject)
        if self.value > object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def equal(self, object):
        assert isinstance(object, W_BoolObject)
        if self.value == object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def not_equal(self, object):
        assert isinstance(object, W_BoolObject)
        if self.value != object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def less_than_or_equal(self, object):
        assert isinstance(object, W_BoolObject)
        if self.value <= object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more_than_or_equal(self, object):
        assert isinstance(object, W_BoolObject)
        if self.value >= object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)