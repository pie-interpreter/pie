import os

from pypy.rlib.objectmodel import we_are_translated
from pypy.rlib.unroll import unrolling_iterable

from pie.objspace import space
from pie.opcodes import OPCODE_INDEX_DIVIDER, get_opcode_name, OPCODE
from pie.objects.base import DivisionByZeroError
from pie.objects.variable import W_Variable
from pie.interpreter.errors.base import InternalError
from pie.interpreter.errors.noticeerrors import NonVariableReturnedByReference
from pie.interpreter.errors.warningerrors import DivisionByZero
from pie.interpreter.errors.fatalerrors import UndefinedFunction
import pie.interpreter.include as include


class Interpreter(object):

    RETURN_FLAG = -1

    def __init__(self, bytecode, context, frame):
        self.bytecode = bytecode
        self.frame = frame
        self.context = context
        self.position = 0

    def interpret(self):
        self.declare_functions()

        code = self.bytecode.code
        bytecode_length = len(self.bytecode.code)

        while True:
            if self.position >= bytecode_length:
                break

            self.context.trace.line = self.bytecode.opcode_lines[self.position]

            opcode_index = ord(code[self.position])
            self.position += 1

            if opcode_index > OPCODE_INDEX_DIVIDER:
                arg = ord(code[self.position]) \
                    + (ord(code[self.position + 1]) << 8)
                self.position += 2
            else:
                arg = 0  # don't make it negative

            assert arg >= 0

            if we_are_translated():
                for index, name in unrolling_bc:
                    if index == opcode_index:
                        getattr(self, name)(arg)
                        break
                else:
                    raise InternalError("Unknown opcode")
            else:
                opcode_name = get_opcode_name(opcode_index)
                getattr(self, opcode_name)(arg)

            # this is a return condition
            if self.position == self.RETURN_FLAG:
                break

    def declare_functions(self):
        for function in self.bytecode.declared_functions:
            self.context.declare_function(function)

    def ECHO(self, value):
        w_value = self.frame.stack.pop()
        os.write(1, w_value.deref().as_string().str_w())

    def PRINT(self, value):
        w_value = self.frame.stack.pop()
        os.write(1, w_value.deref().as_string().str_w())
        self.frame.stack.append(space.int(1))

    def RETURN(self, value):
        self.position = self.RETURN_FLAG

    def POP_STACK(self, value):
        self.frame.stack.pop()

    def DUPLICATE_TOP(self, value):
        self.frame.stack.append(self.frame.stack[-1])

    def EMPTY_VAR(self, value):
        #TODO: array support
        #TODO: object support
        name = self.frame.pop_name()
        if name not in self.frame.variables:
            w_result = space.bool(True)
        else:
            w_value = self.frame.get_variable(name, self.context)
            w_result = space.is_empty(w_value)
        self.frame.stack.append(w_result)

    def EMPTY_RESULT(self, value):
        w_value = self.frame.stack.pop()
        self.frame.stack.append(space.is_empty(w_value))

    def MAKE_REFERENCE(self, value):
        ref_name = self.frame.pop_name()
        w_variable = self.frame.stack.pop()

        if not isinstance(w_variable, W_Variable):
            NonVariableReturnedByReference(self.context).handle()
            self.frame.set_variable(ref_name, w_variable)
            self.frame.stack.append(w_variable)
        else:
            self.frame.variables[ref_name] = w_variable
            self.frame.stack.append(w_variable.deref())

    def NOT(self, value):
        raise InternalError("Not implemented")

    def CAST_TO_ARRAY(self, value):
        raise InternalError("Not implemented")

    def CAST_TO_BOOL(self, value):
        w_object = self.frame.stack.pop()
        self.frame.stack.append(w_object.as_bool())

    def CAST_TO_DOUBLE(self, value):
        w_object = self.frame.stack.pop()
        self.frame.stack.append(w_object.as_float())

    def CAST_TO_INT(self, value):
        w_object = self.frame.stack.pop()
        self.frame.stack.append(w_object.as_int())

    def CAST_TO_OBJECT(self, value):
        raise InternalError("Not implemented")

    def CAST_TO_STRING(self, value):
        w_object = self.frame.stack.pop()
        self.frame.stack.append(w_object.as_string())

    def CAST_TO_UNSET(self, value):
        self.frame.stack.pop()  # Don't need to keep value
        self.frame.stack.append(space.null())

    def PRE_INCREMENT(self, value):
        w_value = self.frame.pop_and_get(self.context)
        w_new_value = w_value.deref().inc()
        w_value.set_value(w_new_value)
        self.frame.stack.append(w_new_value)

    def PRE_DECREMENT(self, value):
        w_value = self.frame.pop_and_get(self.context)
        w_new_value = w_value.deref().dec()
        w_value.set_value(w_new_value)
        self.frame.stack.append(w_new_value)

    def POST_INCREMENT(self, value):
        w_value = self.frame.pop_and_get(self.context)
        w_old_value = w_value.deref().copy()
        w_value.set_value(w_value.deref().inc())
        self.frame.stack.append(w_old_value)

    def POST_DECREMENT(self, value):
        w_value = self.frame.pop_and_get(self.context)
        w_old_value = w_value.deref().copy()
        w_value.set_value(w_value.deref().dec())
        self.frame.stack.append(w_old_value)

    def XOR(self, value):
        raise InternalError("Not implemented")

    def INPLACE_CONCAT(self, var_index):
        var_name = self.frame.pop_name()
        w_concat_value = self.frame.stack.pop()
        w_value = self.frame.get_variable(var_name, self.context).deref()
        # operation itself
        w_value = w_value.as_string().concatenate(w_concat_value.as_string())
        self.frame.set_variable(var_name, w_value)
        self.frame.stack.append(w_value)

    def LOAD_VAR(self, var_index):
        var_name = self.bytecode.names[var_index]
        w_value = self.frame.get_variable(var_name, self.context)
        self.frame.stack.append(w_value)

    def STORE_VAR(self, value):
        raise InternalError("Not implemented")

    def LOAD_CONST(self, value):
        self.frame.stack.append(self.bytecode.consts[value].copy())

    def LOAD_NAME(self, index):
        name = self.bytecode.names[index]
        self.frame.stack.append(space.str(name))

    def LOAD_VAR_FAST(self, var_index):
        var_name = self.bytecode.names[var_index]
        w_value = self.frame.get_variable(var_name, self.context)
        self.frame.stack.append(w_value)

    def STORE_VAR_FAST(self, var_index):
        var_name = self.bytecode.names[var_index]
        w_value = self.frame.stack[-1]  # we need to leave value on the stack
        self.frame.set_variable(var_name, w_value)

    def DECLARE_FUNCTION(self, function_index):
        function = self.bytecode.functions[function_index]
        self.context.declare_function(function)

    def CALL_FUNCTION(self, arguments_number):
        function_name = self.frame.pop_name()
        if function_name not in self.context.functions:
            UndefinedFunction(self.context, function_name).handle()
            self.frame.stack.append(space.null())
            return

        parameters = []
        for index in range(arguments_number):
            parameters.append(self.frame.stack.pop())

        function = self.context.functions[function_name]
        w_return_value = function.call(self.context, parameters)

        self.frame.stack.append(w_return_value)

    def JUMP(self, new_position):
        self.position = new_position

    def JUMP_IF_FALSE(self, new_position):
        w_value = self.frame.stack.pop()
        if not w_value.is_true():
            self.position = new_position

    def JUMP_IF_TRUE(self, new_position):
        w_value = self.frame.stack.pop()
        if w_value.is_true():
            self.position = new_position

    def ISSET(self, names_count):
        #TODO: add array support
        #TODO: add __isset() support
        #TODO: add PHP 5.4 support
        stack = self.frame.stack
        for i in range(names_count):
            var_name = stack.pop().str_w()
            if not var_name in self.frame.variables:
                stack.append(space.bool(False))
                return
            if self.frame.variables[var_name].deref().is_null():
                stack.append(space.bool(False))
                return
        stack.append(space.bool(True))

    def UNSET(self, names_count):
        #TODO: add reference support
        #TODO: add global variable support
        #TODO: add static variable support
        for i in range(names_count):
            var_name = self.frame.pop_name()
            if var_name in self.frame.variables:
                del self.frame.variables[var_name]

    def CONCAT(self, value):
        w_right = self.frame.stack.pop()
        w_left = self.frame.stack.pop()
        self.frame.stack.append(space.concat(w_left, w_right))


def _new_binary_op(name, space_name):
    def func(self, value):
        w_right = self.frame.stack.pop()
        w_left = self.frame.stack.pop()
        try:
            w_result = getattr(space, space_name)(w_left, w_right)
        except DivisionByZeroError:
            DivisionByZero(self.context).handle()
            w_result = space.bool(False)

        self.frame.stack.append(w_result)
    func.func_name = name

    return func

for name in ['ADD', 'SUBSTRACT', 'MULTIPLY', 'MOD', 'DIVIDE', 'LESS_THAN',
              'MORE_THAN', 'LESS_THAN_OR_EQUAL', 'MORE_THAN_OR_EQUAL', 'EQUAL',
              'NOT_EQUAL', 'IDENTICAL', 'NOT_IDENTICAL']:
    setattr(Interpreter, name, _new_binary_op(name, name.lower()))


def _new_inplace_op(name, space_name):
    def func(self, value):
        w_value = self.frame.pop_and_get(self.context)
        w_right = self.frame.stack.pop()
        try:
            w_result = getattr(space, space_name)(w_value, w_right)
        except DivisionByZeroError:
            DivisionByZero(self.context).handle()
            w_result = space.bool(False)

        w_value.set_value(w_result)
        self.frame.stack.append(w_result)
    func.func_name = name

    return func

for name in ['ADD', 'SUBSTRACT', 'MULTIPLY', 'MOD', 'DIVIDE']:
    operation_name = 'INPLACE_' + name
    setattr(Interpreter, operation_name, _new_inplace_op(
        operation_name, name.lower()))


def _new_include_op(name, include_class):
    def func(self, value):
        filename = self.frame.pop_name()
        statement = include_class(self.context, self.frame)
        w_result = statement.include(filename)
        self.frame.stack.append(w_result)
    func.func_name = name

    return func

for name, include_class in [
        ('INCLUDE', include.IncludeStatement),
        ('INCLUDE_ONCE', include.IncludeOnceStatement),
        ('REQUIRE', include.RequireStatement),
        ('REQUIRE_ONCE', include.RequireOnceStatement)
    ]:
    setattr(Interpreter, name, _new_include_op(name, include_class))


def _define_opcodes():
    for index in OPCODE:
        yield index, OPCODE[index]

opcodes = list(_define_opcodes())
unrolling_bc = unrolling_iterable(opcodes)
