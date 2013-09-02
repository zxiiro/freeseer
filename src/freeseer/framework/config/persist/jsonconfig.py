import json

from ..core import Config


class JSONConfig(Config):
    def __init__(self, filename):
        self._filename = filename
        super(JSONConfig, self).__init__()

    def load(self):
        with open(self._filename) as config_fd:
            raw_config = json.load(config_fd)

        for name, option in self.options.iteritems():
            if name in raw_config:
                raw = raw_config[name]
                clean = option.decode(raw)
                self.set_value(name, option, clean)

    def save(self):
        raw_config = {}
        for name, option in self.options.iteritems():
            raw = self.get_value(name, option)
            clean = option.encode(raw)
            raw_config[name] = clean

        with open(self._filename, 'wc') as config_fd:
            clean_json = json.dumps(raw_config,
                                    sort_keys=True,
                                    indent=4,
                                    separators=(',', ': '))
            config_fd.write(clean_json)
