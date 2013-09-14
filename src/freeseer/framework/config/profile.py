import os


class ProfileManager(object):
    def __init__(self, base_folder):
        self._base_folder = base_folder
        self._cache = {}
        self._create_if_needed(base_folder)

    def _create_if_needed(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

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
    def __init__(self, folder, name):
        self._folder = folder
        self._name = name

    @property
    def name(self):
        return self._name

    def get_filepath(self, name):
        return os.path.join(self._folder, name)
