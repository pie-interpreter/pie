from pypy.rlib.rerased import new_erasing_pair

from pie.objects.strategy.base import ReferenceStringStrategy, get_string_strategy
from pie.objects.strategy.general import MutableStringStrategy

__author__ = 'sery0ga'

class StringCopyStrategy(ReferenceStringStrategy):
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
        return parent.is_true()

    def str_w(self, w_string):
        parent = self.unerase(w_string.storage)
        return parent.str_w()

    def len(self, w_string):
        w_parent = self.unerase(w_string.storage)
        return w_parent.strlen()

    def dereference(self, w_string):
        """
        Switches object strategy from reference one to general one
        """
        parent = self.unerase(w_string.storage)
        strategy = parent.strategy

        strategy.dereference(parent)
        w_string.strategy = strategy
        strategy.hard_copy(parent, w_string)

    def make_integral(self, w_string):
        self.unerase(w_string.storage).make_integral()

    def write_into_list(self, w_string, target_list, start):
        parent = self.unerase(w_string.storage)
        parent.strategy.write_into_list(parent, target_list, start)

    def getitem(self, w_string, index):
        w_parent = self.unerase(w_string.storage)
        return w_parent.strategy.getitem(w_parent, index)

    def equal(self, w_left, w_right):
        return self.unerase(w_left.storage) == self.unerase(w_right.storage)


class StringConcatStrategy(ReferenceStringStrategy):
    """
    On string concatenation, we create a resulted string with this strategy
    is created. The string contains references to both concatenating but doesn't
    do any real operation until last possible moment (when dereference() is called)
    """
    erase, unerase = new_erasing_pair("concat")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    def repr(self, w_string):
        return 'ConcatenatedString(%r)' % (self.unerase(w_string.storage),)

    def len(self, w_string):
        left, right, length = self.unerase(w_string.storage)
        return length

    def dereference(self, w_string):
        """
        Switches object strategy from reference one to general one
        """
        new_storage = ['\x00'] * self.len(w_string)
        self.write_into_list(w_string, new_storage, 0)
        strategy = get_string_strategy(MutableStringStrategy)
        w_string.storage = strategy.erase(new_storage)
        w_string.strategy = strategy

    def make_integral(self, w_string):
        self.dereference(w_string)

    def write_into_list(self, w_string, target_list, start):
        current, left_visited, right_visited = (w_string, False, False)
        stack = []
        current_position = start
        while(True):
            left, right, unused = self.unerase(current.storage)
            if not left_visited:
                if isinstance(left.strategy, StringConcatStrategy):
                    stack.append((current, True, False))
                    current = left
                    continue
                else:
                    left.strategy.write_into_list(left, target_list, current_position)
                    current_position += left.strlen()
            if not right_visited:
                if isinstance(right.strategy, StringConcatStrategy):
                    stack.append((current, True, True))
                    current = right
                    continue
                else:
                    right.strategy.write_into_list(right, target_list, current_position)
                    current_position += right.strlen()
            if not stack:
                break
            current, left_visited, right_visited = stack.pop()
