from pie.objects.base import W_Type
from pie.objects.float import W_FloatObject
from pie.objects.int import W_IntObject


class W_ArrayObject(W_Type):

    def __init__(self):
        self.storage = {}

    def __repr__(self):
        return "W_ArrayObject(%s)" % self.storage

    def copy(self):
        assert NotImplementedError

    def is_true(self):
        if not self.storage:
            return False
        return True

    def as_array(self):
        return self

    def as_bool(self):
        from pie.objects.bool import W_BoolObject
        return W_BoolObject(self.is_true())

    def as_float(self):
        return W_FloatObject(float(self.is_true()))

    def as_int(self):
        return W_IntObject(int(self.is_true()))

    def as_number(self):
        return self.as_int()

    def as_string(self):
        from pie.objects.string import W_StringObject
        return W_StringObject('Array')

    def less_than(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_BoolObject)
        if self.storage < object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more_than(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_BoolObject)
        if self.storage > object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_ArrayObject)
        if self.storage == object.storage:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def not_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_BoolObject)
        if self.storage != object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def less_than_or_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_BoolObject)
        if self.storage <= object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more_than_or_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_BoolObject)
        if self.storage >= object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def inc(self):
        raise NotImplementedError

    def dec(self):
        raise NotImplementedError

    def set(self, index, value):
        self.storage[index] = value