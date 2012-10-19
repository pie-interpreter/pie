from pie.error import InterpreterError
from pie.opcodes import OPCODE_INDEX_DIVIDER, get_opcode_name, OPCODE
from pypy.rlib.objectmodel import we_are_translated
from pypy.rlib.unroll import unrolling_iterable
import os

__author__ = 'sery0ga'

class Interpreter:

    def __init__(self):
        pass

    def interpret(self, space, frame, bytecode):
        position = 0
        code = bytecode.code
        bytecode_length = len(bytecode.code)
        try:
            while True:
                if position >= bytecode_length:
                    break

                next_instr = ord(code[position])
                position += 1
                if next_instr > OPCODE_INDEX_DIVIDER:
                    arg = ord(code[position])
                    position += 1
                else:
                    arg = 0 # don't make it negative
                assert arg >= 0

                if we_are_translated():
                    for index, name in unrolling_bc:
                        if index == next_instr:
                            getattr(self, name)(frame, bytecode, arg)
                            break
                    else:
                        assert False
                else:
                    opcode_name = get_opcode_name(next_instr)
                    getattr(self, opcode_name)(frame, bytecode, arg)

        except InterpreterError:
            print "Error occured somewhere"
            raise

    def ECHO(self, frame, bytecode, value):
        stack_value = frame.stack.pop()
        os.write(1, str(stack_value))

        return 0

    def ADD(self, frame, bytecode, value):
        left = frame.stack.pop()
        right = frame.stack.pop()
        result = int(left) + int(right)
        frame.stack.append(str(result))

        return 0

    def LOAD_CONST(self, frame, bytecode, value):
        frame.stack.append(bytecode.consts[value].intval)

        return 0


def define_opcodes():
    for index in OPCODE:
        yield index, OPCODE[index]

opcodes = list(define_opcodes())
unrolling_bc = unrolling_iterable(opcodes)