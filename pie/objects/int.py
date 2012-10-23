from pie.objects.base import W_Root

class W_IntObject(W_Root):
    _immutable_fields_ = ['intval']

    def __init__(self, intval):
        self.intval = intval

    def int_w(self, space):
        return self.intval

    def copy(self, space):
        return self # immutable object

    def as_number(self, space):
        return self

    def to_string(self):
        return str(self.intval)
