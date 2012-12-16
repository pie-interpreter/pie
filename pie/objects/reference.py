from pie.objects.base import W_Root


class W_Variable(W_Root):

    def __init__(self, value):
        self.value = value

    def deref(self):
        return self.value.deref()

    def is_true(self):
        return self.value.is_true()

    def set_value(self, value):
        if isinstance(self.value, W_Reference):
            self.value.set_value(value)
        else:
            self.value = value


class W_Reference(W_Root):

    def __init__(self, value):
        assert isinstance(value, W_Variable)
        self.value = value

    def deref(self):
        return self.value.deref()

    def is_true(self):
        return self.value.is_true()

    def set_value(self, value):
        self.value.set_value(value)
