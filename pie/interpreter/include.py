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

        self.filename = ''
        self.include_paths_were_searched = False
        self.update_cache = False
        self.include_type = self.INCLUDE

    def include_once(self, path):
        self.include_type = self.INCLUDE_ONCE
        return self._include_one_time(path)

    def require_once(self, path):
        self.include_type = self.REQUIRE_ONCE
        return self._include_one_time(path)

    def require(self, path):
        self.include_type = self.REQUIRE
        return self._include_many_times(path)

    def include(self, path):
        return self._include_many_times(path)

    def _include_one_time(self, path):
        result = self._check_path(path)
        if not result:
            return W_BoolObject(False)
        if self.filename in self.context.include_cache:
            # File is already included. Don't parse or interpret it
            return W_BoolObject(True)
        else:
            #TODO: file change time support should be added.
            self.update_cache = True

        return self._handle_include(path)

    def _include_many_times(self, path):
        result = self._check_path(path)
        if not result:
            return W_BoolObject(False)
        if self.filename not in self.context.include_cache:
            #TODO: file change time support should be added.
            self.update_cache = True

        return self._handle_include(path)

    def _check_path(self, path):
        if not path.strip(' '):
            return self._handle_error(path)
        file_found = self._check_nonempty_path(path)
        if not file_found:
            return self._handle_error(path)
        self.filename = os.path.abspath(self.filename)

        return True

    def _handle_include(self, path):
        """
        Include and interpret PHP file

        If you find something strange in behaviour of this function, please,
        look PHP documentation at http://www.php.net/manual/en/function.include.php
        """
        if not self.update_cache:
            source = self.context.include_cache[self.filename]
        else:
            try:
                source = sourcecode.SourceCode(self.filename, self.include_type)
                source.open()
            except OSError:
                #TODO: change error message. 'Cannot open/read file' should be
                error = NoFile(self.context, self.include_type, path)
                error.handle()
                return W_BoolObject(False)
            source.compile()
            self.context.include_cache[self.filename] = source

        w_return_value = source.interpret(self.context, self.frame)

        if w_return_value.is_null():
            return W_BoolObject(True)
        return w_return_value

    def _check_nonempty_path(self, path):
        """
        Search file in include_path, working dir and calling script path.

        For detail logic description visit
            http://www.php.net/manual/en/function.include.php
        """
        # First we detect if path is defined or not. It determines by which way
        # we will resolve file inclusion
        (directory, filename) = split_path(path)
        found = False
        if not directory:
            found = self._check_include_path(filename)
            if not found:
                found = self._check_calling_script_path(filename)
        # At last check current working directory
        if not found and os.path.isfile(path):
            found = True
            self.filename = path

        return found

    def _check_include_path(self, filename):
        """
        Search for requested file in all directories from include_path
        """
        self.include_paths_were_searched = True
        for path_to_check in self.context.config.include_path:
            filename_to_check = path_to_check + '/' + filename
            if os.path.isfile(filename_to_check):
                self.filename = filename_to_check
                return True

        return False

    def _check_calling_script_path(self, filename):
        filename_to_check = self.context.config.calling_script_path + '/' + filename
        if os.path.isfile(filename_to_check):
            self.filename = filename_to_check
            return True

        return False

    def _handle_error(self, path):
        if self.include_type == self.INCLUDE or self.include_type == self.INCLUDE_ONCE:
            return self._handle_include_error(path)
        else:
            return self._handle_require_error(path)

    def _handle_require_error(self, path):
        error = NoRequiredFile(self.context, self.include_type, path)
        error.handle()
        if self.include_paths_were_searched:
            include_path = ':'.join(self.context.config.include_path)
            error = NoRequiredFileInIncludePath(self.context, self.include_type,
                path, include_path)
            error.handle()
            raise error
        raise error

    def _handle_include_error(self, path):
        error = NoFile(self.context, self.include_type, path)
        error.handle()
        if self.include_paths_were_searched:
            include_path = ':'.join(self.context.config.include_path)
            error = NoFileInIncludePath(self.context, self.include_type, path, include_path)
            error.handle()
        return False
