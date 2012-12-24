import os.path
import sys


class PieError(Exception):
    "Base class for app-level errors exceptions"

    level = 0
    severity = ''

    def __init__(self, context, message, additional_message=''):
        self.message = message
        self.context = context
        self.additional_message = additional_message

    def __repr__(self):
        return self.get_message()

    def __str__(self):
        return self.get_message()

    def handle(self):
        if self.level & int(self.context.config.get('error.fatal_level', 1023)):
            raise self

        if self.level & int(self.context.config.get('errors.display_level', 1023)):
            sys.stderr.write(self.get_message())

    def get_message(self):
        message = "PHP %s:  %s in %s on line %s %s\n" \
            % (self.severity,
                self.message,
                self.get_filename(),
                self.get_line(),
                self.get_additional_message())

        if self.context.config.get('error.print_trace', True):
            message = ''.join([message, self.context.trace.to_string()])

        return message

    def get_filename(self):
        __, filename, __ = self.context.trace.stack[-1]
        return os.path.abspath(filename)

    def get_line(self):
        return self.context.trace.line

    def get_additional_message(self):
        return ''


class Fatal(PieError):

    level = 1 << 0
    severity = 'Fatal error'


class Warning(PieError):

    level = 1 << 1
    severity = 'Warning'


class Notice(PieError):

    level = 1 << 2
    severity = 'Notice'


class Parse(PieError):

    level = 1 << 3
    severity = 'Parse error'
