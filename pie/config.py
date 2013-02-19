import string

from rpython.rlib.parsing.parsing import ParseError
from rpython.rlib.objectmodel import instantiate

from pie.utils.ini import raw_parse_ini_file

DEFAULT_CONFIG_PATH = 'conf/pie.ini'


class PieConfiguration(object):
    """
    This class is a simple way to manage multiple Pie settings
    which could be changed through configuration files or
    at runtime
    """

    DEFAULT_SECTION = 'pie'

    def __init__(self):
        self.configuration = self._read_config_file()

    def get(self, key, default=None):
        return self.sectionget(self.DEFAULT_SECTION, key, default)

    def sectionget(self, section, key, default):
        try:
            config_section = self.configuration[section]
            return config_section.get(key, default)
        except KeyError:
            return default

    def set(self, key, value):
        self.sectionset(self.DEFAULT_SECTION, key, value)

    def sectionset(self, section, key, value):
        try:
            config_section = self.configuration[section]
            config_section[key] = value
        except KeyError:
            self.configuration[section] = {key: value}

    def get_include_path(self):
        " Get list of all include paths "
        include_path = self.get('include_path', '')
        return string.split(include_path, ':')

    def copy(self):
        copy = instantiate(PieConfiguration)
        copy.configuration = self.configuration.copy()

        return copy

    def _read_config_file(self):
        #TODO: add errors printing
        try:
            return raw_parse_ini_file(DEFAULT_CONFIG_PATH)
        except IOError:
            return {}
        except ParseError:
            return {}


config = PieConfiguration()
