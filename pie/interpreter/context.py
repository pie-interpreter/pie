from pie.error import RedeclaredFunction
from pie.utils.path import split_path
from pie.launcher.config import config

__author__ = 'sery0ga'


class Context:

    def __init__(self, calling_file):
        self.functions = {}
        self.trace = Trace()
        self.config = config.copy()
        self.include_cache = {}
        self.calling_script_path, self.calling_script = split_path(calling_file)

    def initialize_functions(self, bytecode):
        for name, object in bytecode.functions.iteritems():
            try:
                function = self.functions[name]
                error = RedeclaredFunction(self, name, function)
                error.handle()
                raise error
            except KeyError:
                self.functions[name] = object


class Trace:

    def __init__(self):
        self.stack = []
        self.current_execution_block = None

    def update_position(self, position):
        self.current_execution_block.position = position

    def append(self, function_name, bytecode):
        if self.current_execution_block:
            self.stack.append(self.current_execution_block)
        else:
            function_name = "{main}"

        self.current_execution_block = ExecutionBlock(function_name, bytecode)

    def pop(self):
        if self.stack:
            self.current_execution_block = self.stack.pop()

    def to_string(self):
        message = ''
        if self.stack:
            message = "\nPHP Stack trace:\n"
            depth = 1
            for execution_block in self.stack:
                message = ''.join([message, execution_block.to_string(depth)])
                depth += 1

            message = ''.join([message, self.current_execution_block.to_string(depth)])

        return message


class ExecutionBlock:

    def __init__(self, function_name='', bytecode=None, position=0):
        self.function_name = function_name
        self.bytecode = bytecode
        self.position = position

    def get_line(self):
        assert self.position >= 0
        return self.bytecode.opcode_lines[self.position]

    def get_filename(self):
        return self.bytecode.filename

    def to_string(self, depth=0):
        import os.path
        message = "PHP   %s. %s() %s:%s\n"\
            % (depth, self.function_name, os.path.abspath(
                self.get_filename()),
                self.get_line())

        return message
