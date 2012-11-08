from pypy.rlib.rerased import new_erasing_pair
from pypy.rlib.objectmodel import specialize
import string

__author__ = 'sery0ga'

cache = {}

@specialize.memo()
def get_new_strategy(strategy):
    try:
        return cache[strategy]
    except KeyError:
        new_strategy = strategy()
        cache[strategy] = new_strategy
        return new_strategy

class BaseStringStrategy(object):
    concat = False

    def copy(self, obj):
        return string.W_StringObject.newcopiedstr(obj)

    def get_string_source(self, obj):
        return obj

    def force_concatenate(self, obj):
        pass

class ConstantStringStrategy(BaseStringStrategy):
    erase, unerase = new_erasing_pair("constant")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    concrete = True

    def append(self, string, value):
        raise Exception("You cannot change constant string")

    def conststr_w(self, storage):
        return self.unerase(storage)

    def copy(self, obj):
        return string.W_StringObject(self.unerase(obj.storage))

    def equal(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

    def force_copy(self, sourcestorage, destobj):
        destobj.storage = self.erase(self.unerase(sourcestorage)[:])

    def getchar(self, storage):
        s = self.unerase(storage)
        if not len(s):
            return '\x00'
        return s[0]

    def getitem(self, storage, item):
        return self.unerase(storage)[item]

    def is_true(self, storage):
        return bool(self.unerase(storage))

    def len(self, storage):
        return len(self.unerase(storage))

    def less_than(self, w_obj, w_other):
        return self.unerase(w_obj.storage) < self.unerase(w_other.storage)

    def make_mutable(self, strobj):
        new_strategy = get_new_strategy(MutableStringStrategy)
        strobj.strategy = new_strategy
        strobj.storage = new_strategy.erase([c for c in self.unerase(strobj.storage)])

    def more_than(self, w_obj, w_other):
        return self.unerase(w_obj.storage) > self.unerase(w_other.storage)

    def not_equal(self, w_obj, w_other):
        return self.unerase(w_obj.storage) != self.unerase(w_other.storage)

    def repr(self, storage):
        return 'C(%s)' % self.unerase(storage)

    def setitem(self, storage, item, value):
        raise Exception("You cannot change constant string")

    def str_w(self, storage):
        return self.unerase(storage)

    def write_into(self, storage, target, start):
        s = self.unerase(storage)
        i = 0
        for c in s:
            target[start + i] = c
            i += 1

class MutableStringStrategy(BaseStringStrategy):
    erase, unerase = new_erasing_pair("mutable")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    concrete = True

    def append(self, string, value):
        raw_string = self.unerase(string.storage)
        raw_string.append(value)
        string.storage = self.erase(raw_string)

    def conststr_w(self, storage):
        return ''.join(self.unerase(storage))

    def equal(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

    def force_copy(self, sourcestorage, destobj):
        destobj.storage = self.erase(self.unerase(sourcestorage)[:])

    def getchar(self, storage):
        s = self.unerase(storage)
        if not len(s):
            return '\x00'
        return s[0]

    def getitem(self, storage, item):
        return self.unerase(storage)[item]

    def is_true(self, storage):
        return bool(self.unerase(storage))

    def len(self, storage):
        return len(self.unerase(storage))

    def less_than(self, w_left, w_right):
        length = w_left.strlen()
        right_is_longer = True
        if length > w_right.strlen():
            length = w_right.strlen()
            right_is_longer = False
        raw_left = self.unerase(w_left.storage)
        raw_right = self.unerase(w_right.storage)
        for index in range(length - 1):
            if raw_left[index] < raw_right[index]:
                return True
            elif raw_left[index] == raw_right[index]:
                continue
            else:
                return False
        if w_left.strlen() == w_right.strlen() and raw_left[length] < raw_right[length]:
            return True
        elif raw_left[length] == raw_right[length] and right_is_longer:
            return True
        return False

    def make_mutable(self, strobj):
        pass

    def repr(self, storage):
        return 'M(%s)' % ''.join(self.unerase(storage))

    def setitem(self, storage, item, val):
        self.unerase(storage)[item] = val

    def str_w(self, storage):
        return "".join(self.unerase(storage))

    def write_into(self, storage, target, start):
        s = self.unerase(storage)
        for i, c in enumerate(s):
            target[start + i] = c

class StringCopyStrategy(BaseStringStrategy):
    erase, unerase = new_erasing_pair("copy")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    concrete = False

    def append(self, string, value):
        #TODO fix it
        raise Exception("You cannot modify copied string")

    def equal(self, w_left, w_right):
        return self.unerase(w_left.storage) == self.unerase(w_right.storage)

    def force_concatenate(self, obj):
        self.unerase(obj.storage).force_concatenate()

    def force(self, obj):
        w_orig = self.unerase(obj.storage)
        w_orig.force()
        obj.strategy = w_orig.strategy
        w_orig.strategy.force_copy(w_orig.storage, obj)

    def get_string_source(self, obj):
        return self.unerase(obj.storage)

    def getitem(self, storage, index):
        w_parent = self.unerase(storage)
        return w_parent.strategy.getitem(w_parent.storage, index)

    def getchar(self, storage):
        w_parent = self.unerase(storage)
        return w_parent.strategy.getchar(w_parent.storage)

    def is_true(self, storage):
        parent = self.unerase(storage)
        return parent.strategy.is_true(parent.storage)

    def len(self, storage):
        w_parent = self.unerase(storage)
        return w_parent.strlen()

    def repr(self, storage):
        return 'SC(%r)' % self.unerase(storage)

    def write_into(self, storage, target, start):
        parent = self.unerase(storage)
        parent.write_into(target, start)

class StringConcatStrategy(BaseStringStrategy):
    erase, unerase = new_erasing_pair("concat")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    concrete = False
    concat = True

    def append(self, string, value):
        raise Exception("You cannot modify concatenated string")
        #lgt = len(target)
        #target.extend(['\x00'] * self.len(storage))
        #self.write_into(storage, target, lgt)

    def force(self, obj):
        s = ['\x00'] * self.len(obj.storage)
        self.write_into(obj.storage, s, 0)
        strategy = get_new_strategy(MutableStringStrategy)
        obj.storage = strategy.erase(s)
        obj.strategy = strategy

    def force_concatenate(self, obj):
        self.force(obj)

    def is_true(self, storage):
        # XXX recursion? figure out a way to flatten those easier
        left, right = self.unerase(storage)
        return (left.strategy.is_true(left.storage) or
                right.strategy.is_true(right.storage))

    def len(self, storage):
        l_one, l_two, lgt = self.unerase(storage)
        return lgt

    def repr(self, storage):
        return 'CON(%r)' % (self.unerase(storage),)

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