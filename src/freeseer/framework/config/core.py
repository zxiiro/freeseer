import abc
import collections
import functools

from .exceptions import (
    InvalidOptionValueError,
    OptionValueNotSetError,
)


class Option(object):
    __metaclass__ = abc.ABCMeta

    class NotSpecified(object):
        pass

    def __init__(self, default=NotSpecified):
        self.default = default

    def is_required(self):
        return self.default == self.NotSpecified

    def post_get(self, value):
        pass

    def post_set(self, value):
        pass

    # Override these!

    @abc.abstractmethod
    def is_valid(self, value):
        '''
        Checks if a value is valid for this option.
        '''
        pass

    @abc.abstractmethod
    def encode(self, value):
        '''
        Encodes value into a string.

        Should raise something if unable to encode.
        '''
        pass

    @abc.abstractmethod
    def decode(self, value):
        '''
        Decodes value into a proper Option value.

        Should raise something if unable to decode.
        '''
        pass


class ConfigBase(abc.ABCMeta):
    def __new__(meta, name, bases, dct):
        dct, options = meta.find_options(dct)
        dct['options'] = options
        cls = super(ConfigBase, meta).__new__(meta, name, bases, dct)
        for opt_name, option in options.iteritems():
            opt_get = functools.partial(cls.get_value, name=opt_name, option=option)
            opt_set = functools.partial(cls._set_value, name=opt_name, option=option)
            setattr(cls, opt_name, property(opt_get, opt_set))
        return cls

    @staticmethod
    def find_options(dct):
        new_dct = {}
        options = collections.OrderedDict()
        for name in sorted(dct.keys()):
            attr = dct[name]
            if name.startswith('_') or not isinstance(attr, Option):
                new_dct[name] = attr
            else:
                options[name] = attr
        return new_dct, options 


class Config(object):
    __metaclass__ = ConfigBase

    def __init__(self):
        self.values = {}
        self.set_defaults()

    def _set_value(self, value, name, option):
        self.set_value(name, option, value)

    def set_defaults(self):
        for name, option in self.options.iteritems():
            if not option.is_required():
                self.set_value(name, option, option.default)

    # You probably will not need to override these:

    def get_value(self, name, option):
        if name in self.values:
            value = self.values[name]
            option.post_get(value)
            return value
        else:
            raise OptionValueNotSetError(name, option)

    def set_value(self, name, option, value):
        if option.is_valid(value):
            self.values[name] = value
            option.post_set(value)
        else:
            raise InvalidOptionValueError(name, option)


class ConfigStorage(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, profile, filename):
        self._profile = profile
        self._filepath = profile.get_filepath(filename)

    # Override these!

    @abc.abstractmethod
    def load(self, config_instance):
        '''
        Populates the Config from somewhere.

        It should iterate over all options in self.options and determine the
        value to store by using option.decode(..).
        '''
        pass

    @abc.abstractmethod
    def store(self, config_instance):
        '''
        Persists the Config to somewhere.

        It should iterate over all options in self.options and determine the
        value to persis by using option.encode(..).
        '''
        pass
