from pie.objspace import space
from pie.objects.base import W_Type
from pie.types import PHPTypes

class W_ArrayObject(W_Type):

    _immutable_fields = ['type']
    type = PHPTypes.w_array

    def __init__(self, raw_data = []):
        self.storage = {}
        self.last_index = 0
        record = False
        key = None
        for data_unit in raw_data:
            if record:
                record = False
                self.storage[key] = data_unit
            else:
                record = True
                key = self._get_key(data_unit)

    def _get_key(self, data_unit):
        if data_unit.type == PHPTypes.w_float or \
            data_unit.type == PHPTypes.w_int or \
            data_unit.type == PHPTypes.w_bool:
            key = data_unit.as_int().int_w()
            if key >= self.last_index:
                self.last_index = key + 1
            return key
        elif data_unit.type == PHPTypes.w_string:
            key = data_unit.str_w()
            if key[0] == '0' or (key[0] == '-' and key[1] == '0'):
                return key
            try:
                key = int(key)
                if key >= self.last_index:
                    self.last_index = key + 1
            except ValueError:
                pass
            return key
        elif data_unit.type == PHPTypes.w_null:
            return ""
        elif data_unit.type == PHPTypes.w_undefined:
            key = self.last_index
            self.last_index = key + 1
            return key
        else:
            #TODO: Illegal offset type
            raise NotImplementedError

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
        return space.bool(self.is_true())

    def as_float(self):
        return space.float(float(self.is_true()))

    def as_int(self):
        return space.int(int(self.is_true()))

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
        assert isinstance(object, W_ArrayObject)
        if len(self.storage) != len(object.storage):
            return space.bool(False)
        for key,value in self.storage.iteritems():
            if key not in object.storage:
                return space.bool(False)
            if not space.equal(value, object.storage[key]).is_true():
                return space.bool(False)
        return space.bool(True)

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