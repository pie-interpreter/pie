from pypy.rlib.rerased import new_erasing_pair
from pypy.rlib.objectmodel import specialize
import string

__author__ = 'sery0ga'

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
        return string.W_StringObject(self.unerase(obj.storage))

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

    def equal(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

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

    def equal(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

    def inplace_concat(self, space, storage, w_obj):
        l = self.unerase(storage)
        w_obj.strategy.append(w_obj.storage, l)

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

    def equal(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

    def force_concatenate(self, obj):
        self.unerase(obj.storage).force_concatenateenate()

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

    def force_concatenate(self, obj):
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