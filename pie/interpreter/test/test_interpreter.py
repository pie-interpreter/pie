import unittest

from pie.objspace import space
from pie.interpreter.frame import Frame
# from pie.interpreter.context import Context
from pie.objects.base import W_Undefined
from pie.compiling.bytecode import Bytecode
from pie.objects.array import W_Cell
from pie.interpreter.interpreter import Interpreter


class TestInterpreter(unittest.TestCase):

    def setUp(self):
           self.interpreter = Interpreter(Bytecode(), "dummy_context", Frame())

    def test_RETURN(self):
        self.assertEqual(0, self.interpreter.position)
        dummy_value = 0
        self.interpreter.RETURN(dummy_value)
        self.assertEqual(self.interpreter.RETURN_FLAG,
                         self.interpreter.position)

    def test_DUPLICATE_TOP(self):
        value = space.int(1)
        self.interpreter.frame.stack.append(value)
        dummy_value = 0
        self.interpreter.DUPLICATE_TOP(dummy_value)
        self.assertIs(self.interpreter.frame.stack[0],
                      self.interpreter.frame.stack[1])

    def test_EMPTY_VAR(self):
        #TODO: add test_RETURN
        pass

    def test_GET_INDEX(self):
        name = 'a'
        w_array = space.array([space.int(0), space.int(1),
                               space.int(1), space.int(2)])
        self.interpreter.frame.variables[name] = w_array
        dummy_value = 0
        # good situation
        w_index = space.int(1)
        self.interpreter.frame.stack = [w_index, space.str(name)]
        self.interpreter.GET_INDEX(dummy_value)
        w_value = self.interpreter.frame.stack[0]
        self.assertIsInstance(w_value, W_Cell)
        self.assertTrue(w_value.deref().equal(space.int(2)))
        # empty index
        w_index = space.int(2)
        self.interpreter.frame.stack = [w_index, space.str(name)]
        self.interpreter.GET_INDEX(dummy_value)
        w_value = self.interpreter.frame.stack[0]
        self.assertIsInstance(w_value, W_Undefined)
        # IllegalOffsetType
        w_index = space.array([])
        self.interpreter.frame.stack = [w_index, space.str(name)]
        self.interpreter.GET_INDEX(dummy_value)
        w_value = self.interpreter.frame.stack[0]
        self.assertTrue(w_value.deref().equal(space.null()))

    def test_ISSET(self):
        w_array = space.array([space.int(1), space.int(2),
                               space.int(2), space.null()])
        self.interpreter.frame.variables = {"a": space.int(1),
                                            "b": space.null(),
                                            "c": w_array}
        # Test non-existent variables
        self.interpreter.frame.stack = [space.str("non"), space.str("a")]
        self.interpreter.ISSET(2)
        w_result = self.interpreter.frame.stack[-1]
        self.assertFalse(w_result.is_true())
        # Test null variable
        self.interpreter.frame.stack = [space.str("b"), space.str("a")]
        self.interpreter.ISSET(2)
        w_result = self.interpreter.frame.stack[-1]
        self.assertFalse(w_result.is_true())
        # Test positive branch
        self.interpreter.frame.stack = [space.str("a"), space.str("c")]
        self.interpreter.ISSET(2)
        w_result = self.interpreter.frame.stack[-1]
        self.assertTrue(w_result.is_true())
        # Test non-existent array index
        w_array_element = W_Cell(0, space.undefined())
        self.interpreter.frame.stack = [w_array_element, space.str("a")]
        self.interpreter.ISSET(2)
        w_result = self.interpreter.frame.stack[-1]
        self.assertFalse(w_result.is_true())
        # Test array index with null element
        w_array_element = W_Cell(1, space.null())
        self.interpreter.frame.stack = [w_array_element, space.str("a")]
        self.interpreter.ISSET(2)
        w_result = self.interpreter.frame.stack[-1]
        self.assertFalse(w_result.is_true())
        # Test array index with ordinary element
        w_array_element = W_Cell(1, space.int(1))
        self.interpreter.frame.stack = [w_array_element, space.str("a")]
        self.interpreter.ISSET(2)
        w_result = self.interpreter.frame.stack[-1]
        self.assertTrue(w_result.is_true())
        # Test array index with string element
        w_array_element = W_Cell(1, space.str("test"))
        self.interpreter.frame.stack = [w_array_element, space.str("a")]
        self.interpreter.ISSET(2)
        w_result = self.interpreter.frame.stack[-1]
        self.assertTrue(w_result.is_true())
