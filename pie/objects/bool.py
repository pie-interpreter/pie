from pie.objects.base import W_Type
from pie.objspace import space
from pie.types import PHPTypes


class W_Bool(W_Type):

    _immutable_fields_ = ['value', 'php_type']
    php_type = PHPTypes.w_bool

    def __init__(self, value):
        self.value = bool(value)

    def __repr__(self):
        return "W_Bool(%s)" % self.value

    def copy(self):
        return W_Bool(self.value)

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
            return space.string('1')
        return space.string('')

    def less_than(self, w_object):
        assert isinstance(w_object, W_Bool)
        if self.value < w_object.value:
            return W_Bool(True)
        else:
            return W_Bool(False)

    def more_than(self, w_object):
        assert isinstance(w_object, W_Bool)
        if self.value > w_object.value:
            return W_Bool(True)
        else:
            return W_Bool(False)

    def equal(self, w_object):
        assert isinstance(w_object, W_Bool)
        if self.value == w_object.value:
            return W_Bool(True)
        else:
            return W_Bool(False)

    def not_equal(self, w_object):
        assert isinstance(w_object, W_Bool)
        if self.value != w_object.value:
            return W_Bool(True)
        else:
            return W_Bool(False)

    def less_than_or_equal(self, w_object):
        assert isinstance(w_object, W_Bool)
        if self.value <= w_object.value:
            return W_Bool(True)
        else:
            return W_Bool(False)

    def more_than_or_equal(self, w_object):
        assert isinstance(w_object, W_Bool)
        if self.value >= w_object.value:
            return W_Bool(True)
        else:
            return W_Bool(False)

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