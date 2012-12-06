from pie.objects.stringstrategies import *
from pypy.rlib import jit
from pie.objects.base import W_Type
from pie.objects.bool import W_BoolObject
from pie.objects.int import W_IntObject
from pie.objects.float import W_FloatObject

HEXADECIMAL_SYMBOLS = list("0123456789ABCDEFabcdef")

DECIMAL_SYMBOLS = list("0123456789")

(SYMBOL_Z, SYMBOL_A, SYMBOL_a, SYMBOL_z, SYMBOL_0, SYMBOL_9) = (90, 65, 97, 122, 48, 57)

class NotConvertibleToNumber(Exception):
    pass

class W_StringObject(W_Type):
    """
    This class represents PHP strings.
    It has 2 main attributes:
      - storage  -- contains string data. Its internal representation depends
                    on strategy.
      - strategy -- defines object behaviour. For more info see stringstrategies.py
    """
    convertible_to_number = True

    def __init__(self, strval):
        strategy = get_new_strategy(ConstantStringStrategy)
        self.storage = strategy.erase(strval)
        self.strategy = strategy
        self.copies = None

    def __repr__(self):
        return self.strategy.repr(self)

    def copy(self):
        res = self.strategy.copy(self)
        self.add_copy(res)
        return res

    def is_true(self):
        return self.strategy.is_true(self)

    def str_w(self):
        self.make_concrete()
        return self.strategy.str_w(self)

    def as_bool(self):
        self.make_concrete()
        if not self.is_true():
            return W_BoolObject(False)
        return W_BoolObject(True)

    def as_float(self):
        return self._handle_number(False).as_float()

    def as_int(self):
        value = self._handle_number(strict=False, int_only=True)
        assert isinstance(value, W_IntObject)
        return value

    def as_number(self):
        return self._handle_number(False)

    def as_number_strict(self):
        """
        There's a special case in PHP when we try to convert
        a string to number and if the string is not a pure number
        (like 1e2, 1.43 or 555), we leave the string as a string object

        The above rule is applied, for example, to string increment/decrement
        """
        if not self.convertible_to_number:
            raise NotConvertibleToNumber
        return self._handle_number(True)

    def as_string(self):
        return self

    def equal(self, w_object):
        if self is w_object:
            return W_BoolObject(True)
        if self.strlen() != w_object.strlen():
            return W_BoolObject(False)
        assert isinstance(w_object, W_StringObject)
        if self.strategy is w_object.strategy:
            return W_BoolObject(self.strategy.equal(self, w_object))
        self.force_concatenate()
        w_object.force_concatenate()
        return W_BoolObject(self.str_w() == w_object.str_w())

    def not_equal(self, w_object):
        w_result = self.equal(w_object)
        return W_BoolObject(not w_result.is_true())

    def less_than(self, w_object):
        if self is w_object:
            return W_BoolObject(False)
        assert isinstance(w_object, W_StringObject)
        self.force_concatenate()
        w_object.force_concatenate()
        return W_BoolObject(self.str_w() < w_object.str_w())

    def more_than(self, w_object):
        if self is w_object:
            return W_BoolObject(False)
        assert isinstance(w_object, W_StringObject)
        self.force_concatenate()
        w_object.force_concatenate()
        return W_BoolObject(self.str_w() > w_object.str_w())

    def less_than_or_equal(self, w_object):
        if self is w_object:
            return W_BoolObject(True)
        assert isinstance(w_object, W_StringObject)
        self.force_concatenate()
        w_object.force_concatenate()
        return W_BoolObject(self.str_w() <= w_object.str_w())

    def more_than_or_equal(self, w_object):
        if self is w_object:
            return W_BoolObject(True)
        assert isinstance(w_object, W_StringObject)
        self.force_concatenate()
        w_object.force_concatenate()
        return W_BoolObject(self.str_w() >= w_object.str_w())

    def inc(self):
        if not self.is_true():
            return W_StringObject('1')
        try:
            return self.as_number_strict().inc()
        except NotConvertibleToNumber:
            pass
        self.make_mutable()
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

    def dec(self):
        if not self.is_true():
            return W_IntObject(-1)
        try:
            return self.as_number_strict().dec()
        except NotConvertibleToNumber:
            # there's no decrement for normal non-convertible strings in PHP
            return self

    def concatenate(self, string):
        return StringFactory.newstrconcat(self, string)

    def strlen(self):
        return self.strategy.len(self)



    def add_copy(self, other):
        if self.copies is None:
            self.copies = [other]
        else:
            self.copies.append(other)

    def make_concrete(self):
        self.strategy.make_concrete(self)

    def force_concatenate(self):
        self.strategy.force_concatenate(self)

    def make_mutable(self):
        self.make_concrete()
        if self.copies:
            self._force_mutable_copies()
        self.strategy.make_mutable(self)


    def _force_mutable_copies(self):
        for copy in self.copies:
            if copy:
                copy.make_concrete()
        self.copies = None

    def _handle_number(self, strict = False, int_only = False):
        """
        Converts string to number
        """
        #TODO: add setlocale() support
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
            if int_only:
                return self._handle_decimal(string, begin, end, value_len, strict)
            return self._handle_float_or_decimal(string, begin, end, value_len, strict)

    def _handle_float_or_decimal(self, value, begin, end, value_len, strict = False):
        #detect minus
        minus = 1
        if value[0] == '-':
            begin += 1
            end += 1
            minus = -1

        e_symbol = False # for numbers '1e2'
        dot_symbol = False
        number_after_e_symbol = False
        while end < value_len:
            if value[end] not in DECIMAL_SYMBOLS:
                if not dot_symbol and value[end] == '.':
                    dot_symbol = True
                    end += 1
                    continue
                if not e_symbol and \
                   (value[end] == 'e' or value[end] == 'E'):
                    e_symbol = True
                    end += 1
                    continue
                self.convertible_to_number = False
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
        if e_symbol or dot_symbol:
            return W_FloatObject(float(value) * minus)
        #TODO add PHP_INT_MAX check
        return W_IntObject(int(value) * minus)

    def _handle_decimal(self, value, begin, end, value_len, strict = False):
        #detect minus
        minus = 1
        if value[0] == '-':
            begin += 1
            end += 1
            minus = -1

        while end < value_len:
            if value[end] not in DECIMAL_SYMBOLS:
                self.convertible_to_number = False
                if strict:
                    raise NotConvertibleToNumber
                else:
                    break
            end += 1

        if minus and end == 0:
            return W_IntObject(0)
        elif minus == -1 and end == 1:
            return W_IntObject(0)

        assert begin >= 0
        assert end >= 0
        value = self.str_w()[begin:end]
        #TODO add PHP_INT_MAX check
        return W_IntObject(int(value) * minus)

    def _handle_hexadecimal(self, value, begin, end, value_len, strict = False):
        while end < value_len:
            if value[end] not in HEXADECIMAL_SYMBOLS:
                self.convertible_to_number = False
                if strict:
                    raise NotConvertibleToNumber
                else:
                    break
            end += 1

        if not end:
            return W_IntObject(0)
        return W_IntObject(int(self.str_w()[begin:end], 0))
