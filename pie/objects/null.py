from pie.objects.base import W_Root
from pie.objects.int import W_IntObject

__author__ = 'sery0ga'

class W_NullObject(W_Root):

    def copy(self):
        return self

    def is_true(self):
        return False

    def is_null(self):
        return True

    def as_bool(self):
        from pie.objects.bool import W_BoolObject
        return W_BoolObject(False)

    def as_int(self):
        from pie.objects.int import W_IntObject
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

    def less_than(self, object):
        from pie.objects.bool import W_BoolObject
        return W_BoolObject(False)

    def more_than(self, object):
        from pie.objects.bool import W_BoolObject
        return W_BoolObject(False)

    def equal(self, object):
        from pie.objects.bool import W_BoolObject
        return W_BoolObject(True)

    def not_equal(self, object):
        from pie.objects.bool import W_BoolObject
        return W_BoolObject(False)

    def less_than_or_equal(self, object):
        from pie.objects.bool import W_BoolObject
        return W_BoolObject(True)

    def more_than_or_equal(self, object):
        from pie.objects.bool import W_BoolObject
        return W_BoolObject(True)
