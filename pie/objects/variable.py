from pie.objects.base import W_Root

__author__ = 'sery0ga'

class W_Variable(W_Root):

    def __init__(self, value):
        self.value = value

    def deref(self):
        return self.value.deref()

    def is_true(self):
        return self.value.is_true()

    def set_value(self, value):
        self.value = value
