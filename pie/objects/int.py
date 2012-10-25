from pie.objects.base import W_Root

class W_IntObject(W_Root):
    def __init__(self, intval):
        self.intval = int(intval)

    def __repr__(self):
        return "W_IntObject(%s)" % self.intval

    def int_w(self, space):
        return self.intval

    def str_w(self):
        return str(self.intval)

    def as_int(self):
        return self

    def as_string(self):
        from pie.objects.conststring import W_ConstStringObject
        return W_ConstStringObject(str(self.intval))

    def less(self, object):
        if self.intval < object.intval:
            return W_IntObject(1)
        else:
            return W_IntObject(0)

    def more(self, object):
        if self.intval > object.intval:
            return W_IntObject(1)
        else:
            return W_IntObject(0)

    def is_true(self):
        return self.intval > 0

    def plus(self, number):
        return W_IntObject(self.intval + number.intval)

    def minus(self, number):
        return W_IntObject(self.intval - number.intval)

    def multiply(self, number):
        return W_IntObject(self.intval * number.intval)