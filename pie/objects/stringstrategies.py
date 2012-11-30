from pypy.rlib.rerased import new_erasing_pair
from pypy.rlib.objectmodel import specialize
from pypy.rlib.objectmodel import instantiate
from pie.error import InterpreterError
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

class StringFactory(object):

    @staticmethod
    def str(strval):
        return string.W_StringObject(strval)

    @staticmethod
    def mutable_str(strval):
        w_s = instantiate(string.W_StringObject)
        strategy = get_new_strategy(MutableStringStrategy)
        w_s.storage = strategy.erase(strval)
        w_s.strategy = strategy
        w_s.copies = None
        return w_s

    @staticmethod
    def newcopiedstr(origobj):
        w_s = instantiate(string.W_StringObject)
        strategy = get_new_strategy(StringCopyStrategy)
        w_s.copies = None
        w_s.storage = strategy.erase(origobj)
        w_s.strategy = strategy
        return w_s

    @staticmethod
    def newstrconcat(origobj, other):
        w_s = instantiate(string.W_StringObject)
        strategy = get_new_strategy(StringConcatStrategy)
        w_s.copies = None
        w_s.storage = strategy.erase((origobj, other, origobj.strlen() +
                                                      other.strlen()))
        w_s.strategy = strategy
        origobj.add_copy(w_s)
        other.add_copy(w_s)
        return w_s


class BaseStringStrategy(object):
    """
    This is an abstract strategy. No string object could be an instance of it
    """
    def copy(self, w_string):
        return StringFactory.newcopiedstr(w_string)

    def is_true(self, w_string):
        raise InterpreterError("Not implemented")

    def force_concatenate(self, w_string):
        pass

class BaseConcreteStringStrategy(BaseStringStrategy):
    """
    Basically, concrete strategy means that we grab content of string directly from storage,
        without any additional actions
    """
    def make_concrete(self, w_string):
        pass

    def make_mutable(self, w_string):
        raise InterpreterError("Not implemented")

class ConstantStringStrategy(BaseConcreteStringStrategy):
    """
    Basic strategy. By default all strings has it.

    You can't change a string with this strategy.

    String internal representation -- PYTHON's string
    """
    erase, unerase = new_erasing_pair("constant")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    def repr(self, w_string):
        return 'ConstantString(%s)' % self.str_w(w_string)

    def is_true(self, w_string):
        value = self.unerase(w_string.storage)
        if not value or value == "0":
            return False
        return True

    def len(self, w_string):
        return len(self.unerase(w_string.storage))

    def str_w(self, w_string):
        return self.unerase(w_string.storage)


    def getitem(self, w_string, item):
        return self.unerase(w_string.storage)[item]

    def setitem(self, w_string, item, value):
        raise InterpreterError("You cannot modify constant string")


    def append(self, w_string, value):
        raise InterpreterError("You cannot modify constant string")

    def equal(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

    def force_copy(self, w_source, w_dest_obj):
        # w_dest_obj.storage = self.erase(self.unerase(w_source.storage)[:])
        w_dest_obj.storage = self.erase(self.unerase(w_source.storage))

    def make_mutable(self, w_string):
        new_strategy = get_new_strategy(MutableStringStrategy)
        w_string.strategy = new_strategy
        w_string.storage = new_strategy.erase(
            [c for c in self.unerase(w_string.storage)]
        )

    def write_into(self, w_string, target, start):
        s = self.unerase(w_string.storage)
        i = 0
        for c in s:
            target[start + i] = c
            i += 1

class MutableStringStrategy(BaseConcreteStringStrategy):
    """
    A string got this strategy, if 'make_mutable' is called. It usually happens
    on some string operations.

    String internal representation -- PYTHON's list
    """
    erase, unerase = new_erasing_pair("mutable")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    def repr(self, w_string):
        return 'MutableString(%s)' % self.str_w(w_string)

    def str_w(self, w_string):
        return ''.join(self.unerase(w_string.storage))

    def is_true(self, w_string):
        value = self.unerase(w_string.storage)
        if not value or value == ['0']:
            return False
        return True

    def len(self, w_string):
        return len(self.unerase(w_string.storage))


    def getitem(self, w_string, item):
        return self.unerase(w_string.storage)[item]

    def setitem(self, w_string, item, val):
        self.unerase(w_string.storage)[item] = val


    def make_mutable(self, w_string):
        pass


    def append(self, string, value):
        raw_string = self.unerase(string.storage)
        raw_string.append(value)
        string.storage = self.erase(raw_string)

    def equal(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

    def force_copy(self, w_source, w_dest_obj):
        w_dest_obj.storage = self.erase(self.unerase(w_source.storage)[:])

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

    def repr(self, w_string):
        return 'CopiedString(%r)' % self.unerase(w_string.storage)

    def is_true(self, w_string):
        parent = self.unerase(w_string.storage)
        return parent.strategy.is_true(parent)

    def len(self, w_string):
        w_parent = self.unerase(w_string.storage)
        return w_parent.strlen()


    def getitem(self, w_string, index):
        w_parent = self.unerase(w_string.storage)
        return w_parent.strategy.getitem(w_parent, index)

    def setitem(self, w_string, item, value):
        raise InterpreterError("You cannot modify copied string")


    def make_concrete(self, w_string):
        w_orig = self.unerase(w_string.storage)
        w_orig.make_concrete()
        w_string.strategy = w_orig.strategy
        w_orig.strategy.force_copy(w_orig, w_string)


    def append(self, string, value):
        #TODO: fix it
        raise InterpreterError("You cannot modify copied string")

    def equal(self, w_left, w_right):
        return self.unerase(w_left.storage) == self.unerase(w_right.storage)

    def force_concatenate(self, obj):
        self.unerase(obj.storage).force_concatenate()

    def write_into(self, w_string, target, start):
        parent = self.unerase(w_string.storage)
        parent.write_into(target, start)

class StringConcatStrategy(BaseStringStrategy):
    """
    On string concatenation, we create a resulted string with this strategy
    is created. The string contains references to both concatenating but doesn't
    do any real operation until last possible moment (when make_concrete() is called)
    """
    erase, unerase = new_erasing_pair("concat")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    def repr(self, w_string):
        return 'ConcatenatedString(%r)' % (self.unerase(w_string.storage),)

    def is_true(self, w_string):
        # XXX recursion? figure out a way to flatten those easier
        left, right = self.unerase(w_string.storage)
        return (left.strategy.is_true(left) or
                right.strategy.is_true(right))

    def len(self, w_string):
        l_one, l_two, lgt = self.unerase(w_string.storage)
        return lgt


    def make_concrete(self, w_string):
        new_storage = ['\x00'] * self.len(w_string)
        self.write_into(w_string, new_storage, 0)
        strategy = get_new_strategy(MutableStringStrategy)
        w_string.storage = strategy.erase(new_storage)
        w_string.strategy = strategy


    def append(self, string, value):
        #lgt = len(target)
        #target.extend(['\x00'] * self.len(storage))
        #self.write_into(storage, target, lgt)
        raise InterpreterError("You cannot modify concatenated string")

    def force_concatenate(self, obj):
        self.make_concrete(obj)

    def write_into(self, w_string, target, start):
        l_one, l_two, lgt = self.unerase(w_string.storage)
        l_one.write_into(target, start)
        l_two.write_into(target, start + l_one.strlen())
