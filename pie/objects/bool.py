from pie.objects.base import W_Type
from pie.objects.float import W_FloatObject
from pie.objects.int import W_IntObject
from pie.objects.array import W_ArrayObject
from pie.types import PHPTypes

class W_BoolObject(W_Type):

    _immutable_fields_ = ['value', 'type']

    def __init__(self, value):
        self.value = bool(value)
        self.type = PHPTypes.w_bool

    def __repr__(self):
        return "W_BoolObject(%s)" % self.value

    def copy(self):
        return W_BoolObject(self.value)

    def is_true(self):
        return self.value

    def as_array(self):
        array = W_ArrayObject()
        array.set(0, self.value)

    def as_bool(self):
        return self

    def as_float(self):
        return W_FloatObject(float(self.value))

    def as_int(self):
        return W_IntObject(int(self.value))

    def as_number(self):
        return self.as_int()

    def as_string(self):
        from pie.objects.string import W_StringObject
        if self.value:
            return W_StringObject('1')
        return W_StringObject('')


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

    def inc(self):
        """
        http://www.php.net/manual/en/language.operators.increment.php

         The increment/decrement operators do not affect boolean values
        """
        return self

    def dec(self):
        """
        http://www.php.net/manual/en/language.operators.increment.php

         The increment/decrement operators do not affect boolean values
        """
        return self