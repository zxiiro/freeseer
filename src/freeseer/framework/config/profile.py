import os

from freeseer.framework.config.persist import ConfigParserStorage
from freeseer.framework.config.persist import JSONConfigStorage
from freeseer.framework.database import QtDBConnector


class ProfileManager(object):
    def __init__(self, base_folder):
        self._base_folder = base_folder
        self._cache = {}
        self._create_if_needed(base_folder)

    def _create_if_needed(self, path):
        try:
            os.makedirs(path)
        except OSError:
            pass

    def get(self, name='default'):
        if name not in self._cache:
            full_path = os.path.join(self._base_folder, name)
            self._create_if_needed(full_path)
            self._cache[name] = Profile(full_path, name)
        return self._cache[name]

    @property
    def name(self):
        return self._name


class Profile(object):
    STORAGE_MAP = {
        '.conf': ConfigParserStorage,
        '.json': JSONConfigStorage,
        }

    def __init__(self, folder, name):
        self._folder = folder
        self._name = name
        self._storages = {}
        self._databases = {}

    @property
    def name(self):
        return self._name

    def get_filepath(self, name):
        return os.path.join(self._folder, name)

    def get_storage(self, name):
        if name not in self._storages:
            for suffix, engine in self.STORAGE_MAP.iteritems():
                if name.endswith(suffix):
                    self._storages[name] = engine(self.get_filepath(name))
                    break
        return self._storages[name]

    def get_config(self, filename, config_class, storage_args=None,
                   read_only=False):
        if not storage_args: storage_args = []
        storage = self.get_storage(filename)

        if read_only:
            config = config_class()
        else:
            config = config_class(storage, storage_args)

        return storage.load(config, *storage_args)

    def get_database(self, name='presentations.db'):
        if name not in self._databases:
            self._databases[name] = QtDBConnector(self.get_filepath(name))
        return self._databases[name]
