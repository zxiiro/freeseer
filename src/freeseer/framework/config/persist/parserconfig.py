import ConfigParser
import os

from ..core import Config


class ParserConfig(Config):
    def __init__(self, filename, section):
        self._filename = filename
        self._section = section
        super(ParserConfig, self).__init__()

    def load(self):
        parser = ConfigParser.ConfigParser()
        parser.read([self._filename])
        for name, option in self.options.iteritems():
            raw = parser.get(self._section, name)
            clean = option.decode(raw)
            self.set_value(name, option, clean)

    def load_if_possible(self):
        if os.path.isfile(self._filename):
            self.load()

    def save(self):
        parser = ConfigParser.ConfigParser()
        parser.add_section(self._section)
        for name, option in self.options.iteritems():
            raw = self.get_value(name, option)
            clean = option.encode(raw)
            parser.set(self._section, name, clean)
        with open(self._filename, 'wc') as config_fd:
            parser.write(config_fd)
