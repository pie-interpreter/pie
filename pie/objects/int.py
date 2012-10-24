from pie.objects.base import W_Root

class W_IntObject(W_Root):
    def __init__(self, intval):
        self.intval = int(intval)

    def __repr__(self):
        return str(self.intval)

    def int_w(self, space):
        return self.intval

    def copy(self, space):
        return self # immutable object

    def as_number(self, space):
        return self

    def to_string(self):
        return str(self.intval)

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
