import unittest

from pie.objects.array import W_ArrayObject
from pie.objects.bool import W_BoolObject
from pie.objects.int import W_IntObject
from pie.objects.float import W_FloatObject
from pie.objects.null import W_NullObject
from pie.objects.string import W_StringObject
from pie.objects.base import W_Undefined


class TestArray(unittest.TestCase):

    def setUp(self):
        self.array = W_ArrayObject()

    def test_array_creation_int_branch(self):
        raw = [W_IntObject(3), W_IntObject(1),
                W_FloatObject(-1.2), W_IntObject(2),
                W_BoolObject(False), W_IntObject(2),
                W_BoolObject(True), W_IntObject(3)]
        actual = W_ArrayObject(raw)
        expected = {3: W_IntObject(1), -1: W_IntObject(2),
                    0: W_IntObject(2), 1: W_IntObject(3)}
        self.assertEqual(expected, actual.storage)

    def test_array_creation_null_string_branch(self):
        raw = [W_StringObject("test"), W_IntObject(1),
                W_StringObject("08"), W_IntObject(2),
                W_StringObject("99"), W_IntObject(3),
                W_NullObject(), W_IntObject(4),
                W_StringObject("-5"), W_IntObject(5),
                W_StringObject("-09"), W_IntObject(7)]
        actual = W_ArrayObject(raw)
        expected = {"test": W_IntObject(1), "08": W_IntObject(2),
                    99: W_IntObject(3), "": W_IntObject(4),
                    -5: W_IntObject(5), "-09": W_IntObject(7)}
        self.assertEqual(expected, actual.storage)

    def test_array_creation_one_key(self):
        raw = [W_IntObject(1), W_IntObject(1),
                W_StringObject("1"), W_IntObject(2),
                W_FloatObject(1.5), W_IntObject(3),
                W_BoolObject(True), W_IntObject(4)]
        actual = W_ArrayObject(raw)
        expected = {1: W_IntObject(4)}
        self.assertEqual(expected, actual.storage)

    def test_array_creation_with_no_keys(self):
        raw = [W_Undefined(), W_IntObject(1),
                W_Undefined(), W_IntObject(2),
                W_FloatObject(6.0), W_IntObject(3),
                W_Undefined(), W_IntObject(4),
                W_IntObject(3), W_IntObject(5),
                W_Undefined(), W_IntObject(6)]
        actual = W_ArrayObject(raw)
        expected = {0: W_IntObject(1), 1: W_IntObject(2),
                    6: W_IntObject(3), 7: W_IntObject(4),
                    3: W_IntObject(5), 8: W_IntObject(6)}
        self.assertEqual(expected, actual.storage)
        raw = [W_StringObject("6"), W_IntObject(3),
                W_StringObject("3"), W_IntObject(5),
                W_Undefined(), W_IntObject(6)]
        actual = W_ArrayObject(raw)
        expected = {6: W_IntObject(3), 3: W_IntObject(5),
                    7: W_IntObject(6)}
        self.assertEqual(expected, actual.storage)

    def test_is_true(self):
        self.assertFalse(self.array.is_true())
        self.array.set(0, 3)
        self.assertTrue(self.array.is_true())

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
