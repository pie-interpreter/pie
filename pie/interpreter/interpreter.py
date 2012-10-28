from pie.error import InterpreterError
from pie.interpreter.frame import Frame
from pie.opcodes import OPCODE_INDEX_DIVIDER, get_opcode_name, OPCODE
#from pypy.rlib import jit
from pypy.rlib.objectmodel import we_are_translated
from pypy.rlib.unroll import unrolling_iterable
import os

__author__ = 'sery0ga'

#driver = jit.JitDriver(reds = ['frame'],
#    greens = ['position', 'self'],
#    virtualizables = ['frame'],
#    should_unroll_one_iteration = lambda *args: True)

class Interpreter:

    RETURN_FLAG = -1

    def __init__(self, space, context):
        self.space = space
        self.context = context

    def interpret(self, frame, bytecode):
        self.context.initialize_functions(bytecode)

        position = 0
        code = bytecode.code
        bytecode_length = len(bytecode.code)
        try:
            while True:
                #driver.jit_merge_point(frame=frame,
                #    position=position, self=self)
                if position >= bytecode_length:
                    break

                next_instr = ord(code[position])
                position += 1
                if next_instr > OPCODE_INDEX_DIVIDER:
                    arg = ord(code[position]) + (ord(code[position + 1]) << 8)
                    position += 2
                else:
                    arg = 0 # don't make it negative
                assert arg >= 0

                if we_are_translated():
                    for index, name in unrolling_bc:
                        if index == next_instr:
                            position = getattr(self, name)(frame, bytecode,
                                                           position, arg)
                            break
                    else:
                        assert False
                else:
                    opcode_name = get_opcode_name(next_instr)
                    position = getattr(self, opcode_name)(frame, bytecode,
                                                          position, arg)

                # this is a return condition
                if position == self.RETURN_FLAG:
                    break

        except InterpreterError:
            print "Error occured somewhere"
            raise

        if len(frame.stack):
            return frame.stack.pop()
        else:
            return self.space.int(0)

    def ECHO(self, frame, bytecode, position, value):
        stack_value = frame.stack.pop()
        os.write(1, stack_value.str_w())
        return position

    def RETURN(self, frame, bytecode, position, value):
        return self.RETURN_FLAG

    def ADD(self, frame, bytecode, position, value):
        right = frame.stack.pop()
        left = frame.stack.pop()
        result = self.space.plus(left, right)
        frame.stack.append(result)
        return position

    def SUBSTRACT(self, frame, bytecode, position, value):
        right = frame.stack.pop()
        left = frame.stack.pop()
        result = self.space.minus(left, right)
        frame.stack.append(result)
        return position

    def MULTIPLY(self, frame, bytecode, position, value):
        right = frame.stack.pop()
        left = frame.stack.pop()
        result = self.space.multiply(left, right)
        frame.stack.append(result)
        return position

    def LESS_THAN(self, frame, bytecode, position, value):
        right = frame.stack.pop()
        left = frame.stack.pop()
        result = left.less(right)
        frame.stack.append(result)
        return position

    def MORE_THAN(self, frame, bytecode, position, value):
        right = frame.stack.pop()
        left = frame.stack.pop()
        result = left.more(right)
        frame.stack.append(result)
        return position

    def CONCAT(self, frame, bytecode, position, value):
        right = frame.stack.pop()
        left = frame.stack.pop()
        result = self.space.concatenate(left, right)
        frame.stack.append(result)
        return position

    def POP_STACK(self, frame, bytecode, position, value):
        frame.stack.pop()
        return position

    def DUPLICATE_TOP(self, frame, bytecode, position, value):
        frame.stack.append(frame.stack[-1])
        return position

    def LOAD_CONST(self, frame, bytecode, position, value):
        frame.stack.append(bytecode.consts[value])
        return position

    def LOAD_NAME(self, frame, bytecode, position, function_index):
        function_name = bytecode.names[function_index]
        frame.stack.append(self.space.str(function_name))
        return position

    def LOAD_VAR_FAST(self, frame, bytecode, position, var_index):
        var_name = bytecode.names[var_index]
        try:
            value = frame.variables[var_name]
        except KeyError:
            value = self.space.int(0)
        frame.stack.append(value)
        return position

    def STORE_VAR_FAST(self, frame, bytecode, position, var_index):
        var_name = bytecode.names[var_index]
        # we need to leave value on stack
        value = frame.stack[-1]
        frame.variables[var_name] = value

        return position

    def CALL_FUNCTION(self, frame, bytecode, position, arguments_number):
        # load function name
        function_name = frame.stack.pop().val
        # load function bytecode
        try:
            function = self.context.functions[function_name]
        except KeyError:
            raise InterpreterError("Function %s is not defined" % function_name)

        function_frame = Frame()
        # put function arguments to frame
        for argument in function.arguments:
            function_frame.variables[argument] = frame.stack.pop()

        return_value = self.interpret(function_frame, function.bytecode)
        frame.stack.append(return_value)
        return position

    def JUMP(self, frame, bytecode, position, new_position):
        return new_position

    def JUMP_IF_FALSE(self, frame, bytecode, position, new_position):
        value = frame.stack.pop()
        if value.is_true():
            return position
        return new_position

    def JUMP_IF_TRUE(self, frame, bytecode, position, new_position):
        value = frame.stack.pop()
        if value.is_true():
            return new_position
        return position


def _define_opcodes():
    for index in OPCODE:
        yield index, OPCODE[index]

opcodes = list(_define_opcodes())
unrolling_bc = unrolling_iterable(opcodes)