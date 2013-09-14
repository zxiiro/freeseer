import ConfigParser

from ..core import ConfigStorage


class ConfigParserStorage(ConfigStorage):
    def load(self, config_instance, section):
        parser = ConfigParser.ConfigParser()
        parser.read([self._filepath])

        for name, option in config_instance.options.iteritems():
            if not parser.has_option(section, name):
                continue
            raw = parser.get(section, name)
            clean = option.decode(raw)
            config_instance.set_value(name, option, clean)
        return config_instance

    def store(self, config_instance, section):
        parser = ConfigParser.ConfigParser()
        parser.read([self._filepath])

        if not parser.has_section(section):
            parser.add_section(section)
  
        for name, option in config_instance.options.iteritems():
            raw = config_instance.get_value(name, option)
            clean = option.encode(raw)
            parser.set(section, name, clean)

        with open(self._filepath, 'wc') as config_fd:
            parser.write(config_fd)
