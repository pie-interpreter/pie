from pie.objects.base import W_Root

class W_IntObject(W_Root):
    def __init__(self, intval):
        self.intval = int(intval)

    def __repr__(self):
        return "W_IntObject(%s)" % self.intval

    def int_w(self, space):
        return self.intval

    def as_int(self):
        return self

    def as_string(self):
        from pie.objects.conststring import W_ConstStringObject
        return W_ConstStringObject(str(self.intval))

    def less(self, object):
        from pie.objects.bool import W_BoolObject
        if self.intval < object.intval:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def more(self, object):
        from pie.objects.bool import W_BoolObject
        if self.intval > object.intval:
            return W_BoolObject(True)
        else:
            return W_BoolObject(False)

    def is_true(self):
        return self.intval > 0

    def plus(self, number):
        return W_IntObject(self.intval + number.intval)

    def minus(self, number):
        return W_IntObject(self.intval - number.intval)

    def multiply(self, number):
        return W_IntObject(self.intval * number.intval)

    def mod(self, number):
        divider = number.intval
        if self.intval < 0 and divider > 0:
            divider *= -1
        elif self.intval > 0 and divider < 0:
            divider *= -1
        return W_IntObject(self.intval % divider)