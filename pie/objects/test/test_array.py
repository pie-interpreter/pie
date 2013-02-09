import unittest

from pie.objspace import space

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
        self.array.set(0, 3)
        self.assertTrue(self.array.is_true())

    def test_as_bool(self):
        false = space.bool(False)
        self.assertTrue(false.equal(self.array.as_bool()).is_true())
        true = space.bool(True)
        self.array.set(3, 3)
        self.assertTrue(true.equal(self.array.as_bool()).is_true())
        self.array.set(0, 3)
        self.assertTrue(true.equal(self.array.as_bool()).is_true())
        self.assertFalse(false.equal(self.array.as_bool()).is_true())

    def test_as_float(self):
        zero = space.float(0.0)
        self.assertTrue(zero.equal(self.array.as_float()).is_true())
        self.array.set(3, 3)
        one = space.float(1.0)
        self.assertTrue(one.equal(self.array.as_float()).is_true())
        self.assertFalse(zero.equal(self.array.as_float()).is_true())

    def test_as_int(self):
        zero = space.int(0)
        self.assertTrue(zero.equal(self.array.as_int()).is_true())
        one = space.int(1)
        self.array.set(3, 5)
        self.assertTrue(one.equal(self.array.as_int()).is_true())
        five = space.int(5)
        self.assertFalse(five.equal(self.array.as_int()).is_true())

    def test_as_string(self):
        expected = space.str('Array')
        self.assertTrue(expected.equal(self.array.as_string()).is_true())
        not_expected = space.str('')
        self.assertFalse(not_expected.equal(self.array.as_string()).is_true())
        self.array.set(0, 'Array')
        self.assertTrue(expected.equal(self.array.as_string()).is_true())

    def test_as_equal(self):
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
        self.assertTrue(right.equal(right).is_true())

    def test_as_equal_multidimension(self):
        left = space.array([space.int(0),
                    space.array([space.int(0), space.int(1)])])
        right = space.array([space.int(0),
                    space.array([space.int(0), space.int(1)])])
        self.assertTrue(right.equal(left).is_true())
