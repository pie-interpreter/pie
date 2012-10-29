from pie.objects.bool import W_BoolObject
from pie.objects.conststring import W_ConstStringObject
from pie.objects.int import W_IntObject

__author__ = 'sery0ga'

class ObjSpace(object):

    (w_int, w_str, w_bool, w_array) = range(4)

    def int(self, value):
        return W_IntObject(value)

    def str(self, value):
        return W_ConstStringObject(value)

    def bool(self, value):
        return W_BoolObject(value)

    def plus(self, w_left, w_right):
        """
        In PHP '+' is supported only for numbers and arrays
        """
        type = self.get_common_type(w_left, w_right)
        if type == self.w_int:
            return w_left.as_int().plus(w_right.as_int())
        else:
            return w_left.as_number().plus(w_right.as_number())

    def minus(self, w_left, w_right):
        """
        In PHP '-' is supported only for numbers
        """
        type = self.get_common_type(w_left, w_right)
        if type == self.w_int:
            return w_left.as_int().minus(w_right.as_int())
        else:
            return w_left.as_number().minus(w_right.as_number())

    def multiply(self, w_left, w_right):
        """
        In PHP '*' is supported only for numbers
        """
        type = self.get_common_type(w_left, w_right)
        if type == self.w_int:
            return w_left.as_int().multiply(w_right.as_int())
        else:
            return w_left.as_number().minus(w_right.as_number())

    def divide(self, w_left, w_right):
        """
        In PHP '*' is supported only for numbers
        """
        raise NotImplementedError

    def mod(self, w_left, w_right):
        """
        In PHP '%' is supported only for numbers
        """
        type = self.get_common_type(w_left, w_right)
        if type == self.w_int:
            return w_left.as_int().mod(w_right.as_int())
        raise NotImplementedError

    def concatenate(self, w_left, w_right):
        return w_left.as_string().concatenate(w_right.as_string())

    def get_common_type(self, w_left, w_right):
        left_type = w_left.type
        right_type = w_right.type
        if left_type == right_type:
            return left_type
        elif left_type == self.w_int or right_type == self.w_int:
            return self.w_int
        else:
            raise NotImplementedError

W_IntObject.type = ObjSpace.w_int
W_ConstStringObject.type = ObjSpace.w_str
W_BoolObject.type = ObjSpace.w_bool