import unittest

from pie.objects.array import W_ArrayObject
from pie.objects.bool import W_BoolObject
from pie.objects.bool import W_IntObject
from pie.objects.bool import W_FloatObject
from pie.objects.string import W_StringObject


class TestArray(unittest.TestCase):

    def setUp(self):
        self.array = W_ArrayObject()

    def test_array_creation(self):
        raw = [1,1]
        array = W_ArrayObject(raw)
        expected = {1: 1}
        self.assertEqual(expected, array.storage)

    def test_is_true(self):
        self.assertFalse(self.array.is_true())
        self.array.set(0, 3)
        self.assertTrue(self.array.is_true())

    # def test_as_array(self):
    #     expected = W_ArrayObject()
    #     self.assertNotEqual(expected, self.array.as_array())
    def test_as_bool(self):
        false = W_BoolObject(False)
        self.assertTrue(false.equal(self.array.as_bool()).is_true())
        true = W_BoolObject(True)
        self.array.set(3, 3)
        self.assertTrue(true.equal(self.array.as_bool()).is_true())
        self.array.set(0, 3)
        self.assertTrue(true.equal(self.array.as_bool()).is_true())
        self.assertFalse(false.equal(self.array.as_bool()).is_true())

    def test_as_float(self):
        zero = W_FloatObject(0.0)
        self.assertTrue(zero.equal(self.array.as_float()).is_true())
        self.array.set(3, 3)
        one = W_FloatObject(1.0)
        self.assertTrue(one.equal(self.array.as_float()).is_true())
        self.assertFalse(zero.equal(self.array.as_float()).is_true())

    def test_as_int(self):
        zero = W_IntObject(0)
        self.assertTrue(zero.equal(self.array.as_int()).is_true())
        one = W_IntObject(1)
        self.array.set(3, 5)
        self.assertTrue(one.equal(self.array.as_int()).is_true())
        five = W_IntObject(5)
        self.assertFalse(five.equal(self.array.as_int()).is_true())

    def test_as_string(self):
        expected = W_StringObject('Array')
        self.assertTrue(expected.equal(self.array.as_string()).is_true())
        not_expected = W_StringObject('')
        self.assertFalse(not_expected.equal(self.array.as_string()).is_true())
        self.array.set(0, 'Array')
        self.assertTrue(expected.equal(self.array.as_string()).is_true())

    def test_as_equal(self):
        expected = W_ArrayObject()
        self.assertFalse(expected.equal(self.array).is_true())
