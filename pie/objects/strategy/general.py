from pypy.rlib.rerased import new_erasing_pair
from pie.objects.strategy.base import GeneralStringStrategy, get_string_strategy

__author__ = 'sery0ga'


class ConstantStringStrategy(GeneralStringStrategy):
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
        assert False, "You cannot modify constant string"

    def append(self, w_string, value):
        assert False, "You cannot modify constant string"

    def equal(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

    def hard_copy(self, w_source, w_dest_obj):
        w_dest_obj.storage = self.erase(self.unerase(w_source.storage))

    def make_mutable(self, w_string):
        new_strategy = get_string_strategy(MutableStringStrategy)
        w_string.strategy = new_strategy
        w_string.storage = new_strategy.erase(
            [c for c in self.unerase(w_string.storage)]
        )

    def write_into_list(self, w_string, target_list, start):
        s = self.unerase(w_string.storage)
        i = 0
        for c in s:
            target_list[start + i] = c
            i += 1


class MutableStringStrategy(GeneralStringStrategy):
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

    def append(self, string, value):
        raw_string = self.unerase(string.storage)
        raw_string.append(value)
        string.storage = self.erase(raw_string)

    def getitem(self, w_string, item):
        return self.unerase(w_string.storage)[item]

    def setitem(self, w_string, item, value):
        self.unerase(w_string.storage)[item] = value

    def make_mutable(self, w_string):
        pass

    def equal(self, w_obj, w_other):
        return self.unerase(w_obj.storage) == self.unerase(w_other.storage)

    def hard_copy(self, w_source, w_dest_obj):
        w_dest_obj.storage = self.erase(self.unerase(w_source.storage)[:])

    def write_into_list(self, w_string, target_list, start):
        s = self.unerase(w_string.storage)
        for i, c in enumerate(s):
            target_list[start + i] = c
