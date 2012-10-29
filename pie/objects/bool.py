from pie.objects.base import W_Root
from pie.objects.int import W_IntObject

class W_BoolObject(W_Root):
    def __init__(self, boolval):
        self.boolval = bool(boolval)

    def __repr__(self):
        return "W_BoolObject(%s)" % self.boolval

    def as_int(self):
        return W_IntObject(int(self.boolval))

    def as_string(self):
        from pie.objects.conststring import W_ConstStringObject
        if self.boolval:
            return W_ConstStringObject('1')
        return W_ConstStringObject('')

    def as_bool(self):
        return self

    def less(self, object):
        if self.boolval < object.boolval:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more(self, object):
        if self.boolval > object.boolval:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def is_true(self):
        return self.boolval

    def plus(self, number):
        return W_IntObject(int(self.boolval + number.boolval))

    def minus(self, number):
        return W_IntObject(int(self.boolval - number.boolval))

    def multiply(self, number):
        return W_IntObject(int(self.boolval * number.boolval))

    def mod(self, number):
        raise NotImplemented