from pie.error import NoFile, NoFileInIncludePath, NoRequiredFile, \
    NoRequiredFileInIncludePath
from pie.objects.bool import W_BoolObject
import sourcecode
import os.path
from pie.utils.path import split_path

__author__ = 'sery0ga'

class IncludeStatement(object):
    """
    Helps to include php files

    Functionality is different to PHP one, described one
        http://www.php.net/manual/en/function.include.php

    Differences:
        - on successes include*, require* returns bool(true), not int(1)
        - not supported protocols:
          - http://
          - ftp://
          - php://
          - zlib://
          - data://
          - rar://
          - glob://
          - phar://
          - ssh2://
          - ogg://
          - expect://
          - file://

    TODO: add support for multiple protocols (???)
    """
    (INCLUDE, INCLUDE_ONCE, REQUIRE, REQUIRE_ONCE) = ("include", "include_once",
        "require", "require_once")

    def __init__(self, context, frame):
        self.context = context
        self.frame = frame

        self.full_filename = ''
        self.include_paths_were_searched = False
        self.include_type = self.INCLUDE

    def include_once(self, path):
        if self._is_path_empty(path):
            return self._handle_error()
        self.path = path
        if path in self.context.include_cache:
            # File is already included. Don't parse or interpret it
            return W_BoolObject(True)
        else:
            self.context.include_cache[path] = 1
        self.include_type = self.INCLUDE_ONCE
        return self._handle_include()

    def require_once(self, path):
        if self._is_path_empty(path):
            return self._handle_error()
        self.path = path
        if path in self.context.include_cache:
            # File is already included. Don't parse or interpret it
            return W_BoolObject(True)
        else:
            self.context.include_cache[path] = 1
        self.include_type = self.REQUIRE_ONCE
        return self._handle_include()

    def require(self, path):
        if self._is_path_empty(path):
            return self._handle_error()
        self.path = path
        if path not in self.context.include_cache:
            self.context.include_cache[path] = 1
        self.include_type = self.REQUIRE
        return self._handle_include()

    def include(self, path):
        if self._is_path_empty(path):
            return self._handle_error()
        self.path = path
        #TODO: add better cache support with blackjack and whores
        if path not in self.context.include_cache:
            self.context.include_cache[path] = 1
        return self._handle_include()

    def _handle_include(self):
        """
        Include and interpret PHP file

        If you find something strange in behaviour of this function, please,
        look PHP documentation at http://www.php.net/manual/en/function.include.php
        """
        found = self._check_path()
        if not found:
            return self._handle_error()

        try:
            source = sourcecode.SourceCode(self.full_filename)
            source.open()
        except OSError:
            #TODO: change error message. 'Cannot open/read file' should be
            error = NoFile(self.context, self.include_type, self.path)
            error.handle()
            return W_BoolObject(False)

        bytecode = source.compile()
        self.context.trace.append(self.include_type, bytecode)
        self.context.initialize_functions(bytecode)
        w_return_value = sourcecode.interpret_bytecode(bytecode, self.context, self.frame)
        self.context.trace.pop()
        if w_return_value.is_null():
            return W_BoolObject(True)
        return w_return_value

    def _is_path_empty(self, path):
        if not path.strip(' '):
            return True
        return False

    def _check_path(self):
        # First we detect if path is defined or not. It determines by which way
        # we will resolve file inclusion
        (directory, filename) = split_path(self.path)
        found = False
        if not directory:
            found = self._check_include_path(filename)
            if not found:
                found = self._check_calling_script_path(filename)
        # At last check current working directory
        if not found and os.path.isfile(self.path):
            found = True
            self.full_filename = self.path

        return found

    def _check_include_path(self, filename):
        """
        Search for requested file in all directories from include_path
        """
        self.include_paths_were_searched = True
        for path_to_check in self.context.config.include_path:
            filename_to_check = path_to_check + '/' + filename
            if os.path.isfile(filename_to_check):
                self.full_filename = filename_to_check
                return True

        return False

    def _check_calling_script_path(self, filename):
        filename_to_check = self.context.config.calling_script_path + '/' + filename
        if os.path.isfile(filename_to_check):
            self.full_filename = filename_to_check
            return True

        return False

    def _handle_error(self):
        if self.include_type == self.INCLUDE or self.include_type == self.INCLUDE_ONCE:
            return self._handle_include_error()
        else:
            return self._handle_require_error()

    def _handle_require_error(self):
        error = NoRequiredFile(self.context, self.include_type, self.path)
        error.handle()
        if self.include_paths_were_searched:
            include_path = ':'.join(self.context.config.include_path)
            error = NoRequiredFileInIncludePath(self.context, self.include_type,
                self.path, include_path)
            error.handle()
            raise error
        raise error

    def _handle_include_error(self):
        error = NoFile(self.context, self.include_type, self.path)
        error.handle()
        if self.include_paths_were_searched:
            include_path = ':'.join(self.context.config.include_path)
            error = NoFileInIncludePath(self.context, self.include_type, self.path, include_path)
            error.handle()
        return W_BoolObject(False)
