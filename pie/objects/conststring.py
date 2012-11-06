from pypy.rlib.rerased import new_erasing_pair
from pypy.rlib.objectmodel import instantiate, specialize, compute_hash,\
    _hash_string
from pypy.rlib import jit

from pie.objects.base import W_Root
from pie.objects.bool import W_BoolObject
from pie.objects.int import W_IntObject

HEXADECIMAL_SYMBOLS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                       'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f']

DECIMAL_SYMBOLS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

(SYMBOL_Z, SYMBOL_z, SYMBOL_9) = (90, 122, 57)

class NotConvertibleToNumber(Exception):
    pass

cache = {}

@specialize.memo()
def new_strategy(strategy):
    try:
        return cache[strategy]
    except KeyError:
        new_strategy = strategy()
        cache[strategy] = new_strategy
        return new_strategy

class BaseStringStrategy(object):
    concat = False

    def copy(self, obj):
        return W_StringObject.newcopiedstr(obj)

    def get_string_source(self, obj):
        return obj

    def force_concat(self, obj):
        pass

class ConstantStringStrategy(BaseStringStrategy):
    erase, unerase = new_erasing_pair("constant")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    concrete = True

    def conststr_w(self, storage):
        return self.unerase(storage)

    def getitem(self, storage, item):
        return self.unerase(storage)[item]

    def setitem(self, storage, item, val):
        raise Exception("Should not happen")

    def len(self, storage):
        return len(self.unerase(storage))

    def getchar(self, storage):
        s = self.unerase(storage)
        if len(s) == 0:
            return '\x00'
        return s[0]

    def str_w(self, storage):
        return self.unerase(storage)

    def force_mutable(self, strobj):
        newstrat = new_strategy(MutableStringStrategy)
        strobj.strategy = newstrat
        strobj.storage = newstrat.erase([c
                                         for c in self.unerase(strobj.storage)])

    def copy(self, obj):
        return W_StringObject(self.unerase(obj.storage))

    def repr(self, storage):
        return 'C(%s)' % self.unerase(storage)

    def force_copy(self, sourcestorage, destobj):
        destobj.storage = self.erase(self.unerase(sourcestorage)[:])

    def write_into(self, storage, target, start):
        s = self.unerase(storage)
        i = 0
        for c in s:
            target[start + i] = c
            i += 1

    def append(self, storage, target):
        s = self.unerase(storage)
        i = 0
        for c in s:
            target.append(c)
            i += 1

    def is_true(self, storage):
        return bool(self.unerase(storage))

    def eq(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

    def strslice(self, space, storage, start, stop):
        return W_StringObject(self.unerase(storage)[start:stop])

    def hash(self, storage):
        return compute_hash(self.unerase(storage))

class MutableStringStrategy(BaseStringStrategy):
    erase, unerase = new_erasing_pair("mutable")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    concrete = True

    def conststr_w(self, storage):
        return ''.join(self.unerase(storage))

    def getitem(self, storage, item):
        return self.unerase(storage)[item]

    def len(self, storage):
        return len(self.unerase(storage))

    def force_mutable(self, strobj):
        pass

    def setitem(self, storage, item, val):
        self.unerase(storage)[item] = val

    def getchar(self, storage):
        s = self.unerase(storage)
        if len(s) == 0:
            return '\x00'
        return s[0]

    def str_w(self, storage):
        return "".join(self.unerase(storage))

    def repr(self, storage):
        return 'M(%s)' % ''.join(self.unerase(storage))

    def force_copy(self, sourcestorage, destobj):
        destobj.storage = self.erase(self.unerase(sourcestorage)[:])

    def write_into(self, storage, target, start):
        s = self.unerase(storage)
        for i, c in enumerate(s):
            target[start + i] = c

    def append(self, storage, target):
        s = self.unerase(storage)
        target.extend(s)

    def is_true(self, storage):
        return bool(self.unerase(storage))

    def eq(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

    def strslice(self, space, storage, start, stop):
        return W_StringObject.newstr(self.unerase(storage)[start:stop])

    def inplace_concat(self, space, storage, w_obj):
        l = self.unerase(storage)
        w_obj.strategy.append(w_obj.storage, l)

    def hash(self, storage):
        return hash_string(self.unerase(storage))

class StringCopyStrategy(BaseStringStrategy):
    erase, unerase = new_erasing_pair("copy")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    concrete = False

    def force(self, obj):
        w_orig = self.unerase(obj.storage)
        w_orig.force()
        obj.strategy = w_orig.strategy
        w_orig.strategy.force_copy(w_orig.storage, obj)

    def getitem(self, storage, index):
        w_parent = self.unerase(storage)
        return w_parent.strategy.getitem(w_parent.storage, index)

    def getchar(self, storage):
        w_parent = self.unerase(storage)
        return w_parent.strategy.getchar(w_parent.storage)

    def len(self, storage):
        w_parent = self.unerase(storage)
        return w_parent.strlen()

    def repr(self, storage):
        return 'SC(%r)' % self.unerase(storage)

    def write_into(self, storage, target, start):
        parent = self.unerase(storage)
        parent.write_into(target, start)

    def append(self, storage, target):
        parent = self.unerase(storage)
        parent.strategy.append(parent.storage, target)

    def get_string_source(self, obj):
        return self.unerase(obj.storage)

    def is_true(self, storage):
        parent = self.unerase(storage)
        return parent.strategy.is_true(parent.storage)

    def eq(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

    def strslice(self, space, storage, start, stop):
        return self.unerase(storage).strslice(space, start, stop)

    def force_concat(self, obj):
        self.unerase(obj.storage).force_concat()

    def hash(self, storage):
        parent = self.unerase(storage)
        return parent.strategy.hash(parent.storage)

class StringConcatStrategy(BaseStringStrategy):
    erase, unerase = new_erasing_pair("concat")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    concrete = False
    concat = True

    def force(self, obj):
        s = ['\x00'] * self.len(obj.storage)
        self.write_into(obj.storage, s, 0)
        strategy = new_strategy(MutableStringStrategy)
        obj.storage = strategy.erase(s)
        obj.strategy = strategy

    def force_concat(self, obj):
        self.force(obj)

    def len(self, storage):
        l_one, l_two, lgt = self.unerase(storage)
        return lgt

    def append(self, storage, target):
        lgt = len(target)
        target.extend(['\x00'] * self.len(storage))
        self.write_into(storage, target, lgt)

    def write_into(self, storage, target, start):
        l_one, l_two, lgt = self.unerase(storage)
        l_one.write_into(target, start)
        l_two.write_into(target, start + l_one.strlen())
        #so_far = [(0, l_one), (l_one.strlen(), l_two)]
        #while so_far:
        #    # XXX jit driver anyone?
        #    index, obj = so_far.pop()
        #    strat = obj.strategy
        #    obj = strat.get_string_source(obj)
        #    strat = obj.strategy # might be a different one
        #    if isinstance(strat, StringConcatStrategy):
        #        one, two, lgt = strat.unerase(obj.storage)
        #        so_far.append((index, one))
        #        so_far.append((index + one.strlen(), two))
        #    else:
        #        obj.write_into(target, index)

    def repr(self, storage):
        return 'CON(%r)' % (self.unerase(storage),)

    def is_true(self, storage):
        # XXX recursion? figure out a way to flatten those easier
        left, right = self.unerase(storage)
        return (left.strategy.is_true(left.storage) or
                right.strategy.is_true(right.storage))

class W_StringObject(W_Root):

    def __init__(self, strval):
        strategy = new_strategy(ConstantStringStrategy)
        self.storage = strategy.erase(strval)
        self.strategy = strategy
        self.copies = None

    @staticmethod
    def newstr(strval):
        w_s = instantiate(W_StringObject)
        strategy = new_strategy(MutableStringStrategy)
        w_s.storage = strategy.erase(strval)
        w_s.strategy = strategy
        w_s.copies = None
        return w_s

    @staticmethod
    def newcopiedstr(origobj):
        w_s = instantiate(W_StringObject)
        strategy = new_strategy(StringCopyStrategy)
        w_s.copies = None
        w_s.storage = strategy.erase(origobj)
        w_s.strategy = strategy
        return w_s

    @staticmethod
    def newstrconcat(origobj, other):
        w_s = instantiate(W_StringObject)
        strategy = new_strategy(StringConcatStrategy)
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
        self.strategy.write_into(self.storage, s, start)

    def force(self):
        if self.strategy.concrete:
            return
        self.strategy.force(self)

    def force_concat(self):
        self.strategy.force_concat(self)

    def _force_mutable_copies(self):
        for copy in self.copies:
            if copy:
                copy.force()
        self.copies = None

    def force_mutable(self):
        self.force()
        if self.copies:
            self._force_mutable_copies()
        self.strategy.force_mutable(self)

    def conststr_w(self):
        self.force()
        return self.strategy.conststr_w(self.storage)

    def getitem(self, space, w_arg):
        return space.newstrconst(str(self.strategy.getitem(self.storage,
            space.int_w(w_arg))))

    def setitem(self, space, w_arg, w_value):
        self.force_mutable()
        self.strategy.setitem(self.storage, space.int_w(w_arg),
            space.getchar(w_value))

    def str_w(self):
        self.force()
        return self.strategy.str_w(self.storage)

    def getchar(self, space):
        return self.strategy.getchar(self.storage)

    def strlen(self):
        return self.strategy.len(self.storage)

    def copy(self):
        res = self.strategy.copy(self)
        self.add_copy(res)
        return res

    def as_string(self):
        return self

    def is_true(self):
        return self.strategy.is_true(self.storage)

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

    def __repr__(self):
        return self.strategy.repr(self.storage)

    def concatenate(self, string):
        return W_StringObject.newstrconcat(self, string)

    def inc(self):
        if not self.is_true():
            return W_IntObject(1)
        self.force_mutable()
        length = self.strlen()
        if length == 1:
            symbol_number = ord(self.strategy.getitem(self.storage, 0))
            if symbol_number == SYMBOL_Z:
                self.strategy.setitem(self.storage, 0, 'A')
            elif symbol_number == SYMBOL_z:
                self.strategy.setitem(self.storage, 0, 'a')
            else:
                symbol_number += 1
                self.strategy.setitem(self.storage, 0, chr(symbol_number))
            return self

        index = length - 1
        while index >= 0:
            symbol_number = ord(self.strategy.getitem(self.storage, index))
            if symbol_number == SYMBOL_Z:
                self.strategy.setitem(self.storage, index, 'A')
            elif symbol_number == SYMBOL_z:
                self.strategy.setitem(self.storage, index, 'a')
            elif symbol_number == SYMBOL_9:
                self.strategy.setitem(self.storage, index, '0')
            else:
                symbol_number += 1
                self.strategy.setitem(self.storage, index, chr(symbol_number))
                break
            index -= 1

        return self

    def dec(self):
        if not self.is_true():
            return W_IntObject(-1)
        try:
            return self.as_int_strict().dec()
        except NotConvertibleToNumber:
            # there's no decrement for normal non-convertible strings in PHP
            return self

    def less_than(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_StringObject)
        left_value = self.str_w()
        right_value = object.str_w()
        if left_value < right_value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more_than(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_StringObject)
        left_value = self.str_w()
        right_value = object.str_w()
        if left_value > right_value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def equal(self, object):
        from pie.objects.bool import W_BoolObject
        if self is object:
            return W_BoolObject(True)
        if self.strlen() != object.strlen():
            return W_BoolObject(False)
        assert isinstance(object, W_StringObject)
        self.force_concat()
        object.force_concat()
        if self.strategy is object.strategy:
            return W_BoolObject(self.strategy.eq(self, object))
        return W_BoolObject(self.str_w() == object.str_w())

    def not_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_StringObject)
        left_value = self.str_w()
        right_value = object.str_w()
        if left_value != right_value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def less_than_or_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_StringObject)
        left_value = self.str_w()
        right_value = object.str_w()
        if left_value <= right_value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more_than_or_equal(self, object):
        from pie.objects.bool import W_BoolObject
        assert isinstance(object, W_StringObject)
        left_value = self.str_w()
        right_value = object.str_w()
        if left_value >= right_value:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def _handle_int(self, strict = False):
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

        return W_IntObject(int(value[:]) * minus)

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