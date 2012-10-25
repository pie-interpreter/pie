from pie.error import InterpreterError, PHPError
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

class InterpreterArg:
    """
    Stores data required for each operand handler in interpreter
    """
    def __init__(self, frame, bytecode):
        self.frame = frame
        self.bytecode = bytecode
        self.position = 0

    def get_line(self):
        return self.bytecode.get_line(self.position)

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
        args = InterpreterArg(frame, bytecode)
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
                args.position = position
                if we_are_translated():
                    for index, name in unrolling_bc:
                        if index == next_instr:
                            position = getattr(self, name)(args, arg)
                            break
                    else:
                        assert False
                else:
                    opcode_name = get_opcode_name(next_instr)
                    position = getattr(self, opcode_name)(args, arg)

                # this is a return condition
                if position == self.RETURN_FLAG:
                    break

        except InterpreterError:
            raise

        if len(frame.stack):
            return frame.stack.pop()
        else:
            return self.space.int(0)

    def ECHO(self, args, value):
        stack_value = args.frame.stack.pop()
        os.write(1, stack_value.str_w())
        return args.position

    def RETURN(self, args, value):
        return self.RETURN_FLAG

    def ADD(self, args, value):
        right = args.frame.stack.pop()
        left = args.frame.stack.pop()
        result = self.space.plus(left, right)
        args.frame.stack.append(result)
        return args.position

    def SUBSTRACT(self, args, value):
        right = args.frame.stack.pop()
        left = args.frame.stack.pop()
        result = self.space.minus(left, right)
        args.frame.stack.append(result)
        return args.position

    def MULTIPLY(self, args, value):
        right = args.frame.stack.pop()
        left = args.frame.stack.pop()
        result = self.space.multiply(left, right)
        args.frame.stack.append(result)
        return args.position

    def LESS_THAN(self, args, value):
        right = args.frame.stack.pop()
        left = args.frame.stack.pop()
        result = left.less(right)
        args.frame.stack.append(result)
        return args.position

    def MORE_THAN(self, args, value):
        right = args.frame.stack.pop()
        left = args.frame.stack.pop()
        result = left.more(right)
        args.frame.stack.append(result)
        return args.position

    def CONCAT(self, args, value):
        right = args.frame.stack.pop()
        left = args.frame.stack.pop()
        result = self.space.concatenate(left, right)
        args.frame.stack.append(result)
        return args.position

    def LOAD_CONST(self, args, value):
        args.frame.stack.append(args.bytecode.consts[value])
        return args.position

    def LOAD_NAME(self, args, function_index):
        function_name = args.bytecode.names[function_index]
        args.frame.stack.append(self.space.str(function_name))
        return args.position

    def LOAD_FAST(self, args, var_index):
        var_name = args.bytecode.names[var_index]
        try:
            value = args.frame.variables[var_name]
        except KeyError:
            value = self.space.int(0)
        args.frame.stack.append(value)
        return args.position

    def STORE_FAST(self, args, var_index):
        var_name = args.bytecode.names[var_index]
        value = args.frame.stack.pop()
        args.frame.variables[var_name] = value

        return args.position

    def CALL_FUNCTION(self, args, arguments_number):
        # load function name
        function_name = args.frame.stack.pop().val
        # load function bytecode
        try:
            function = self.context.functions[function_name]
        except KeyError:
            message = "Call to undefined function %s()" % function_name
            raise PHPError(message,
                           PHPError.FATAL,
                           args.bytecode.get_filename(),
                           args.get_line())

        function_frame = Frame()
        # put function arguments to frame
        for argument in function.arguments:
            function_frame.variables[argument] = args.frame.stack.pop()

        return_value = self.interpret(function_frame, function.bytecode)
        args.frame.stack.append(return_value)
        return args.position

    def JUMP(self, args, new_position):
        return new_position

    def JUMP_IF_FALSE(self, args, new_position):
        value = args.frame.stack.pop()
        if value.is_true():
            return args.position
        return new_position


def _define_opcodes():
    for index in OPCODE:
        yield index, OPCODE[index]

opcodes = list(_define_opcodes())
unrolling_bc = unrolling_iterable(opcodes)