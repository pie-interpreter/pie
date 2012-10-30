from pie.objects.base import W_Root

class W_IntObject(W_Root):
    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return "W_IntObject(%s)" % self.value

    def int_w(self, space):
        return self.value

    def as_int(self):
        return self

    def as_string(self):
        from pie.objects.conststring import W_ConstStringObject
        return W_ConstStringObject(str(self.value))

    def as_bool(self):
        from pie.objects.bool import W_BoolObject
        return W_BoolObject(bool(self.value))

    def is_true(self):
        return self.value > 0

    def plus(self, number):
        return W_IntObject(self.value + number.value)

    def minus(self, number):
        return W_IntObject(self.value - number.value)

    def multiply(self, number):
        return W_IntObject(self.value * number.value)

    def mod(self, number):
        divider = number.value
        if self.value < 0 and divider:
            divider *= -1
        elif self.value and divider < 0:
            divider *= -1
        return W_IntObject(self.value % divider)