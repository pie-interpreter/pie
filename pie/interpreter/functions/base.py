" Module with base class for function classes "


class AbstractFunction(object):
    "Interface for all functions"

    def __init__(self, name):
        self.name = name

    def call(self, context, stack_values):
        raise NotImplementedError
