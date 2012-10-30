from pie.objects.bool import W_BoolObject
from pie.objects.conststring import W_ConstStringObject, NotConvertibleToNumber
from pie.objects.int import W_IntObject

__author__ = 'sery0ga'

class ObjSpace(object):

    (w_int, w_str, w_bool, w_array, w_null, w_object, w_resource) = range(7)

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
        type = self.get_common_arithmetic_type(w_left, w_right)
        if type == self.w_int:
            return w_left.as_int().plus(w_right.as_int())
        else:
            return w_left.as_number().plus(w_right.as_number())

    def minus(self, w_left, w_right):
        """
        In PHP '-' is supported only for numbers
        """
        type = self.get_common_arithmetic_type(w_left, w_right)
        if type == self.w_int:
            return w_left.as_int().minus(w_right.as_int())
        else:
            return w_left.as_number().minus(w_right.as_number())

    def multiply(self, w_left, w_right):
        """
        In PHP '*' is supported only for numbers
        """
        type = self.get_common_arithmetic_type(w_left, w_right)
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
        type = self.get_common_arithmetic_type(w_left, w_right)
        if type == self.w_int:
            return w_left.as_int().mod(w_right.as_int())
        raise NotImplementedError

    def concatenate(self, w_left, w_right):
        return w_left.as_string().concatenate(w_right.as_string())

    def less_than(self, w_left, w_right):
        name = 'less_than'
        type = self.get_common_comparison_type(w_left, w_right)
        if type == self.w_str:
            try:
                return getattr(w_left.as_int_strict(), name)(w_right.as_int_strict())
            except NotConvertibleToNumber:
                return getattr(w_left, name)(w_right)
        elif type == self.w_int:
            return getattr(w_left.as_int(), name)(w_right.as_int())
        elif type == self.w_bool:
            return getattr(w_left.as_bool(), name)(w_right.as_bool())

    def more_than(self, w_left, w_right):
        name = 'more_than'
        type = self.get_common_comparison_type(w_left, w_right)
        if type == self.w_str:
            try:
                return getattr(w_left.as_int_strict(), name)(w_right.as_int_strict())
            except NotConvertibleToNumber:
                return getattr(w_left, name)(w_right)
        elif type == self.w_int:
            return getattr(w_left.as_int(), name)(w_right.as_int())
        elif type == self.w_bool:
            return getattr(w_left.as_bool(), name)(w_right.as_bool())

    def equal(self, w_left, w_right):
        name = 'equal'
        type = self.get_common_comparison_type(w_left, w_right)
        if type == self.w_str:
            try:
                return getattr(w_left.as_int_strict(), name)(w_right.as_int_strict())
            except NotConvertibleToNumber:
                return getattr(w_left, name)(w_right)
        elif type == self.w_int:
            return getattr(w_left.as_int(), name)(w_right.as_int())
        elif type == self.w_bool:
            return getattr(w_left.as_bool(), name)(w_right.as_bool())

    def get_common_comparison_type(self, w_left, w_right):
        """ Use this function only in comparison operations (like '>' or '<=')
        """
        left_type = w_left.type
        if left_type == self.w_str and w_right.type == self.w_int:
            """
            http://www.php.net/manual/en/language.operators.comparison.php

            If you compare a number with a string or the comparison involves numerical strings,
            then each string is converted to a number and the comparison performed numerically
            """
            return self.w_int
        return w_left.type

    def get_common_arithmetic_type(self, w_left, w_right):
        """ Use this function only in arithmetic operations (like '-' or '+')
        """
        left_type = w_left.type
        right_type = w_right.type
        return self.w_int

W_IntObject.type = ObjSpace.w_int
W_ConstStringObject.type = ObjSpace.w_str
W_BoolObject.type = ObjSpace.w_bool