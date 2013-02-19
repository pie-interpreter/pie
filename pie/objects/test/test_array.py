import unittest

from pie.objspace import space
from pie.objects.array import IllegalOffsetType


class TestArray(unittest.TestCase):

    def setUp(self):
        self.array = space.array([])

    def test_array_creation_int_branch(self):
        raw = [space.int(3), space.int(1),
                space.float(-1.2), space.int(2),
                space.bool(False), space.int(2),
                space.bool(True), space.int(3)]
        actual = space.array(raw)
        expected = {3: space.int(1), -1: space.int(2),
                    0: space.int(2), 1: space.int(3)}
        self.assertEqual(expected, actual.storage)

    def test_array_creation_null_string_branch(self):
        raw = [space.str("test"), space.int(1),
                space.str("08"), space.int(2),
                space.str("99"), space.int(3),
                space.null(), space.int(4),
                space.str("-5"), space.int(5),
                space.str("-09"), space.int(7)]
        actual = space.array(raw)
        expected = {"test": space.int(1), "08": space.int(2),
                    99: space.int(3), "": space.int(4),
                    -5: space.int(5), "-09": space.int(7)}
        self.assertEqual(expected, actual.storage)

    def test_array_creation_one_key(self):
        raw = [space.int(1), space.int(1),
                space.str("1"), space.int(2),
                space.float(1.5), space.int(3),
                space.bool(True), space.int(4)]
        actual = space.array(raw)
        expected = {1: space.int(4)}
        self.assertEqual(expected, actual.storage)

    def test_array_creation_with_no_keys(self):
        raw = [space.undefined(), space.int(1),
                space.undefined(), space.int(2),
                space.float(6.0), space.int(3),
                space.undefined(), space.int(4),
                space.int(3), space.int(5),
                space.undefined(), space.int(6)]
        actual = space.array(raw)
        expected = {0: space.int(1), 1: space.int(2),
                    6: space.int(3), 7: space.int(4),
                    3: space.int(5), 8: space.int(6)}
        self.assertEqual(expected, actual.storage)
        raw = [space.str("6"), space.int(3),
                space.str("3"), space.int(5),
                space.undefined(), space.int(6)]
        actual = space.array(raw)
        expected = {6: space.int(3), 3: space.int(5),
                    7: space.int(6)}
        self.assertEqual(expected, actual.storage)

    def test_is_true(self):
        self.assertFalse(self.array.is_true())
        self.array.set(space.int(0), space.int(3))
        self.assertTrue(self.array.is_true())

    def test_as_bool(self):
        false = space.bool(False)
        self.assertTrue(false.equal(self.array.as_bool()).is_true())
        true = space.bool(True)
        self.array.set(space.int(3), space.int(3))
        self.assertTrue(true.equal(self.array.as_bool()).is_true())
        self.array.set(space.int(0), space.int(3))
        self.assertTrue(true.equal(self.array.as_bool()).is_true())
        self.assertFalse(false.equal(self.array.as_bool()).is_true())

    def test_as_float(self):
        zero = space.float(0.0)
        self.assertTrue(zero.equal(self.array.as_float()).is_true())
        self.array.set(space.int(3), space.int(3))
        one = space.float(1.0)
        self.assertTrue(one.equal(self.array.as_float()).is_true())
        self.assertFalse(zero.equal(self.array.as_float()).is_true())

    def test_as_int(self):
        zero = space.int(0)
        self.assertTrue(zero.equal(self.array.as_int()).is_true())
        one = space.int(1)
        self.array.set(space.int(3), space.int(5))
        self.assertTrue(one.equal(self.array.as_int()).is_true())
        five = space.int(5)
        self.assertFalse(five.equal(self.array.as_int()).is_true())

    def test_as_string(self):
        expected = space.str('Array')
        self.assertTrue(expected.equal(self.array.as_string()).is_true())
        not_expected = space.str('')
        self.assertFalse(not_expected.equal(self.array.as_string()).is_true())
        self.array.set(space.int(0), space.str('Array'))
        self.assertTrue(expected.equal(self.array.as_string()).is_true())

    def test_equal(self):
        left = space.array()
        right = space.array()
        self.assertTrue(right.equal(left).is_true())
        left = space.array([space.int(1), space.int(1)])
        self.assertFalse(right.equal(left).is_true())
        right = space.array([space.int(1), space.int(1)])
        self.assertTrue(right.equal(left).is_true())
        right = space.array([space.int(2), space.int(1)])
        self.assertFalse(right.equal(left).is_true())
        right = space.array([space.int(1), space.int(2)])
        self.assertFalse(right.equal(left).is_true())
        right = space.array([space.int(1),
            space.array([space.int(0), space.int(1)])])
        self.assertFalse(right.equal(left).is_true())

    def test_equal_multidimension(self):
        left = space.array([space.int(0),
                    space.array([space.int(0), space.int(1)])])
        right = space.array([space.int(0),
                    space.array([space.int(0), space.int(1)])])
        self.assertTrue(right.equal(left).is_true())

    def test_less_than(self):
        left = space.array([space.int(0), space.int(1)])
        right = space.array()
        self.assertTrue(right.less_than(left).is_true())
        right = space.array([space.int(0), space.int(0)])
        self.assertTrue(right.less_than(left).is_true())
        right = space.array([space.int(1), space.int(0)])
        self.assertFalse(right.less_than(left).is_true())
        right = space.array([space.int(0),
                space.array([space.int(0), space.int(1)])])
        self.assertFalse(right.less_than(left).is_true())
        self.assertFalse(left.less_than(right).is_true())
        left = space.array()
        self.assertFalse(right.less_than(left).is_true())


    def test_more_than(self):
        left = space.array()
        right = space.array([space.int(0), space.int(1)])
        self.assertTrue(right.more_than(left).is_true())
        left = space.array([space.int(0), space.int(0)])
        self.assertTrue(right.more_than(left).is_true())
        left = space.array([space.int(1), space.int(0)])
        self.assertFalse(right.more_than(left).is_true())
        left = space.array([space.int(0), space.int(0)])
        right = space.array([space.int(0),
                space.array([space.int(0), space.int(1)])])
        self.assertTrue(right.more_than(left).is_true())
        left = space.array([space.int(0), space.int(1),
                            space.int(1), space.int(2)])
        self.assertFalse(right.more_than(left).is_true())

    def test_not_equal(self):
        left = space.array()
        right = space.array()
        self.assertFalse(right.not_equal(left).is_true())
        left = space.array([space.int(1), space.int(1)])
        self.assertTrue(right.not_equal(left).is_true())
        right = space.array([space.int(1), space.int(1)])
        self.assertFalse(right.not_equal(left).is_true())
        right = space.array([space.int(2), space.int(1)])
        self.assertTrue(right.not_equal(left).is_true())
        right = space.array([space.int(1), space.int(2)])
        self.assertTrue(right.not_equal(left).is_true())
        right = space.array([space.int(1),
            space.array([space.int(0), space.int(1)])])
        self.assertTrue(right.not_equal(left).is_true())

    def test_less_than_or_equal(self):
        left = space.array([space.int(0), space.int(1)])
        right = space.array()
        self.assertTrue(right.less_than_or_equal(left).is_true())
        right = space.array([space.int(0), space.int(1)])
        self.assertTrue(right.less_than_or_equal(left).is_true())
        right = space.array([space.int(1), space.int(0)])
        self.assertFalse(right.less_than_or_equal(left).is_true())
        right = space.array([space.int(0),
                space.array([space.int(0), space.int(1)])])
        self.assertFalse(right.less_than_or_equal(left).is_true())
        left = space.array()
        self.assertFalse(right.less_than_or_equal(left).is_true())

    def test_more_than_or_equal(self):
        left = space.array()
        right = space.array([space.int(0), space.int(1)])
        self.assertTrue(right.more_than_or_equal(left).is_true())
        left = space.array([space.int(0), space.int(1)])
        self.assertTrue(right.more_than_or_equal(left).is_true())
        left = space.array([space.int(1), space.int(0)])
        self.assertFalse(right.more_than_or_equal(left).is_true())
        left = space.array([space.int(0), space.int(0)])
        right = space.array([space.int(0),
                space.array([space.int(0), space.int(1)])])
        self.assertTrue(right.more_than_or_equal(left).is_true())
        left = space.array([space.int(0), space.int(1),
                            space.int(1), space.int(2)])
        self.assertFalse(right.more_than_or_equal(left).is_true())

    def test_increment(self):
        actual = space.array([space.int(0), space.int(1)])
        actual.inc()
        expected = space.array([space.int(0), space.int(1)])
        self.assertTrue(expected.equal(actual).is_true())

    def test_decrement(self):
        actual = space.array([space.int(0), space.int(1)])
        actual.dec()
        expected = space.array([space.int(0), space.int(1)])
        self.assertTrue(expected.equal(actual).is_true())

    def test_get(self):
        array = space.array([space.int(0), space.int(1),
                             space.int(1), space.int(2)])
        value = array.get(space.int(0))
        self.assertTrue(value.equal(space.int(1)).is_true())
        value = array.get(space.int(1))
        self.assertTrue(value.equal(space.int(2)).is_true())
        # check no valid key exception
        with self.assertRaises(KeyError):
            array.get(space.int(2))

    def test_get_type_conversion_string(self):
        array = space.array([space.int(0), space.int(1),
                             space.int(1), space.int(2),
                             space.int(-1), space.int(3)])
        value = array.get(space.str("1"))
        self.assertTrue(value.equal(space.int(2)).is_true())
        value = array.get(space.str("-1"))
        self.assertTrue(value.equal(space.int(3)).is_true())
        with self.assertRaises(KeyError):
            value = array.get(space.str("01"))
        with self.assertRaises(KeyError):
            value = array.get(space.str("-0"))
        value = array.get(space.str("0"))
        self.assertTrue(value.equal(space.int(1)).is_true())
        with self.assertRaises(KeyError):
            value = array.get(space.str("12Tst"))

    def test_get_type_conversion_other(self):
        array = space.array([space.int(0), space.int(1),
                             space.int(1), space.int(2),
                             space.int(-1), space.int(3)])
        value = array.get(space.float(1.5))
        self.assertTrue(value.equal(space.int(2)).is_true())
        value = array.get(space.bool(True))
        self.assertTrue(value.equal(space.int(2)).is_true())
        value = array.get(space.bool(False))
        self.assertTrue(value.equal(space.int(1)).is_true())
        with self.assertRaises(KeyError):
            value = array.get(space.null())
        with self.assertRaises(IllegalOffsetType):
            value = array.get(space.array())

    def test_set(self):
        array = space.array([space.int(5), space.int(1),
                             space.int(12), space.int(2)])
        array.set(space.int(2), space.int(3))
        value = array.get(space.int(2))
        self.assertTrue(value.equal(space.int(3)).is_true())
        array.set(space.str("4"), space.int(4))
        value = array.get(space.int(4))
        self.assertTrue(value.equal(space.int(4)).is_true())
        # no index test
        array.set(space.undefined(), space.int(13))
        value = array.get(space.int(13))
        self.assertTrue(value.equal(space.int(13)).is_true())
        array.set(space.int(15), space.int(15))
        array.set(space.undefined(), space.int(16))
        value = array.get(space.int(16))
        self.assertTrue(value.equal(space.int(16)).is_true())
        # now string
        array.set(space.str("20"), space.int(20))
        array.set(space.undefined(), space.int(21))
        value = array.get(space.int(21))
        self.assertTrue(value.equal(space.int(21)).is_true())

    def test_get_set_combination(self):
        array = space.array()
        with self.assertRaises(KeyError):
            array.get(space.int(5))
        array.set(space.undefined(), space.int(1))
        value = array.get(space.int(0))
        self.assertTrue(value.equal(space.int(1)).is_true())
        with self.assertRaises(KeyError):
            array.get(space.str("7"))
        array.set(space.undefined(), space.int(2))
        value = array.get(space.int(1))
        self.assertTrue(value.equal(space.int(2)).is_true())
