import abc
import functools

from .exceptions import (
    InvalidOptionValueError,
    InvalidOptionDefaultValueError,
    OptionValueNotSetError,
)


class Option(object):
    class NotSpecified(object):
        pass

    def __init__(self, default=NotSpecified):
        self.default = default
        if not self.is_required and not self.is_valid(default):
            raise InvalidOptionDefaultValueError(self)

    def is_required(self):
        return self.default == self.NotSpecified

    # Override these!

    def is_valid(self, value):
        raise NotImplementedError()

    def encode(self, value):
        '''
        Encodes value into a string.

        Should raise something if unable to encode.
        '''
        raise NotImplementedError()

    def decode(self, value):
        '''
        Decodes value into a proper Option value.

        Should raise something if unable to decode.
        '''
        raise NotImplementedError()


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
        options = {}
        for name, attr in dct.iteritems():
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
            return self.values[name]
        else:
            raise OptionValueNotSetError(option)

    def set_value(self, name, option, value):
        if option.is_valid(value):
            self.values[name] = value
        else:
            raise InvalidOptionValueError(option)

    # You must implement these!

    @abc.abstractmethod
    def load(self):
        '''
        Populates the Config from somewhere.

        It should iterate over all options in self.options and determine the
        value to store by using option.decode(..).
        '''
        pass

    @abc.abstractmethod
    def load_if_possible(self):
        '''
        Tries to call self.load() if possible. Otherwise, it should fail gracefully.

        For example, if your class loads its values from a file, you can check if the
        file exists before calling self.load().
        '''
        pass

    @abc.abstractmethod
    def save(self):
        '''
        Persists the Config to somewhere.

        It should iterate over all options in self.options and determine the
        value to persis by using option.encode(..).
        '''
        pass
