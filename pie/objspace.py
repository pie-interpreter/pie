from pie.objects.null import W_NullObject
from pie.objects.bool import W_BoolObject
from pie.objects.float import W_FloatObject
from pie.objects.string import W_StringObject, NotConvertibleToNumber
from pie.objects.int import W_IntObject
from pie.objects.variable import W_Variable

__author__ = 'sery0ga'


class ObjSpace(object):

    (w_int, w_float, w_str, w_bool, w_null) = range(5)

    def int(self, value):
        return W_IntObject(value)

    def str(self, value):
        return W_StringObject(value)

    def bool(self, value):
        return W_BoolObject(value)

    def float(self, value):
        return W_FloatObject(value)

    def null(self):
        return W_NullObject()

    def variable(self, w_object):
        if isinstance(w_object, W_Variable):
            return W_Variable(w_object.value)
        return W_Variable(w_object)

    def add(self, w_left, w_right):
        """
        In PHP '+' is supported only for numbers and arrays
        """
        #TODO: add array support
        left_number = w_left.deref().as_number()
        right_number = w_right.deref().as_number()
        type = self.get_common_arithmetic_type(left_number, right_number)
        if type == self.w_int:
            return left_number.as_int().plus(right_number.as_int())
        else:
            return left_number.as_float().plus(right_number.as_float())

    def substract(self, w_left, w_right):
        """
        In PHP '-' is supported only for numbers
        """
        left_number = w_left.deref().as_number()
        right_number = w_right.deref().as_number()
        type = self.get_common_arithmetic_type(left_number, right_number)
        if type == self.w_int:
            return left_number.as_int().minus(right_number.as_int())
        else:
            return left_number.as_float().minus(right_number.as_float())

    def multiply(self, w_left, w_right):
        """
        In PHP '*' is supported only for numbers
        """
        left_number = w_left.deref().as_number()
        right_number = w_right.deref().as_number()
        type = self.get_common_arithmetic_type(left_number, right_number)
        if type == self.w_int:
            return left_number.as_int().multiply(right_number.as_int())
        else:
            return left_number.as_float().multiply(right_number.as_float())

    def divide(self, w_left, w_right):
        """
        In PHP '*' is supported only for numbers
        """
        left_number = w_left.deref().as_number()
        right_number = w_right.deref().as_number()
        type = self.get_common_arithmetic_type(left_number, right_number)
        if type == self.w_int:
            return left_number.as_int().divide(right_number.as_int())
        else:
            return left_number.as_float().divide(right_number.as_float())

    def mod(self, w_left, w_right):
        """
        In PHP '%' is supported only for integers
        """
        return w_left.deref().as_int().mod(w_right.deref().as_int())

    def concat(self, w_left, w_right):
        w_left = w_left.deref()
        w_right = w_right.deref()
        return w_left.as_string().concatenate(w_right.as_string())

    def identical(self, w_left, w_right):
        if w_left.deref().type != w_right.deref().type:
            return W_BoolObject(False)
        return w_left.deref().equal(w_right.deref())

    def not_identical(self, w_left, w_right):
        if w_left.deref().type != w_right.deref().type:
            return W_BoolObject(True)
        return w_left.deref().not_equal(w_right.deref())

    def is_empty(self, w_object):
        return W_BoolObject(not w_object.deref().is_true())

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
            """
            http://www.php.net/manual/en/language.types.type-juggling.php

             If either operand is a float, then both operands are evaluated as floats,
             and the result will be a float
            """
            return self.w_float
        elif left_type == self.w_null and w_right.type == self.w_str:
            """
            http://www.php.net/manual/en/language.operators.comparison.php

            Table "Comparison with Various Types", line 1
            Convert NULL to "", numerical or lexical comparison
            """
            return self.w_str
        elif left_type == self.w_null and w_right.type != self.w_null:
            """
            http://www.php.net/manual/en/language.operators.comparison.php

            Table "Comparison with Various Types", line 2
            Convert to bool, FALSE < TRUE
            """
            return self.w_bool
        elif left_type == self.w_bool:
            return self.w_bool
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
        w_left = w_left.deref()
        w_right = w_right.deref()
        type = self.get_common_comparison_type(w_left, w_right)
        if type == self.w_str:
            try:
                if w_left.type == self.w_null:
                    return getattr(w_left.as_string(), name)(w_right)
                left_number = w_left.as_number_strict()
                right_number = w_right.as_number_strict()
                if self._is_any_float(left_number.type, right_number.type):
                    return getattr(left_number.as_float(), name)(right_number.as_float())
                assert isinstance(left_number, W_IntObject)
                return getattr(left_number, name)(right_number)
            except NotConvertibleToNumber:
                return getattr(w_left, name)(w_right)
        elif type == self.w_int:
            return getattr(w_left.as_int(), name)(w_right.as_int())
        elif type == self.w_float:
            return getattr(w_left.as_float(), name)(w_right.as_float())
        elif type == self.w_bool:
            return getattr(w_left.as_bool(), name)(w_right.as_bool())
        elif type == self.w_null:
            # this is possible only if both arguments are null
            return getattr(w_left, name)(w_right)

        raise NotImplementedError

    func.func_name = name
    return func

for _name in ['less_than', 'more_than', 'equal', 'not_equal',
              'less_than_or_equal', 'more_than_or_equal']:
    setattr(ObjSpace, _name, _new_comparison_op(_name))

W_IntObject.type = ObjSpace.w_int
W_StringObject.type = ObjSpace.w_str
W_BoolObject.type = ObjSpace.w_bool
W_FloatObject.type = ObjSpace.w_float
W_NullObject.type = ObjSpace.w_null
space = ObjSpace()
