from pie.rpy.rdict import RDict

from pie.objspace import space
from pie.objects.base import W_Type, W_Root
from pie.types import PHPTypes


class IllegalOffsetType(Exception):
    pass


class W_ArrayObject(W_Type):

    _immutable_fields = ['type']
    type = PHPTypes.w_array

    @staticmethod
    def array_from_array(w_array):
        w_new_array = W_ArrayObject()
        w_new_array.storage = w_array.storage.copy()
        return w_new_array

    def __init__(self, raw_data=[]):
        self.storage = RDict(W_Root)
        self.last_index = 0
        self.last_index_changed = False

        record = False
        index = None
        for w_data_unit in raw_data:
            if record:
                record = False
                self.storage[index] = w_data_unit
            else:
                record = True
                int_index, str_index = self._convert_index(w_data_unit)
                if self.last_index_changed:
                    self._update_last_index(int_index)
                if str_index is None:
                    index = str(int_index)
                else:
                    index = str_index

    def __repr__(self):
        return "W_ArrayObject(%s)" % self.storage

    def copy(self):
        return W_ArrayObject.array_from_array(self)

    def is_true(self):
        if not self.storage:
            return False
        return True

    def as_array(self):
        return self

    def as_bool(self):
        return space.bool(self.is_true())

    def as_float(self):
        #TODO: make caution
        # http://www.php.net/manual/en/language.types.integer.php
        return space.float(float(self.is_true()))

    def as_int(self):
        #TODO: make caution
        # http://www.php.net/manual/en/language.types.integer.php
        return space.int(int(self.is_true()))

    def as_number(self):
        return self.as_int()

    def as_string(self):
        from pie.objects.string import W_StringObject
        return W_StringObject('Array')

    def less_than(self, w_object):
        assert isinstance(w_object, W_ArrayObject)
        self_length = len(self.storage)
        object_length = len(w_object.storage)
        if self_length < object_length:
            return space.bool(True)
        elif self_length == object_length and self_length > 0:
            iterator = self.storage.iter()
            for i in range(len(self.storage)):
                key, w_value = iterator.nextitem()
                if key not in w_object.storage:
                    return space.bool(False)
                w_result = space.less_than(w_value,
                                           w_object.storage[key])
                if not w_result.is_true():
                    return space.bool(False)
                return space.bool(True)
        return space.bool(False)

    def more_than(self, w_object):
        assert isinstance(w_object, W_ArrayObject)
        self_length = len(self.storage)
        object_length = len(w_object.storage)
        if self_length > object_length:
            return space.bool(True)
        elif self_length == object_length and self_length > 0:
            iterator = self.storage.iter()
            for i in range(len(self.storage)):
                key, w_value = iterator.nextitem()
                if key not in w_object.storage:
                    return space.bool(False)
                w_result = space.more_than(w_value,
                                           w_object.storage[key])
                if not w_result.is_true():
                    return space.bool(False)
                return space.bool(True)
        return space.bool(False)

    def equal(self, w_object):
        assert isinstance(w_object, W_ArrayObject)
        if len(self.storage) != len(w_object.storage):
            return space.bool(False)
        iterator = self.storage.iter()
        for i in range(len(self.storage)):
            key, w_value = iterator.nextitem()
            if key not in w_object.storage:
                return space.bool(False)
            w_result = space.equal(w_value,
                                   w_object.storage[key])
            if not w_result.is_true():
                return space.bool(False)
            return space.bool(True)
        return space.bool(True)

    def not_equal(self, w_object):
        assert isinstance(w_object, W_ArrayObject)
        if len(self.storage) != len(w_object.storage):
            return space.bool(True)
        else:
            iterator = self.storage.iter()
            for i in range(len(self.storage)):
                key, w_value = iterator.nextitem()
                if key not in w_object.storage:
                    return space.bool(True)
                if space.not_equal(w_value, w_object.storage[key]).is_true():
                    return space.bool(True)
            return space.bool(False)

    def less_than_or_equal(self, w_object):
        assert isinstance(w_object, W_ArrayObject)
        self_length = len(self.storage)
        object_length = len(w_object.storage)
        if self_length < object_length:
            return space.bool(True)
        elif self_length == object_length:
            iterator = self.storage.iter()
            for i in range(len(self.storage)):
                key, w_value = iterator.nextitem()
                if key not in w_object.storage:
                    return space.bool(False)
                w_result = space.less_than_or_equal(w_value,
                                                    w_object.storage[key])
                if not w_result.is_true():
                    return space.bool(False)
                return space.bool(True)
        return space.bool(False)

    def more_than_or_equal(self, w_object):
        assert isinstance(w_object, W_ArrayObject)
        self_length = len(self.storage)
        object_length = len(w_object.storage)
        if self_length > object_length:
            return space.bool(True)
        elif self_length == object_length:
            iterator = self.storage.iter()
            for i in range(len(self.storage)):
                key, w_value = iterator.nextitem()
                if key not in w_object.storage:
                    return space.bool(False)
                w_result = space.more_than_or_equal(w_value,
                                                    w_object.storage[key])
                if not w_result.is_true():
                    return space.bool(False)
                return space.bool(True)
        return space.bool(False)

    def inc(self):
        return self

    def dec(self):
        return self

    def len(self):
        return len(self.storage)

    def get(self, w_index):
        assert isinstance(w_index, W_Type)
        int_index, str_index = self._convert_index(w_index)
        if str_index is None:
            index = str(int_index)
        else:
            index = str_index
        return W_Cell(index, self.storage[index])

    def set(self, w_index, w_value):
        assert isinstance(w_index, W_Type)
        assert isinstance(w_value, W_Type)
        int_index, str_index = self._convert_index(w_index)
        if str_index is None:
            index = str(int_index)
        else:
            index = str_index

        self.storage[index] = w_value
        if self.last_index_changed:
            self._update_last_index(int_index)

    def _compare_elements(self, operation, w_object):
        for key, w_value in self.storage.iteritems():
            if key not in w_object.storage:
                return space.bool(False)
            w_result = getattr(space, operation)(w_value,
                                                 w_object.storage[key])
            if not w_result.is_true():
                return space.bool(False)
        return space.bool(True)

    def _convert_index(self, w_index):
        if (w_index.type == PHPTypes.w_float or
                w_index.type == PHPTypes.w_int or
                w_index.type == PHPTypes.w_bool):
            key = w_index.as_int().int_w()
            if key >= self.last_index:
                self.last_index_changed = True
            return key, None
        elif w_index.type == PHPTypes.w_string:
            key = w_index.str_w()
            if (len(key) > 1 and
                    ((key[0] == '0') or (key[0] == '-' and key[1] == '0'))):
                return 0, key
            try:
                key = int(key)
                if key >= self.last_index:
                    self.last_index_changed = True
                return key, None
            except ValueError:
                pass
            return 0, key
        elif w_index.type == PHPTypes.w_null:
            return 0, ""
        elif w_index.type == PHPTypes.w_undefined:
            key = self.last_index
            self.last_index_changed = True
            return key, None
        else:
            raise IllegalOffsetType

    def _update_last_index(self, index):
        assert isinstance(index, int)
        self.last_index = index + 1
        self.last_index_changed = False


class W_Cell(W_Root):

    def __init__(self, index, w_value):
        self.index = index
        self.value = w_value

    def deref(self):
        return self.value.deref()
