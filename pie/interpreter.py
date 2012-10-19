import os
from pie.opcodes import OPCODE_INDEX_DIVIDER, get_opcode_name
from pie.error import InterpreterError

__author__ = 'sery0ga'

class Interpreter:

    def __init__(self):
        pass

    def interpret(self, space, frame, bytecode):
        pc = 0
        code = bytecode.code
        try:
            while True:
                next_instr = ord(code[pc])
                args_number = 0
                if next_instr > OPCODE_INDEX_DIVIDER:
                    args_number = 1
                pc += 1
                if args_number == 1:
                    arg = ord(code[pc])
                    pc += 1
                else:
                    arg = 0 # don't make it negative
                assert arg >= 0
                getattr(self, get_opcode_name(next_instr))(frame, arg)
        except InterpreterError:
            print "Error occured somewhere"
            raise

    def ECHO(self, frame):
        value = frame.stack.pop()
        os.write(1, str(value))

    def ADD(self, frame):
        left = frame.stack.pop()
        right = frame.stack.pop()
        result = left + right
        frame.stack.append(result)
        pass

    def LOAD_CONST(self, frame, value):
        frame.stack.append(value)
        pass
