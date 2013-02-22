from pie.objspace import space
from pie.objects.base import W_Type
from pie.types import PHPTypes

class IllegalOffsetType(Exception):
    pass

class W_ArrayObject(W_Type):

    _immutable_fields = ['type']
    type = PHPTypes.w_array

    def __init__(self, raw_data = []):
        self.storage = {}
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
                index = self._convert_index(w_data_unit)
                if self.last_index_changed:
                    self._update_last_index(index)

    def __repr__(self):
        return "W_ArrayObject(%s)" % self.storage

    def copy(self):
        raw_data = []
        for key, value in self.storage.iteritems():
            raw_data.append(space.str(key))
            raw_data.append(value)
        return space.array(raw_data)

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
        elif self_length == object_length:
            return self._compare_elements('less_than', w_object)
        return space.bool(False)

    def more_than(self, w_object):
        assert isinstance(w_object, W_ArrayObject)
        self_length = len(self.storage)
        object_length = len(w_object.storage)
        if self_length > object_length:
            return space.bool(True)
        elif self_length == object_length:
            return self._compare_elements('more_than', w_object)
        return space.bool(False)

    def equal(self, w_object):
        assert isinstance(w_object, W_ArrayObject)
        if len(self.storage) != len(w_object.storage):
            return space.bool(False)
        return self._compare_elements('equal', w_object)

    def not_equal(self, w_object):
        assert isinstance(w_object, W_ArrayObject)
        if len(self.storage) != len(w_object.storage):
            return space.bool(True)
        else:
            for key,value in self.storage.iteritems():
                if key not in w_object.storage:
                    return space.bool(True)
                if space.not_equal(value, w_object.storage[key]).is_true():
                    return space.bool(True)
            return space.bool(False)

    def less_than_or_equal(self, w_object):
        assert isinstance(w_object, W_ArrayObject)
        self_length = len(self.storage)
        object_length = len(w_object.storage)
        if self_length < object_length:
            return space.bool(True)
        elif self_length == object_length:
            return self._compare_elements('less_than_or_equal', w_object)
        return space.bool(False)

    def more_than_or_equal(self, w_object):
        assert isinstance(w_object, W_ArrayObject)
        self_length = len(self.storage)
        object_length = len(w_object.storage)
        if self_length > object_length:
            return space.bool(True)
        elif self_length == object_length:
            return self._compare_elements('more_than_or_equal', w_object)
        return space.bool(False)

    def inc(self):
        return self

    def dec(self):
        return self

    def len(self):
        return len(self.storage)

    def get(self, w_index):
        assert isinstance(w_index, W_Type)
        index = self._convert_index(w_index)
        return self.storage[index]

    def set(self, w_index, w_value):
        assert isinstance(w_index, W_Type)
        assert isinstance(w_value, W_Type)
        index = self._convert_index(w_index)
        self.storage[index] = w_value
        if self.last_index_changed:
            self._update_last_index(index)

    def _compare_elements(self, operation, w_object):
        for key, w_value in self.storage.iteritems():
            if key not in w_object.storage:
                return space.bool(False)
            if not getattr(space, operation)(w_value,
                                             w_object.storage[key]).is_true():
                return space.bool(False)
        return space.bool(True)

    def _convert_index(self, w_index):
        # Right now all indexes are strings because
        #  we cannot translate otherwise.
        #TODO: change such behaviour as soon as internal represent. is implement
        if w_index.type == PHPTypes.w_float or \
            w_index.type == PHPTypes.w_int or \
            w_index.type == PHPTypes.w_bool:
            key = w_index.as_int().int_w()
            if key >= self.last_index:
                self.last_index_changed = True
            return str(key)
        elif w_index.type == PHPTypes.w_string:
            key = w_index.str_w()
            if (len(key) > 1 and key[0] == '0') \
                or (key[0] == '-' and key[1] == '0'):
                return key
            try:
                key = int(key)
                if key >= self.last_index:
                    self.last_index_changed = True
                return str(key)
            except ValueError:
                pass
            return key
        elif w_index.type == PHPTypes.w_null:
            return ""
        elif w_index.type == PHPTypes.w_undefined:
            key = self.last_index
            self.last_index_changed = True
            return str(key)
        else:
            raise IllegalOffsetType

    def _update_last_index(self, index):
        if isinstance(index, str):
            index = int(index)
        self.last_index = index + 1
        self.last_index_changed = False