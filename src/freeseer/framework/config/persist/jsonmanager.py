import json
import os

from ..core import ConfigStorage


class JSONConfigStorage(ConfigStorage):
    def parse_json(self):
        if os.path.isfile(self._filepath):
            return json.load(open(self._filepath))
        else:
            return {}

    def write_json(self, dct):
        with open(self._filepath, 'wc') as config_fd:
            config_fd.write(json.dumps(dct,
                                       sort_keys=True,
                                       indent=4,
                                       separators=(',', ': ')))

    def load(self, config_instance, section):
        dct = self.parse_json()
        if section not in dct:
            return config_instance

        for name, option in config_instance.options.iteritems():
            if name not in dct[section]:
                continue
            raw = dct[section][name]
            clean = option.decode(raw)
            config_instance.set_value(name, option, clean)
        return config_instance

    def store(self, config_instance, section):
        dct = self.parse_json()
        if section not in dct:
            dct[section] = {}

        for name, option in config_instance.options.iteritems():
            raw = config_instance.get_value(name, option)
            clean = option.encode(raw)
            dct[section][name] = clean

        self.write_json(dct)
