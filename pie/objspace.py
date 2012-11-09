from pie.objects.bool import W_BoolObject
from pie.objects.float import W_FloatObject
from pie.objects.string import W_StringObject, NotConvertibleToNumber
from pie.objects.int import W_IntObject
from distutils.errors import CompileError

__author__ = 'sery0ga'

class ObjSpace(object):

    (w_int, w_float, w_str, w_bool, w_array, w_null, w_object, w_resource) = range(8)

    def int(self, value):
        return W_IntObject(value)

    def str(self, value):
        return W_StringObject(value)

    def bool(self, value):
        return W_BoolObject(value)

    def float(self, value):
        raise CompileError, "Not implemented"

    def null(self):
        raise CompileError, "Not implemented"

    def add(self, w_left, w_right):
        """
        In PHP '+' is supported only for numbers and arrays
        """
        left_number = w_left.as_number()
        right_number = w_right.as_number()
        type = self.get_common_arithmetic_type(left_number, right_number)
        if type == self.w_int:
            return left_number.as_int().plus(right_number.as_int())
        else:
            return left_number.as_float().plus(right_number.as_float())

    def substract(self, w_left, w_right):
        """
        In PHP '-' is supported only for numbers
        """
        left_number = w_left.as_number()
        right_number = w_right.as_number()
        type = self.get_common_arithmetic_type(left_number, right_number)
        if type == self.w_int:
            return left_number.as_int().minus(right_number.as_int())
        else:
            return left_number.as_float().minus(right_number.as_float())

    def multiply(self, w_left, w_right):
        """
        In PHP '*' is supported only for numbers
        """
        left_number = w_left.as_number()
        right_number = w_right.as_number()
        type = self.get_common_arithmetic_type(left_number, right_number)
        if type == self.w_int:
            return left_number.as_int().multiply(right_number.as_int())
        else:
            return left_number.as_float().multiply(right_number.as_float())

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

    def concat(self, w_left, w_right):
        return w_left.copy().as_string().concatenate(w_right.as_string())

    def identical(self, w_left, w_right):
        if w_left.type != w_right.type:
            return W_BoolObject(False)
        return w_left.equal(w_right)

    def not_identical(self, w_left, w_right):
        if w_left.type != w_right.type:
            return W_BoolObject(True)
        return w_left.not_equal(w_right)

    def get_common_comparison_type(self, w_left, w_right):
        """ Use this function only in comparison operations (like '>' or '<=')
        """
        left_type = w_left.type
        if self._is_any_number(left_type, w_right.type) and self._is_any_string(left_type, w_right.type):
            """
            http://www.php.net/manual/en/language.operators.comparison.php

            If you compare a number with a string or the comparison involves numerical strings,
            then each string is converted to a number and the comparison performed numerically
            """
            return self.w_float
        elif left_type == self.w_int and w_right.type == self.w_float:
            return self.w_float
        return w_left.type

    def get_common_arithmetic_type(self, w_left, w_right):
        """ Use this function only in arithmetic operations (like '-' or '+')
        """
        if self._is_any_float(w_left.type, w_right.type):
            return self.w_float
        return self.w_int

    def _is_any_number(self, left_type, right_type):
        if left_type == self.w_int or right_type == self.w_int \
            or self._is_any_float(left_type, right_type):
            return True
        return False

    def _is_any_float(self, left_type, right_type):
        if left_type == self.w_float or right_type == self.w_float:
            return True
        return False

    def _is_any_string(self, left_type, right_type):
        if left_type == self.w_str or right_type == self.w_str:
            return True
        return False

def _new_comparison_op(name):
    def func(self, w_left, w_right):
        type = self.get_common_comparison_type(w_left, w_right)
        if type == self.w_str:
            try:
                left_number = w_left.as_number_strict()
                right_number = w_right.as_number_strict()
                if self._is_any_float(left_number.type, right_number.type):
                    return getattr(left_number.as_float(), name)(right_number.as_float())
                return getattr(left_number, name)(right_number)
            except NotConvertibleToNumber:
                return getattr(w_left, name)(w_right)
        elif type == self.w_int:
            return getattr(w_left.as_int(), name)(w_right.as_int())
        elif type == self.w_float:
            return getattr(w_left.as_float(), name)(w_right.as_float())
        elif type == self.w_bool:
            return getattr(w_left.as_bool(), name)(w_right.as_bool())
    func.func_name = name
    return func

for _name in ['less_than', 'more_than', 'equal', 'not_equal', 'less_than_or_equal', 'more_than_or_equal']:
    setattr(ObjSpace, _name, _new_comparison_op(_name))

W_IntObject.type = ObjSpace.w_int
W_StringObject.type = ObjSpace.w_str
W_BoolObject.type = ObjSpace.w_bool
W_FloatObject.type = ObjSpace.w_float
space = ObjSpace()