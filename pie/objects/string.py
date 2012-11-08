from pie.objects.stringstrategies import *
from pypy.rlib.objectmodel import instantiate
from pypy.rlib import jit
from pie.objects.base import W_Root
from pie.objects.bool import W_BoolObject
from pie.objects.int import W_IntObject
import operator

HEXADECIMAL_SYMBOLS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                       'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f']

DECIMAL_SYMBOLS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

(SYMBOL_Z, SYMBOL_A, SYMBOL_a, SYMBOL_z, SYMBOL_0, SYMBOL_9) = (90, 65, 97, 122, 48, 57)

METHOD_TO_OPERATOR = {
    'equal': 'eq',
    'not_equal': 'ne',
    'less_than': 'lt',
    'less_than_or_equal': 'le',
    'more_than': 'gt',
    'more_than_or_equal': 'ge'

}

class NotConvertibleToNumber(Exception):
    pass

class W_StringObject(W_Root):

    def __init__(self, strval):
        strategy = get_new_strategy(ConstantStringStrategy)
        self.storage = strategy.erase(strval)
        self.strategy = strategy
        self.copies = None

    def __repr__(self):
        return self.strategy.repr(self)

    @staticmethod
    def newstr(strval):
        w_s = instantiate(W_StringObject)
        strategy = get_new_strategy(MutableStringStrategy)
        w_s.storage = strategy.erase(strval)
        w_s.strategy = strategy
        w_s.copies = None
        return w_s

    @staticmethod
    def newcopiedstr(origobj):
        w_s = instantiate(W_StringObject)
        strategy = get_new_strategy(StringCopyStrategy)
        w_s.copies = None
        w_s.storage = strategy.erase(origobj)
        w_s.strategy = strategy
        return w_s

    @staticmethod
    def newstrconcat(origobj, other):
        w_s = instantiate(W_StringObject)
        strategy = get_new_strategy(StringConcatStrategy)
        w_s.copies = None
        w_s.storage = strategy.erase((origobj, other, origobj.strlen() +
                                                      other.strlen()))
        w_s.strategy = strategy
        origobj.add_copy(w_s)
        other.add_copy(w_s)
        return w_s

    def add_copy(self, other):
        if self.copies is None:
            self.copies = [other]
        else:
            self.copies.append(other)

    def write_into(self, s, start):
        self.strategy.write_into(self, s, start)

    def force(self):
        if self.strategy.concrete:
            return
        self.strategy.force(self)

    def force_concatenate(self):
        self.strategy.force_concatenate(self)

    def _force_mutable_copies(self):
        for copy in self.copies:
            if copy:
                copy.force()
        self.copies = None

    def force_mutable(self):
        self.force()
        if self.copies:
            self._force_mutable_copies()
        self.strategy.make_mutable(self)

    def conststr_w(self):
        self.force()
        return self.strategy.conststr_w(self)

    def str_w(self):
        self.force()
        return self.strategy.str_w(self)

    def strlen(self):
        return self.strategy.len(self)

    def copy(self):
        res = self.strategy.copy(self)
        self.add_copy(res)
        return res

    def as_string(self):
        return self

    def is_true(self):
        return self.strategy.is_true(self)

    def as_int(self):
        return self._handle_int(False)

    def as_int_strict(self):
        return self._handle_int(True)

    def as_bool(self):
        if not self.is_true() or self.str_w()[0] == '0':
            return W_BoolObject(False)
        return W_BoolObject(True)

    def as_number(self):
        return self.as_int()

    def concatenate(self, string):
        return W_StringObject.newstrconcat(self, string)

    def inc(self):
        if not self.is_true():
            return W_IntObject(1)
        try:
            return self.as_int_strict().inc()
        except NotConvertibleToNumber:
            #TODO make a flag for convertible to string
            pass
        self.force_mutable()
        index = self.strlen() - 1
        symbol = ''
        while index >= 0:
            item = self.strategy.getitem(self, index)
            symbol_index = ord(item[0])
            if SYMBOL_A <= symbol_index <= SYMBOL_z or SYMBOL_0 <= symbol_index <= SYMBOL_9:
                if symbol_index == SYMBOL_9:
                    symbol = '0'
                    self.strategy.setitem(self, index, symbol)
                elif symbol_index == SYMBOL_Z:
                    symbol = 'A'
                    self.strategy.setitem(self, index, symbol)
                elif symbol_index == SYMBOL_z:
                    symbol = 'a'
                    self.strategy.setitem(self, index, symbol)
                else:
                    symbol_index += 1
                    self.strategy.setitem(self, index, chr(symbol_index))
                    return self
            else:
                return self
            index -= 1
        if index < 0 and symbol:
            self.strategy.append(self, symbol)

        return self

    def _ord(self, character):
        return ord(character)

    def dec(self):
        if not self.is_true():
            return W_IntObject(-1)
        try:
            return self.as_int_strict().dec()
        except NotConvertibleToNumber:
            # there's no decrement for normal non-convertible strings in PHP
            return self

    def equal(self, w_object):
        if self is w_object:
            return W_BoolObject(True)
        if self.strlen() != w_object.strlen():
            return W_BoolObject(False)
        assert isinstance(w_object, W_StringObject)
        self.force_concatenate()
        w_object.force_concatenate()
        if self.strategy is w_object.strategy:
            return W_BoolObject(self.strategy.equal(self, w_object))
        return W_BoolObject(self.str_w() == w_object.str_w())

    def less_than(self, w_object):
        if self is w_object:
            return W_BoolObject(False)
        assert isinstance(w_object, W_StringObject)
        self.force_concatenate()
        w_object.force_concatenate()
        if self.strategy is w_object.strategy:
            return W_BoolObject(self.strategy.less_than(self, w_object))
        return W_BoolObject(self.str_w() < w_object.str_w())

    def more_than(self, w_object):
        if self is w_object:
            return W_BoolObject(False)
        assert isinstance(w_object, W_StringObject)
        self.force_concatenate()
        w_object.force_concatenate()
        if self.strategy is w_object.strategy:
            return W_BoolObject(self.strategy.more_than(self, w_object))
        return W_BoolObject(self.str_w() > w_object.str_w())

    def not_equal(self, w_object):
        if self is w_object:
            return W_BoolObject(False)
        if self.strlen() != w_object.strlen():
            return W_BoolObject(True)
        assert isinstance(w_object, W_StringObject)
        self.force_concatenate()
        w_object.force_concatenate()
        if self.strategy is w_object.strategy:
            return W_BoolObject(self.strategy.not_equal(self, w_object))
        return W_BoolObject(self.str_w() != w_object.str_w())

    def less_than_or_equal(self, object):
        assert isinstance(object, W_StringObject)
        left_value = self.str_w()
        right_value = object.str_w()
        if left_value <= right_value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more_than_or_equal(self, object):
        assert isinstance(object, W_StringObject)
        left_value = self.str_w()
        right_value = object.str_w()
        if left_value >= right_value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def _handle_int(self, strict = False):
        self.force_concatenate()
        if not self.is_true():
            return W_IntObject(0)

        (begin, end) = (0, 0)
        value_len = self.strlen()
        string = self.str_w()
        # check for hexadecimal
        if value_len > 2 and string[end] == '0' and \
           (string[end + 1] == 'x' or string[end + 1] == 'X'):
            end += 2
            return self._handle_hexadecimal(string, begin, end, value_len, strict)
        else:
            assert begin >= 0
            assert end >= 0
            return self._handle_decimal(string, begin, end, value_len, strict)

    def _handle_decimal(self, value, begin, end, value_len, strict = False):
        #detect minus
        minus = 1
        if value[0] == '-':
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
        value = self.str_w()[begin:end]
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

        return W_IntObject(int(self.str_w()[begin:end], 0))