from pie.objects.base import W_Root
from pie.objects.int import W_IntObject

class W_ConstStringObject(W_Root):

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.val

    def str_w(self):
        return self.val

    def as_int(self):
        if not self.val:
            return W_IntObject(0)
        begin = 0
        end = 0
        minus = 1
        if self.val[0] == '-':
            begin += 1
            end += 1
            minus = -1
        while end < len(self.val):
            if self.val[end] < '0' or self.val[end] > '9':
                break
            end += 1
        if minus and end == 0:
            return W_IntObject(0)
        elif minus == -1 and end == 1:
            return W_IntObject(0)
        return W_IntObject(int(self.val[begin:end]) * minus)