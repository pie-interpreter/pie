from pie.utils.ini import raw_parse_ini_file
from pie.utils.path import split_path
from pypy.rlib.parsing.parsing import ParseError
from pypy.rlib.objectmodel import instantiate
import string

__author__ = 'sery0ga'

DEFAULT_CONFIG_PATH = 'conf/pie.ini'

config = None


class PHPConfiguration(object):
    """
    This class is a simple way to manage multiple PHP settings
    which could be changed through configuration files or
    at runtime
    """

    def __init__(self):
        self.display_errors = True
        self.display_to_stderr = False
        self.include_path = ['.', '/usr/share/php']
        self.calling_script_path = ''
        self.calling_script = ''
        self._initialize(self._read_config_file())

    def display_error(self, error):
        #TODO: add error level filter
        if self.display_errors:
            return True
        return False

    def set_include_path(self, path):
        if not isinstance(path, str):
            raise Exception("Include path should be a string")
        #TODO add windows support (';')
        self.include_path = string.split(path, ':')

    def set_calling_file(self, calling_file):
        self.calling_script_path, self.calling_script = split_path(calling_file)

    def copy(self):
        copy = instantiate(PHPConfiguration)
        copy.display_errors = self.display_errors
        copy.display_to_stderr = self.display_to_stderr
        copy.include_path = self.include_path[:]
        copy.calling_script_path = self.calling_script_path[:]
        copy.calling_script = self.calling_script[:]

        return copy

    def _read_config_file(self):
        #TODO: add errors printing
        try:
            return raw_parse_ini_file(DEFAULT_CONFIG_PATH)
        except IOError:
            return {}
        except ParseError:
            return {}

    def _initialize(self, mapped_config):
        if 'PHP' in mapped_config:
            if 'display_errors' in mapped_config['PHP'] and \
                mapped_config['PHP']['display_errors'] == 'on':
                self.display_errors = True
            else:
                self.display_errors = False
            if 'include_path' in mapped_config['PHP']:
                self.set_include_path(mapped_config['PHP']['include_path'])


config = PHPConfiguration()
