from pie.objects.base import W_Root
from pie.objects.int import W_IntObject

class W_BoolObject(W_Root):
    def __init__(self, value):
        self.value = bool(value)

    def __repr__(self):
        return "W_BoolObject(%s)" % self.value

    def as_int(self):
        return W_IntObject(int(self.value))

    def as_string(self):
        from pie.objects.conststring import W_ConstStringObject
        if self.value:
            return W_ConstStringObject('1')
        return W_ConstStringObject('')

    def as_bool(self):
        return self

    def is_true(self):
        return self.value

    def plus(self, number):
        return W_IntObject(int(self.value + number.value))

    def minus(self, number):
        return W_IntObject(int(self.value - number.value))

    def multiply(self, number):
        return W_IntObject(int(self.value * number.value))

    def mod(self, number):
        raise NotImplemented