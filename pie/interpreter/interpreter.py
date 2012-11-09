from pie.compiling import compiling
from pie.error import InterpreterError, PHPError, DivisionByZero
from pie.interpreter.context import Context
from pie.interpreter.frame import Frame
from pie.objspace import space
from pie.opcodes import OPCODE_INDEX_DIVIDER, get_opcode_name, OPCODE
from pypy.rlib.objectmodel import we_are_translated
from pypy.rlib.unroll import unrolling_iterable
import os

__author__ = 'sery0ga'


def interpret(source):
    bytecode = compiling.compile_source(source)
    context = Context()
    context.initialize_function_trace_stack(source.filename)

    return interpret_bytecode(bytecode, context, Frame())


def interpret_bytecode(bytecode, context, frame):
    interpreter = Interpreter(bytecode, context, frame)
    return interpreter.interpret()


class Interpreter(object):

    RETURN_FLAG = -1

    def __init__(self, bytecode, context, frame):
        self.bytecode = bytecode
        self.context = context
        self.frame = frame

        self.position = 0
        self.opcode_position = 0
        self.context.initialize_functions(self.bytecode)

    def interpret(self):
        code = self.bytecode.code
        bytecode_length = len(self.bytecode.code)
        try:
            while True:
                if self.position >= bytecode_length:
                    break

                self.opcode_position = self.position

                next_instr = ord(code[self.position])
                self.position += 1

                if next_instr > OPCODE_INDEX_DIVIDER:
                    arg = ord(code[self.position]) \
                        + (ord(code[self.position + 1]) << 8)
                    self.position += 2
                else:
                    arg = 0  # don't make it negative

                assert arg >= 0

                if we_are_translated():
                    for index, name in unrolling_bc:
                        if index == next_instr:
                            getattr(self, name)(arg)
                            break
                    else:
                        assert False
                else:
                    opcode_name = get_opcode_name(next_instr)
                    getattr(self, opcode_name)(arg)

                # this is a return condition
                if self.position == self.RETURN_FLAG:
                    break

        except InterpreterError:
            raise

        if self.frame.stack:
            return self.frame.stack.pop()
        else:
            return space.int(0)

    def ECHO(self, value):
        stack_value = self.frame.stack.pop()
        os.write(1, stack_value.as_string().conststr_w())

    def PRINT(self, value):
        stack_value = self.frame.stack.pop()
        os.write(1, stack_value.as_string().str_w())
        self.frame.stack.append(space.int(1))

    def RETURN(self, value):
        self.position = self.RETURN_FLAG

    def POP_STACK(self, value):
        self.frame.stack.pop()

    def DUPLICATE_TOP(self, value):
        self.frame.stack.append(self.frame.stack[-1])

    def INCLUDE(self, value):
        raise InterpreterError, "Not implemented"

    def INCLUDE_ONCE(self, value):
        raise InterpreterError, "Not implemented"

    def REQUIRE(self, value):
        raise InterpreterError, "Not implemented"

    def REQUIRE_ONCE(self, value):
        raise InterpreterError, "Not implemented"

    def EMPTY_VAR(self, value):
        raise InterpreterError, "Not implemented"

    def EMPTY_RESULT(self, value):
        raise InterpreterError, "Not implemented"

    def NOT(self, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_ARRAY(self, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_BOOL(self, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_DOUBLE(self, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_INT(self, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_OBJECT(self, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_STRING(self, value):
        raise InterpreterError, "Not implemented"

    def CAST_TO_UNSET(self, value):
        raise InterpreterError, "Not implemented"

    def PRE_INCREMENT(self, value):
        var_name = self.frame.stack.pop().str_w()
        try:
            value = self.frame.variables[var_name]
        except KeyError:
            value = self._handle_undefined(var_name)
        new_value = value.inc()
        self.frame.variables[var_name] = new_value
        self.frame.stack.append(new_value)

    def PRE_DECREMENT(self, value):
        var_name = self.frame.stack.pop().str_w()
        try:
            value = self.frame.variables[var_name]
        except KeyError:
            value = self._handle_undefined(var_name)
        new_value = value.dec()
        self.frame.variables[var_name] = new_value
        self.frame.stack.append(new_value)

    def POST_INCREMENT(self, value):
        var_name = self.frame.stack.pop().str_w()
        try:
            value = self.frame.variables[var_name]
        except KeyError:
            value = self._handle_undefined(var_name)
        old_value = value.copy()
        self.frame.variables[var_name] = value.inc()
        self.frame.stack.append(old_value)

    def POST_DECREMENT(self, value):
        var_name = self.frame.stack.pop().str_w()
        try:
            value = self.frame.variables[var_name]
        except KeyError:
            value = self._handle_undefined(var_name)
        old_value = value.copy()
        self.frame.variables[var_name] = value.dec()
        self.frame.stack.append(old_value)

    def DIVIDE(self, value):
        raise InterpreterError, "Not implemented"

    def XOR(self, value):
        raise InterpreterError, "Not implemented"

    def INPLACE_ADD(self, value):
        raise InterpreterError, "Not implemented"

    def INPLACE_SUBSTRACT(self, value):
        raise InterpreterError, "Not implemented"

    def INPLACE_CONCAT(self, var_index):
        var_name = self.frame.stack.pop().str_w()
        concat_value = self.frame.stack.pop()
        try:
            value = self.frame.variables[var_name]
        except KeyError:
            value = self._handle_undefined(var_name)
            # operation itself
        value = value.as_string().concatenate(concat_value.as_string())
        self.frame.variables[var_name] = value
        self.frame.stack.append(value)

    def INPLACE_MULTIPLY(self, value):
        raise InterpreterError, "Not implemented"

    def INPLACE_DIVIDE(self, value):
        raise InterpreterError, "Not implemented"

    def INPLACE_MOD(self, value):
        raise InterpreterError, "Not implemented"

    def LOAD_VAR(self, var_index):
        var_name = self.bytecode.names[var_index]
        self.frame.stack.append(space.str(var_name))

    def STORE_VAR(self, value):
        raise InterpreterError, "Not implemented"

    def LOAD_CONST(self, value):
        self.frame.stack.append(self.bytecode.consts[value].copy())

    def LOAD_NAME(self, index):
        name = self.bytecode.names[index]
        self.frame.stack.append(space.str(name))

    def LOAD_VAR_FAST(self, var_index):
        var_name = self.bytecode.names[var_index]
        try:
            value = self.frame.variables[var_name]
        except KeyError:
            value = self._handle_undefined(var_name)
        self.frame.stack.append(value)

    def STORE_VAR_FAST(self, var_index):
        var_name = self.bytecode.names[var_index]
        value = self.frame.stack[-1] # we need to leave value on the stack
        self.frame.variables[var_name] = value

    def CALL_FUNCTION(self, arguments_number):
        # load function name
        function_name = self.frame.stack.pop().str_w()
        # load function bytecode
        try:
            function = self.context.functions[function_name]
        except KeyError:
            message = "Call to undefined function %s()" % function_name
            raise PHPError(message,
                            PHPError.FATAL,
                            self.bytecode.filename,
                            self._get_line(),
                            self.context.function_trace_stack)

        function_frame = Frame()
        # put function arguments to frame
        arg_position = 1
        for argument in function.arguments:
            if not self.frame.stack:
                message = "Missing argument %s for %s(), called" \
                    % (arg_position, function_name)
                self._warning(message)
            else:
                function_frame.variables[argument] = self.frame.stack.pop()
            arg_position += 1

        # update trace stack and call function
        self.context.function_trace_stack.append(
            (function_name, self._get_line(), function.bytecode.filename)
        )
        return_value = interpret_bytecode(function.bytecode,
                                          self.context,
                                          function_frame)
        self.context.function_trace_stack.pop()

        self.frame.stack.append(return_value)

    def JUMP(self, new_position):
        self.position = new_position

    def JUMP_IF_FALSE(self, new_position):
        value = self.frame.stack.pop()
        if not value.is_true():
            self.position = new_position

    def JUMP_IF_TRUE(self, new_position):
        value = self.frame.stack.pop()
        if value.is_true():
            self.position = new_position

    def ISSET(self, names_count):
        #TODO add array support
        #TODO add __isset() support
        #TODO add PHP 5.4 support
        stack = self.frame.stack
        for i in range(names_count):
            var_name = stack.pop().str_w()
            if not var_name in self.frame.variables:
                stack.append(space.bool(False))
                return
            if self.frame.variables[var_name].is_null():
                stack.append(space.bool(False))
                return
        stack.append(space.bool(True))

    def UNSET(self, names_count):
        #TODO add reference support
        #TODO add global variable support
        #TODO add static variable support
        for i in range(names_count):
            var_name = self.frame.stack.pop().str_w()
            if var_name in self.frame.variables:
                del self.frame.variables[var_name]

    def CONCAT(self, value):
        right = self.frame.stack.pop()
        left = self.frame.stack.pop()
        self.frame.stack.append(space.concat(left, right))

    def _handle_undefined(self, name):
        message = "Undefined variable: %s" % name
        self._notice(message)
        return space.null()

    def _get_line(self):
        return self.bytecode.opcode_lines[self.opcode_position]

    def _error(self, message, type, display = True):
        error = PHPError(message,
                         type,
                         self.bytecode.filename,
                         self._get_line(),
                         self.context.function_trace_stack)
        if display:
            print error

        return error

    def _warning(self, message, display = True):
        self._error(message, PHPError.WARNING, display)

    def _fatal(self, message, display = True):
        self._error(message, PHPError.FATAL, display)

    def _notice(self, message, display = True):
        self._error(message, PHPError.NOTICE, display)

def _new_binary_op(name, space_name):
    def func(self, value):
        right = self.frame.stack.pop()
        left = self.frame.stack.pop()
        try:
            result = getattr(space, space_name)(left, right)
        except DivisionByZero:
            self._warning('Division by zero')
            result = space.bool(False)
        self.frame.stack.append(result)
    func.func_name = name
    return func

for _name in ['ADD', 'SUBSTRACT', 'MULTIPLY', 'MOD', 'LESS_THAN',
              'MORE_THAN', 'LESS_THAN_OR_EQUAL' ,'MORE_THAN_OR_EQUAL', 'EQUAL',
              'NOT_EQUAL', 'IDENTICAL', 'NOT_IDENTICAL']:
    setattr(Interpreter, _name, _new_binary_op(_name, _name.lower()))

def _define_opcodes():
    for index in OPCODE:
        yield index, OPCODE[index]

opcodes = list(_define_opcodes())
unrolling_bc = unrolling_iterable(opcodes)