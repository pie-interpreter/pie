import os.path
from pie.config import config
from pie.utils.path import split_path
from pie.interpreter.errors.fatalerrors import RedeclaredFunction, RedeclaredUserFunction


class SharedContext(object):
    "Context data, that is shared between all other contexts"

    def __init__(self):
        self.functions = {}

shared_context = SharedContext()


class Context(object):

    def __init__(self, filename):
        self.functions = shared_context.functions.copy()
        self.include_cache = {}
        self.config = config.copy()
        self.trace = Trace(filename)
        self.calling_script_path, self.calling_script = split_path(filename)

    def declare_function(self, function):
        name = function.name
        if name in self.functions:
            from pie.interpreter.function import UserFunction
            if isinstance(self.functions[name], UserFunction):
                RedeclaredUserFunction(
                    self, function, self.functions[name]).handle()
            else:
                RedeclaredFunction(self, function).handle()

        else:
            self.functions[function.name] = function


class Trace(object):

    def __init__(self, filename):
        self.line = 0
        self.stack = [('{main}', filename, 0)]

    def append(self, function_name, filename):
        self.stack.append((function_name, filename, self.line))

    def pop(self):
        assert self.stack, 'You can\'t pop an empty stack trace'
        self.stack.pop()

    def to_string(self):
        lines = []
        if self.stack:
            lines.append('PHP Stack trace:\n')
            for depth, entry in enumerate(self.stack):
                function_name, filename, line = entry
                lines.append(
                    'PHP   %s. %s() %s:%s\n' \
                        % ((depth + 1),
                            function_name,
                            os.path.abspath(filename),
                            line)
                        )

        return ''.join(lines)
