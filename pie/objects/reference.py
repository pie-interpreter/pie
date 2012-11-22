from pie.objects.root import W_Root

class W_Reference(W_Root):

    def __init__(self, w_variable):
        self.variable = w_variable

    def deref(self):
        return self.variable.deref()
