import os.path
import sourcecode
from abc import ABCMeta, abstractmethod
from pypy.rlib.objectmodel import specialize
from pie.objects.bool import W_BoolObject
from pie.utils.path import split_path
from pie.interpreter.errors.warnings import NoFile, NoFileInIncludePath
from pie.interpreter.errors.fatalerrors import NoRequiredFile, NoRequiredFileInIncludePath

__author__ = 'sery0ga'

cache = {}


@specialize.memo()
def _get_strategy(strategy):
    """
    Helps to cache strategies' objects
    """
    try:
        return cache[strategy]
    except KeyError:
        new_strategy = strategy()
        cache[strategy] = new_strategy
        return new_strategy


class FileNotFound(Exception):
    pass


class FileReadFailure(Exception):
    pass


class BaseErrorStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle_error(self, context, function_name, filename):
        pass


class IncludeErrorStrategy(BaseErrorStrategy):

    def handle_error(self, context, function_name, filename):
        NoFile(context, function_name, filename).handle()


class RequireErrorStrategy(BaseErrorStrategy):

    def handle_error(self, context, function_name, filename):
        NoRequiredFile(context, function_name, filename).handle()


class IncludeWithPathErrorStrategy(IncludeErrorStrategy):

    def handle_error(self, context, function_name, filename):
        IncludeErrorStrategy.handle_error(self, context, function_name, filename)
        NoFileInIncludePath(
            context, function_name, filename, context.config.get('include_path')
            ).handle()


class RequireWithPathErrorStrategy(RequireErrorStrategy):

    def handle_error(self, context, function_name, filename):
        RequireErrorStrategy.handle_error(self, context, function_name, filename)
        NoRequiredFileInIncludePath(
            context, function_name, filename, context.config.get('include_path')
            ).handle()


class BaseIncludeStatement(object):
    """
    Helps to include php files

    Functionality is different to PHP one, described one
        http://www.php.net/manual/en/function.include.php

    Differences:
        - on successes include*, require* returns bool(true), not int(1)
        - no protocol is supported

    TODO: add support for multiple protocols (???)
    """
    __metaclass__ = ABCMeta

    def __init__(self, context, frame):
        self.context = context
        self.frame = frame

    def include(self, filename):
        try:
            absolute_filename = os.path.abspath(self._search(filename))
        except FileNotFound:
            self._handle_error(filename)
            return W_BoolObject(False)

        (in_cache, update_cache) = (False, False)
        try:
            source = self.context.include_cache[absolute_filename]
            in_cache = True
        except KeyError:
            source = None
            update_cache = True

        if in_cache:
            #TODO: file change time support should be added.
            pass
        if self._return_if_file_in_cache(in_cache):
            return W_BoolObject(True)

        if update_cache:
            try:
                source = self._get_source(absolute_filename)
            except FileReadFailure:
                return W_BoolObject(False)

            self.context.include_cache[absolute_filename] = source

        return self._interpret(source)

    def _search(self, filename):
        """
        Search file in include_path, working dir and calling script path.

        For detail logic description visit
            http://www.php.net/manual/en/function.include.php
        """
        # First we detect if path is defined or not. It determines by which way
        # we will resolve file inclusion
        if not filename.strip(' '):
            raise FileNotFound(filename)

        (directory, dummy_filename) = split_path(filename)
        if not directory or directory[0] not in ['.', '/']:
            self._switch_error_strategy()
            return self._search_in_possible_directories(filename)
        elif os.path.isfile(filename):
            return filename

        raise FileNotFound(filename)

    def _search_in_possible_directories(self, filename):
        for path_to_check in self.context.config.get_include_path():
            filename_to_check = path_to_check + '/' + filename
            if os.path.isfile(filename_to_check):
                return filename_to_check
        filename_to_check = self.context.calling_script_path + '/' + filename
        if os.path.isfile(filename_to_check):
            return filename_to_check
        if os.path.isfile(filename):
            return filename

        raise FileNotFound(filename)

    def _get_source(self, filename):
        try:
            source = sourcecode.SourceCode(filename)
            source.open()
        except OSError:
            #TODO: change error message. 'Cannot open/read file' should be
            NoFile(self.context, self._get_statement_name(), filename).handle()
            raise FileReadFailure()

        return source

    def _interpret(self, source):
        self.context.trace.append(self._get_statement_name(), source.filename)
        w_return_value = source.interpret(self.context, self.frame)
        self.context.trace.pop()

        if w_return_value.deref().is_null():
            return W_BoolObject(True)

        return w_return_value

    def _handle_error(self, filename):
        self.error_strategy.handle_error(
            self.context, self._get_statement_name(), filename)

    @abstractmethod
    def _return_if_file_in_cache(self, is_in_cache):
        return False

    @abstractmethod
    def _switch_error_strategy(self):
        pass

    @abstractmethod
    def _get_statement_name(self):
        return ''


class IncludeStatement(BaseIncludeStatement):

    def __init__(self, context, frame):
        BaseIncludeStatement.__init__(self, context, frame)
        self.error_strategy = _get_strategy(IncludeErrorStrategy)

    def _return_if_file_in_cache(self, is_in_cache):
        return False

    def _switch_error_strategy(self):
        self.error_strategy = _get_strategy(IncludeWithPathErrorStrategy)

    def _get_statement_name(self):
        return "include"


class RequireStatement(BaseIncludeStatement):

    def __init__(self, context, frame):
        BaseIncludeStatement.__init__(self, context, frame)
        self.error_strategy = _get_strategy(RequireErrorStrategy)

    def _return_if_file_in_cache(self, is_in_cache):
        return False

    def _switch_error_strategy(self):
        self.error_strategy = _get_strategy(RequireWithPathErrorStrategy)

    def _get_statement_name(self):
        return "require"


class IncludeOnceStatement(BaseIncludeStatement):

    def __init__(self, context, frame):
        BaseIncludeStatement.__init__(self, context, frame)
        self.error_strategy = _get_strategy(IncludeErrorStrategy)

    def _return_if_file_in_cache(self, is_in_cache):
        return is_in_cache

    def _switch_error_strategy(self):
        self.error_strategy = _get_strategy(IncludeWithPathErrorStrategy)

    def _get_statement_name(self):
        return "include_once"


class RequireOnceStatement(BaseIncludeStatement):

    def __init__(self, context, frame):
        BaseIncludeStatement.__init__(self, context, frame)
        self.error_strategy = _get_strategy(RequireErrorStrategy)

    def _return_if_file_in_cache(self, is_in_cache):
        return is_in_cache

    def _switch_error_strategy(self):
        self.error_strategy = _get_strategy(RequireWithPathErrorStrategy)

    def _get_statement_name(self):
        return "require_once"
