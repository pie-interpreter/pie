from pie.objects.variable import W_Variable
from pie.types import PHPTypes

__author__ = 'sery0ga'


class ObjSpace(object):

    def int(self, value):
        from pie.objects.int import W_Int
        return W_Int(value)

    def string(self, value):
        from pie.objects.string import W_String
        return W_String(value)

    def bool(self, value):
        from pie.objects.bool import W_Bool
        return W_Bool(value)

    def float(self, value):
        from pie.objects.float import W_Float
        return W_Float(value)

    def null(self):
        from pie.objects.null import W_Null
        return W_Null()

    def array(self, value=[]):
        from pie.objects.array import W_Array
        return W_Array(value)

    def undefined(self):
        from pie.objects.base import W_Undefined
        return W_Undefined()

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
        common_type = self.get_common_arithmetic_type(left_number, right_number)
        if common_type == PHPTypes.w_int:
            return left_number.as_int().plus(right_number.as_int())
        else:
            return left_number.as_float().plus(right_number.as_float())

    def substract(self, w_left, w_right):
        """
        In PHP '-' is supported only for numbers
        """
        left_number = w_left.deref().as_number()
        right_number = w_right.deref().as_number()
        common_type = self.get_common_arithmetic_type(left_number, right_number)
        if common_type == PHPTypes.w_int:
            return left_number.as_int().minus(right_number.as_int())
        else:
            return left_number.as_float().minus(right_number.as_float())

    def multiply(self, w_left, w_right):
        """
        In PHP '*' is supported only for numbers
        """
        left_number = w_left.deref().as_number()
        right_number = w_right.deref().as_number()
        common_type = self.get_common_arithmetic_type(left_number, right_number)
        if common_type == PHPTypes.w_int:
            return left_number.as_int().multiply(right_number.as_int())
        else:
            return left_number.as_float().multiply(right_number.as_float())

    def divide(self, w_left, w_right):
        """
        In PHP '*' is supported only for numbers
        """
        left_number = w_left.deref().as_number()
        right_number = w_right.deref().as_number()
        common_type = self.get_common_arithmetic_type(left_number, right_number)
        if common_type == PHPTypes.w_int:
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
        if w_left.deref().get_type() != w_right.deref().get_type():
            return self.bool(False)
        return w_left.deref().equal(w_right.deref())

    def not_identical(self, w_left, w_right):
        if w_left.deref().get_type() != w_right.deref().get_type():
            return self.bool(True)
        return w_left.deref().not_equal(w_right.deref())

    def is_empty(self, w_object):
        return self.bool(not w_object.deref().is_true())

    def get_common_comparison_type(self, w_left, w_right):
        """ Use this function only in comparison operations (like '>' or '<=')
        """
        left_type = w_left.get_type()
        right_type = w_right.get_type()
        if (self._is_any_number(left_type, right_type) and
                self._is_any_string(left_type, right_type)):
            """
            http://www.php.net/manual/en/language.operators.comparison.php

            If you compare a number with a string or the comparison involves numerical strings,
            then each string is converted to a number and the comparison performed numerically
            """
            return PHPTypes.w_float
        elif left_type == PHPTypes.w_int and right_type == PHPTypes.w_float:
            """
            http://www.php.net/manual/en/language.types.type-juggling.php

             If either operand is a float, then both operands are evaluated as floats,
             and the result will be a float
            """
            return PHPTypes.w_float
        elif left_type == PHPTypes.w_null and right_type == PHPTypes.w_string:
            """
            http://www.php.net/manual/en/language.operators.comparison.php

            Table "Comparison with Various Types", line 1
            Convert NULL to "", numerical or lexical comparison
            """
            return PHPTypes.w_string
        elif left_type == PHPTypes.w_null and right_type != PHPTypes.w_null:
            """
            http://www.php.net/manual/en/language.operators.comparison.php

            Table "Comparison with Various Types", line 2
            Convert to bool, FALSE < TRUE
            """
            return PHPTypes.w_bool
        elif left_type == PHPTypes.w_bool:
            return PHPTypes.w_bool
        return left_type

    def get_common_arithmetic_type(self, w_left, w_right):
        """ Use this function only in arithmetic operations (like '-' or '+')
        """
        if self._is_any_float(w_left.get_type(), w_right.get_type()):
            return PHPTypes.w_float
        return PHPTypes.w_int

    def _is_any_number(self, left_type, right_type):
        if (left_type == PHPTypes.w_int or right_type == PHPTypes.w_int
                or self._is_any_float(left_type, right_type)):
            return True
        return False

    def _is_any_float(self, left_type, right_type):
        if left_type == PHPTypes.w_float or right_type == PHPTypes.w_float:
            return True
        return False

    def _is_any_string(self, left_type, right_type):
        if left_type == PHPTypes.w_string or right_type == PHPTypes.w_string:
            return True
        return False


def _new_comparison_op(name):
    def func(self, w_left, w_right):
        from pie.objects.int import W_Int
        from pie.objects.string import NotConvertibleToNumber
        w_left = w_left.deref()
        w_right = w_right.deref()
        php_type = self.get_common_comparison_type(w_left, w_right)
        if php_type == PHPTypes.w_string:
            try:
                if w_left.get_type() == PHPTypes.w_null:
                    return getattr(w_left.as_string(), name)(w_right)
                left_number = w_left.as_number_strict()
                right_number = w_right.as_number_strict()
                if self._is_any_float(left_number.get_type(), right_number.get_type()):
                    return getattr(left_number.as_float(), name)(right_number.as_float())
                assert isinstance(left_number, W_Int)
                return getattr(left_number, name)(right_number)
            except NotConvertibleToNumber:
                return getattr(w_left, name)(w_right)
        elif php_type == PHPTypes.w_int:
            return getattr(w_left.as_int(), name)(w_right.as_int())
        elif php_type == PHPTypes.w_float:
            return getattr(w_left.as_float(), name)(w_right.as_float())
        elif php_type == PHPTypes.w_bool:
            return getattr(w_left.as_bool(), name)(w_right.as_bool())
        elif php_type == PHPTypes.w_null:
            # this is possible only if both arguments are null
            return getattr(w_left, name)(w_right)
        elif php_type == PHPTypes.w_array:
            # we're sure now, that at least w_left.php_type == PHPTypes.w_array
            if w_right.get_type() == PHPTypes.w_array:
                return getattr(w_left, name)(w_right)
            # in php array on the left is always > than anything (except array)
            # on the right:
            # Example: array(5) > 7, array(0) > true.
            # But: true == array(0) due to type conversion
            elif name == 'more_than' or name == 'more_than_or_equal' \
                    or name == 'not_equal':
                return space.bool(True)
            else:
                return space.bool(False)
        raise NotImplementedError

    func.func_name = name
    return func

for _name in ['less_than', 'more_than', 'equal', 'not_equal',
              'less_than_or_equal', 'more_than_or_equal']:
    setattr(ObjSpace, _name, _new_comparison_op(_name))

space = ObjSpace()
