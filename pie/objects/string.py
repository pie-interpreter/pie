from pie.objects.strategy.base import get_string_strategy, StringFactory
from pie.objects.base import W_Type
from pie.objspace import space
from pie.types import PHPTypes

__author__ = 'sery0ga'


HEXADECIMAL_SYMBOLS = list("0123456789ABCDEFabcdef")

DECIMAL_SYMBOLS = list("0123456789")

(SYMBOL_Z, SYMBOL_A, SYMBOL_a, SYMBOL_z, SYMBOL_0, SYMBOL_9) = (90, 65, 97, 122, 48, 57)

class NotConvertibleToNumber(Exception):
    pass

class W_String(W_Type):
    """
    This class represents PHP strings.
    It has 2 main attributes:
      - storage  -- contains string data. Its internal representation depends
                    on strategy.
      - strategy -- defines object behaviour. For more info see stringstrategies.py
    """
    _immutable_fields_ = ['php_type']
    convertible_to_number = True
    php_type = PHPTypes.w_string

    def __init__(self, strval):
        from pie.objects.strategy.general import ConstantStringStrategy
        strategy = get_string_strategy(ConstantStringStrategy)
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
        self.make_integral()
        return self.strategy.str_w(self)

    def as_array(self):
        array = space.array()
        return array.set(0, self.str_w())

    def as_bool(self):
        self.make_integral()
        if not self.is_true():
            return space.bool(False)
        return space.bool(True)

    def as_float(self):
        return self._handle_number(False).as_float()

    def as_int(self):
        value = self._handle_number(strict=False, int_only=True)
        from pie.objects.int import W_Int
        assert isinstance(value, W_Int)
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

    def is_convertible_to_number_strict(self):
        try:
            self.as_number_strict()
            return space.bool(True)
        except NotConvertibleToNumber:
            return space.bool(False)

    def equal(self, w_object):
        if self is w_object:
            return space.bool(True)
        if self.strlen() != w_object.strlen():
            return space.bool(False)
        assert isinstance(w_object, W_String)
        if self.strategy is w_object.strategy:
            return space.bool(self.strategy.equal(self, w_object))
        self.make_integral()
        w_object.make_integral()
        return space.bool(self.str_w() == w_object.str_w())

    def not_equal(self, w_object):
        w_result = self.equal(w_object)
        return space.bool(not w_result.is_true())

    def less_than(self, w_object):
        if self is w_object:
            return space.bool(False)
        assert isinstance(w_object, W_String)
        self.make_integral()
        w_object.make_integral()
        return space.bool(self.str_w() < w_object.str_w())

    def more_than(self, w_object):
        if self is w_object:
            return space.bool(False)
        assert isinstance(w_object, W_String)
        self.make_integral()
        w_object.make_integral()
        return space.bool(self.str_w() > w_object.str_w())

    def less_than_or_equal(self, w_object):
        if self is w_object:
            return space.bool(True)
        assert isinstance(w_object, W_String)
        self.make_integral()
        w_object.make_integral()
        return space.bool(self.str_w() <= w_object.str_w())

    def more_than_or_equal(self, w_object):
        if self is w_object:
            return space.bool(True)
        assert isinstance(w_object, W_String)
        self.make_integral()
        w_object.make_integral()
        return space.bool(self.str_w() >= w_object.str_w())

    def inc(self):
        if not self.is_true():
            return space.string('1')
        try:
            return self.as_number_strict().inc()
        except NotConvertibleToNumber:
            pass
        self._make_mutable()
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
            return space.int(-1)
        try:
            return self.as_number_strict().dec()
        except NotConvertibleToNumber:
            # there's no decrement for normal non-convertible strings in PHP
            return self

    def concatenate(self, string):
        return StringFactory.concat_str(self, string)

    def strlen(self):
        return self.strategy.len(self)


    def make_integral(self):
        self.strategy.make_integral(self)

    def add_copy(self, w_copy):
        if self.copies is None:
            self.copies = [w_copy]
        else:
            self.copies.append(w_copy)

    def _make_mutable(self):
        self._dereference()
        if self.copies:
            self._dereference_copies()
        self.strategy.make_mutable(self)

    def _dereference(self):
        self.strategy.dereference(self)

    def _dereference_copies(self):
        for copy in self.copies:
            if copy:
                copy._dereference()
        self.copies = None

    def _handle_number(self, strict = False, int_only = False):
        """
        Converts string to number
        """
        #TODO: add setlocale() support
        self.make_integral()
        if not self.is_true():
            return space.int(0)
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
                if (not e_symbol and
                        (value[end] == 'e' or value[end] == 'E')):
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
            return space.int(0)
        elif minus == -1 and end == 1:
            return space.int(0)

        assert begin >= 0
        assert end >= 0
        value = self.str_w()[begin:end]
        if e_symbol or dot_symbol:
            return space.float(float(value) * minus)
        #TODO add PHP_INT_MAX check
        return space.int(int(value) * minus)

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
            return space.int(0)
        elif minus == -1 and end == 1:
            return space.int(0)

        assert begin >= 0
        assert end >= 0
        value = self.str_w()[begin:end]
        #TODO add PHP_INT_MAX check
        return space.int(int(value) * minus)

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
            return space.int(0)
        return space.int(int(self.str_w()[begin:end], 0))
