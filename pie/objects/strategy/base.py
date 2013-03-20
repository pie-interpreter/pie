from rpython.rlib.objectmodel import instantiate
from rpython.rlib.objectmodel import specialize

import pie.objects.string

__author__ = 'sery0ga'

cache = {}


@specialize.memo()
def get_string_strategy(strategy):
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
    def constant_str(strval):
        return pie.objects.string.W_String(strval)

    @staticmethod
    def mutable_str(strval):
        w_s = instantiate(pie.objects.string.W_String)
        from pie.objects.strategy.general import MutableStringStrategy
        strategy = get_string_strategy(MutableStringStrategy)
        w_s.storage = strategy.erase(strval)
        w_s.strategy = strategy
        w_s.copies = None
        return w_s

    @staticmethod
    def copied_str(w_original_string):
        w_s = instantiate(pie.objects.string.W_String)
        from pie.objects.strategy.reference import StringCopyStrategy
        strategy = get_string_strategy(StringCopyStrategy)
        w_s.storage = strategy.erase(w_original_string)
        w_s.strategy = strategy
        w_s.copies = None
        return w_s

    @staticmethod
    def concat_str(w_left, w_right):
        w_string = instantiate(pie.objects.string.W_String)
        from pie.objects.strategy.reference import StringConcatStrategy
        strategy = get_string_strategy(StringConcatStrategy)
        w_string.storage = strategy.erase((w_left, w_right, w_left.strlen() +
                                                      w_right.strlen()))
        w_string.strategy = strategy
        w_string.copies = None
        w_left.add_copy(w_string)
        w_right.add_copy(w_string)
        return w_string


class BaseStringStrategy(object):
    """
    This is an abstract strategy. No string object could be an instance of it
    """
    def copy(self, w_string):
        return StringFactory.copied_str(w_string)

    def is_true(self, w_string):
        raise NotImplementedError

    def len(self, w_string):
        raise NotImplementedError

    def getitem(self, w_string, item):
        raise NotImplementedError

    def equal(self, w_obj, w_other):
        raise NotImplementedError

    def make_integral(self, w_string):
        raise NotImplementedError

    def write_into_list(self, w_string, target, start):
        raise NotImplementedError


class GeneralStringStrategy(BaseStringStrategy):
    """
    Basically, this strategy means that we grab content of string directly from storage,
        without any additional actions
    """
    def dereference(self, w_string):
        """
        Switches object strategy from reference one to general one
        """
        pass

    def make_integral(self, w_string):
        """ Integral by definition """
        pass

    def append(self, w_string, value):
        raise NotImplementedError

    def hard_copy(self, w_source, w_dest_obj):
        raise NotImplementedError

    def make_mutable(self, w_string):
        raise NotImplementedError

    def setitem(self, w_string, item, value):
        raise NotImplementedError


class ReferenceStringStrategy(BaseStringStrategy):

    def dereference(self, w_string):
        """
        Switches object strategy from 'reference' one to 'general' one
        """
        raise NotImplementedError

    def make_integral(self, w_string):
        raise NotImplementedError
