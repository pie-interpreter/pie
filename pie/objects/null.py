from pie.objects.base import W_Type
from pie.objspace import space
from pie.types import PHPTypes


class W_NullObject(W_Type):

    _immutable_fields_ = ['type']
    php_type = PHPTypes.w_null

    def __repr__(self):
        return "W_NullObject()"

    def copy(self):
        return self

    def is_true(self):
        return False

    def as_array(self):
        return space.array()

    def as_bool(self):
        return space.bool(False)

    def as_int(self):
        return space.int(0)

    def as_float(self):
        return space.float(0.0)

    def as_number(self):
        return self.as_int()

    def as_number_strict(self):
        return self.as_int()

    def as_string(self):
        return space.str("")

    def is_null(self):
        return True

    def less_than(self, object):
        return space.bool(False)

    def more_than(self, object):
        return space.bool(False)

    def equal(self, object):
        return space.bool(True)

    def not_equal(self, object):
        return space.bool(False)

    def less_than_or_equal(self, object):
        return space.bool(True)

    def more_than_or_equal(self, object):
        return space.bool(True)

    def inc(self):
        """
        http://www.php.net/manual/en/language.operators.increment.php

         Decrementing NULL values has no effect too, but incrementing them results in 1.
        """
        return space.int(1)

    def dec(self):
        """
        http://www.php.net/manual/en/language.operators.increment.php

         Decrementing NULL values has no effect too, but incrementing them results in 1.
        """
        return self