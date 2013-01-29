from pie.objects.base import W_Type
from pie.objects.int import W_IntObject
import pie.objects.bool as boolean


class W_NullObject(W_Type):

    def __repr__(self):
        return "W_NullObject()"

    def copy(self):
        return self

    def is_true(self):
        return False

    def as_bool(self):
        return boolean.W_BoolObject(False)

    def as_int(self):
        return W_IntObject(0)

    def as_float(self):
        from pie.objects.float import W_FloatObject
        return W_FloatObject(0.0)

    def as_number(self):
        return self.as_int()

    def as_number_strict(self):
        return self.as_int()

    def as_string(self):
        from pie.objects.string import W_StringObject
        return W_StringObject("")

    def is_null(self):
        return True

    def less_than(self, object):
        return boolean.W_BoolObject(False)

    def more_than(self, object):
        return boolean.W_BoolObject(False)

    def equal(self, object):
        return boolean.W_BoolObject(True)

    def not_equal(self, object):
        return boolean.W_BoolObject(False)

    def less_than_or_equal(self, object):
        return boolean.W_BoolObject(True)

    def more_than_or_equal(self, object):
        return boolean.W_BoolObject(True)

    def inc(self):
        """
        http://www.php.net/manual/en/language.operators.increment.php

         Decrementing NULL values has no effect too, but incrementing them results in 1.
        """
        return W_IntObject(1)

    def dec(self):
        """
        http://www.php.net/manual/en/language.operators.increment.php

         Decrementing NULL values has no effect too, but incrementing them results in 1.
        """
        return self