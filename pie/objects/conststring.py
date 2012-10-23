from pie.objects.base import W_Root

class W_ConstStringObject(W_Root):

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.val
