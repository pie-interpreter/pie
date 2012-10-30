from pie.error import InterpreterError, PHPError
from pie.interpreter.frame import Frame
from pie.opcodes import OPCODE_INDEX_DIVIDER, get_opcode_name, OPCODE
from pypy.rlib.jit import JitDriver
from pypy.rlib.objectmodel import we_are_translated
from pypy.rlib.unroll import unrolling_iterable
import os

__author__ = 'sery0ga'

jitdriver = JitDriver(
    greens=['bytecode_length', 'position', 'code', 'space', 'self'],
    reds=['args', 'frame'])

class InterpreterArg:
    """
    Stores data required for each operand handler in interpreter
    """
    def __init__(self, frame, bytecode):
        self.frame = frame
        self.bytecode = bytecode
        self.position = 0
        self.opcode_position = 0

    def get_line(self):
        return self.bytecode.opcode_lines[self.opcode_position]

class Interpreter:

    RETURN_FLAG = -1

    def __init__(self, space, context):
        self.space = space
        self.context = context

    def interpret(self, frame, bytecode):
        #initialization phase
        self.context.initialize_functions(bytecode)

        position = 0
        code = bytecode.code
        bytecode_length = len(bytecode.code)
        args = InterpreterArg(frame, bytecode)
        try:
            while True:
                jitdriver.jit_merge_point(bytecode_length=bytecode_length,
                                          space=self.space,
                                          position=position,
                                          code=code,
                                          args=args,
                                          frame=frame,
                                          self=self)

                if position >= bytecode_length:
                    break

                args.opcode_position = position

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

        if frame.stack:
            return frame.stack.pop()
        else:
            return self.space.int(0)

    def ECHO(self, args, value):
        stack_value = args.frame.stack.pop()
        os.write(1, stack_value.str_w())
        return args.position

    def RETURN(self, args, value):
        return self.RETURN_FLAG

    def POP_STACK(self, args, value):
        args.frame.stack.pop()
        return args.position

    def DUPLICATE_TOP(self, args, value):
        args.frame.stack.append(args.frame.stack[-1])
        return args.position

    def INCLUDE(self, args, value):
        raise InterpreterError, "Not implemented"

    def INCLUDE_ONCE(self, args, value):
        raise InterpreterError, "Not implemented"

    def REQUIRE(self, args, value):
        raise InterpreterError, "Not implemented"

    def REQUIRE_ONCE(self, args, value):
        raise InterpreterError, "Not implemented"

    def NOT(self, args, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_ARRAY(self, args, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_BOOL(self, args, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_DOUBLE(self, args, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_INT(self, args, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_OBJECT(self, args, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_STRING(self, args, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_UNSET(self, args, value):
        raise InterpreterError, "Not implemented"

    def PRE_INCREMENT(self, args, value):
        raise InterpreterError, "Not implemented"

    def PRE_DECREMENT(self, args, value):
        raise InterpreterError, "Not implemented"

    def POST_INCREMENT(self, args, value):
        raise InterpreterError, "Not implemented"

    def POST_DECREMENT(self, args, value):
        raise InterpreterError, "Not implemented"

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

    def CONCAT(self, args, value):
        right = args.frame.stack.pop()
        left = args.frame.stack.pop()
        result = self.space.concatenate(left, right)
        args.frame.stack.append(result)
        return args.position

    def MULTIPLY(self, args, value):
        right = args.frame.stack.pop()
        left = args.frame.stack.pop()
        result = self.space.multiply(left, right)
        args.frame.stack.append(result)
        return args.position

    def DIVIDE(self, args, value):
        raise InterpreterError, "Not implemented"

    def MOD(self, args, value):
        raise InterpreterError, "Not implemented"

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

    def LESS_THAN_OR_EQUAL(self, args, value):
        raise InterpreterError, "Not implemented"

    def MORE_THAN_OR_EQUAL(self, args, value):
        raise InterpreterError, "Not implemented"

    def EQUAL(self, args, value):
        raise InterpreterError, "Not implemented"

    def NOT_EQUAL(self, args, value):
        raise InterpreterError, "Not implemented"

    def IDENTICAL(self, args, value):
        raise InterpreterError, "Not implemented"

    def NOT_IDENTICAL(self, args, value):
        raise InterpreterError, "Not implemented"

    def XOR(self, args, value):
        raise InterpreterError, "Not implemented"

    def INPLACE_ADD(self, args, value):
        raise InterpreterError, "Not implemented"

    def INPLACE_SUBSTRACT(self, args, value):
        raise InterpreterError, "Not implemented"

    def INPLACE_CONCAT(self, args, value):
        raise InterpreterError, "Not implemented"

    def INPLACE_MULTIPLY(self, args, value):
        raise InterpreterError, "Not implemented"

    def INPLACE_DIVIDE(self, args, value):
        raise InterpreterError, "Not implemented"

    def INPLACE_MOD(self, args, value):
        raise InterpreterError, "Not implemented"

    def LOAD_VAR(self, args, value):
        raise InterpreterError, "Not implemented"

    def STORE_VAR(self, args, value):
        raise InterpreterError, "Not implemented"

    def LOAD_CONST(self, args, value):
        args.frame.stack.append(args.bytecode.consts[value])
        return args.position

    def LOAD_NAME(self, args, function_index):
        function_name = args.bytecode.names[function_index]
        args.frame.stack.append(self.space.str(function_name))
        return args.position

    def LOAD_VAR_FAST(self, args, var_index):
        var_name = args.bytecode.names[var_index]
        try:
            value = args.frame.variables[var_name]
        except KeyError:
            value = self._handle_undefined(var_name, args)
        args.frame.stack.append(value)
        return args.position

    def STORE_VAR_FAST(self, args, var_index):
        var_name = args.bytecode.names[var_index]
        value = args.frame.stack[-1] # we need to leave value on the stack
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
                           args.bytecode.filename,
                           args.get_line(),
                           self.context.function_trace_stack)

        function_frame = Frame()
        # put function arguments to frame
        arg_position = 1
        for argument in function.arguments:
            if not args.frame.stack:
                message = "Missing argument %s for %s(), called" \
                    % (arg_position, function_name)
                error = PHPError(message,
                                 PHPError.WARNING,
                                 args.bytecode.filename,
                                 args.get_line(),
                                 self.context.function_trace_stack)
                print error
            else:
                function_frame.variables[argument] = args.frame.stack.pop()
            arg_position += 1

        # update trace stack and call function
        self.context.function_trace_stack.append(
            (function_name, args.get_line(), function.bytecode.filename)
        )
        return_value = self.interpret(function_frame, function.bytecode)
        self.context.function_trace_stack.pop()

        args.frame.stack.append(return_value)

        return args.position

    def JUMP(self, args, new_position):
        return new_position

    def JUMP_IF_FALSE(self, args, new_position):
        value = args.frame.stack.pop()
        if value.is_true():
            return args.position
        return new_position

    def JUMP_IF_TRUE(self, args, new_position):
        value = args.frame.stack.pop()
        if value.is_true():
            return new_position
        return args.position

    def _handle_undefined(self, name, args):
        message = "Undefined variable: %s" % name
        error = PHPError(message,
                         PHPError.NOTICE,
                         args.bytecode.filename,
                         args.get_line(),
                         self.context.function_trace_stack)
        print error
        return self.space.str("")

def _define_opcodes():
    for index in OPCODE:
        yield index, OPCODE[index]

opcodes = list(_define_opcodes())
unrolling_bc = unrolling_iterable(opcodes)