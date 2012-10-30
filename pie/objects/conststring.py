from pie.objects.base import W_Root
from pie.objects.bool import W_BoolObject
from pie.objects.int import W_IntObject

HEXADECIMAL_SYMBOLS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                       'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f']

DECIMAL_SYMBOLS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

class NotConvertibleToNumber(Exception):
    pass

class W_ConstStringObject(W_Root):
    _immutable_fields_ = ['value']

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "W_ConstStringObject(%s)" % self.value

    def str_w(self):
        return self.value

    def as_int(self):
        return self._handle_int()

    def as_int_strict(self):
        return self._handle_int(True)

    def as_bool(self):
        if not self.value or self.value == '0':
            return W_BoolObject(False)
        return W_BoolObject(True)

    def as_number(self):
        return self.as_int()

    def as_string(self):
        return self

    def concatenate(self, string):
        return W_ConstStringObject(''.join([self.value, string.value]))

    def less_than(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_ConstStringObject)
        if self.value < object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more_than(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_ConstStringObject)
        if self.value > object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_ConstStringObject)
        if self.value == object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def not_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_ConstStringObject)
        if self.value != object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def less_than_or_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_ConstStringObject)
        if self.value <= object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more_than_or_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_ConstStringObject)
        if self.value >= object.value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def _handle_int(self, strict = False):
        if not self.value:
            return W_IntObject(0)

        (begin, end) = (0, 0)
        value_len = len(self.value)
        # check for hexadecimal
        if value_len > 2 and self.value[end] == '0' and\
           (self.value[end + 1] == 'x' or self.value[end + 1] == 'X'):
            end += 2
            return self._handle_hexadecimal(self.value, begin, end, value_len, strict)
        else:
            assert begin >= 0
            assert end >= 0
            return self._handle_decimal(self.value, begin, end, value_len, strict)

    def _handle_decimal(self, value, begin, end, value_len, strict = False):
        #detect minus
        minus = 1
        if self.value[0] == '-':
            begin += 1
            end += 1
            minus = -1

        e_symbol = False # for numbers '1e2'
        number_after_e_symbol = False
        while end < value_len:
            if value[end] not in DECIMAL_SYMBOLS:
                if not e_symbol and \
                   (value[end] == 'e' or value[end] == 'E'):
                    e_symbol = True
                    end += 1
                    continue
                if strict:
                    raise NotConvertibleToNumber
                else:
                    break
            if e_symbol:
                number_after_e_symbol = True
            end += 1
        # truncate 'e' if it's the last symbol in number
        if e_symbol and not number_after_e_symbol:
            end -= 1

        if minus and end == 0:
            return W_IntObject(0)
        elif minus == -1 and end == 1:
            return W_IntObject(0)

        assert begin >= 0
        assert end >= 0
        value = self.value[begin:end]
        if e_symbol:
            return W_IntObject(int(float(value)) * minus)

        return W_IntObject(int(value) * minus)

    def _handle_hexadecimal(self, value, begin, end, value_len, strict = False):
        while end < value_len:
            if value[end] not in HEXADECIMAL_SYMBOLS:
                if strict:
                    raise NotConvertibleToNumber
                else:
                    break
            end += 1

        if not end:
            return W_IntObject(0)

        return W_IntObject(int(value[begin:end], 0))