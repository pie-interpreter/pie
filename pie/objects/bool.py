from pie.objects.base import W_Type
from pie.objspace import space
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
        array = space.array([])
        array.set(0, self.value)

    def as_bool(self):
        return self

    def as_float(self):
        return space.float(float(self.value))

    def as_int(self):
        return space.int(int(self.value))

    def as_number(self):
        return self.as_int()

    def as_string(self):
        if self.value:
            return space.str('1')
        return space.str('')


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