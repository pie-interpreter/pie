from pypy.rlib.rerased import new_erasing_pair
from pypy.rlib.objectmodel import specialize
import string

__author__ = 'sery0ga'

cache = {}

@specialize.memo()
def get_new_strategy(strategy):
    """
    Helps to cache strategies' objects
    """
    try:
        return cache[strategy]
    except KeyError:
        new_strategy = strategy()
        cache[strategy] = new_strategy
        return new_strategy

class BaseStringStrategy(object):
    """
    This is an abstract strategy. No string object could be an instance of it
    """
    concat = False

    def copy(self, w_string):
        return string.W_StringObject.newcopiedstr(w_string)

    def force_concatenate(self, w_string):
        pass

class ConstantStringStrategy(BaseStringStrategy):
    """
    Basic strategy. By default all strings has it.

    You can't change a string with this strategy.

    String internal representation -- PYTHON's string
    """
    erase, unerase = new_erasing_pair("constant")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    concrete = True

    def append(self, w_string, value):
        raise Exception("You cannot change constant string")

    def conststr_w(self, w_string):
        return self.unerase(w_string.storage)

    def copy(self, obj):
        return string.W_StringObject(self.unerase(obj.storage))

    def equal(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

    def force_copy(self, w_source, w_dest_obj):
        w_dest_obj.storage = self.erase(self.unerase(w_source.storage)[:])

    def getitem(self, w_string, item):
        return self.unerase(w_string.storage)[item]

    def is_true(self, w_string):
        value = self.unerase(w_string.storage)
        if not value or value == "0":
            return False
        return True

    def len(self, w_string):
        return len(self.unerase(w_string.storage))

    def make_mutable(self, w_string):
        new_strategy = get_new_strategy(MutableStringStrategy)
        w_string.strategy = new_strategy
        w_string.storage = new_strategy.erase(
            [c for c in self.unerase(w_string.storage)]
        )

    def repr(self, w_string):
        return 'W_ConstantString(%s)' % self.unerase(w_string.storage)

    def setitem(self, w_string, item, value):
        raise Exception("You cannot change constant string")

    def str_w(self, w_string):
        return self.unerase(w_string.storage)

    def write_into(self, w_string, target, start):
        s = self.unerase(w_string.storage)
        i = 0
        for c in s:
            target[start + i] = c
            i += 1

class MutableStringStrategy(BaseStringStrategy):
    """
    A string got this strategy, if 'make_mutable' is called. It usually happens
    on some string operations.

    String internal representation -- PYTHON's list
    """
    erase, unerase = new_erasing_pair("mutable")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    concrete = True

    def append(self, string, value):
        raw_string = self.unerase(string.storage)
        raw_string.append(value)
        string.storage = self.erase(raw_string)

    def conststr_w(self, w_string):
        return ''.join(self.unerase(w_string.storage))

    def equal(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

    def force_copy(self, w_source, w_dest_obj):
        w_dest_obj.storage = self.erase(self.unerase(w_source.storage)[:])

    def getitem(self, w_string, item):
        return self.unerase(w_string.storage)[item]

    def is_true(self, w_string):
        value = self.unerase(w_string.storage)
        if not value or value == ['0']:
            return False
        return True

    def len(self, w_string):
        return len(self.unerase(w_string.storage))

    def make_mutable(self, w_string):
        pass

    def repr(self, w_string):
        return 'W_MutableString(%s)' % ''.join(self.unerase(w_string.storage))

    def setitem(self, w_string, item, val):
        self.unerase(w_string.storage)[item] = val

    def str_w(self, w_string):
        return "".join(self.unerase(w_string.storage))

    def write_into(self, w_string, target, start):
        s = self.unerase(w_string.storage)
        for i, c in enumerate(s):
            target[start + i] = c

class StringCopyStrategy(BaseStringStrategy):
    """
    If string A is copied, string B with this strategy is created. We make just
    a reference to original string without copying its content.

    String internal representation -- None, reference to original string object
    """
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

    def force(self, w_string):
        w_orig = self.unerase(w_string.storage)
        w_orig.force()
        w_string.strategy = w_orig.strategy
        w_orig.strategy.force_copy(w_orig, w_string)

    def getitem(self, w_string, index):
        w_parent = self.unerase(w_string.storage)
        return w_parent.strategy.getitem(w_parent, index)

    def is_true(self, w_string):
        parent = self.unerase(w_string.storage)
        return parent.strategy.is_true(parent)

    def len(self, w_string):
        w_parent = self.unerase(w_string.storage)
        return w_parent.strlen()

    def repr(self, w_string):
        return 'W_CopiedString(%r)' % self.unerase(w_string.storage)

    def write_into(self, w_string, target, start):
        parent = self.unerase(w_string.storage)
        parent.write_into(target, start)

class StringConcatStrategy(BaseStringStrategy):
    """
    On string concatenation, we create a resulted string with this strategy
    is created. The string contains references to both concatenating but doesn't
    do any real operation until last possible moment (when force() is called)
    """
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

    def force(self, w_string):
        new_storage = ['\x00'] * self.len(w_string)
        self.write_into(w_string, new_storage, 0)
        strategy = get_new_strategy(MutableStringStrategy)
        w_string.storage = strategy.erase(new_storage)
        w_string.strategy = strategy

    def force_concatenate(self, obj):
        self.force(obj)

    def is_true(self, w_string):
        # XXX recursion? figure out a way to flatten those easier
        left, right = self.unerase(w_string.storage)
        return (left.strategy.is_true(left) or
                right.strategy.is_true(right))

    def len(self, w_string):
        l_one, l_two, lgt = self.unerase(w_string.storage)
        return lgt

    def repr(self, w_string):
        return 'W_ConcatenatedString(%r)' % (self.unerase(w_string.storage),)

    def write_into(self, w_string, target, start):
        l_one, l_two, lgt = self.unerase(w_string.storage)
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