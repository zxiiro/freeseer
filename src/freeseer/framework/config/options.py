import os

from freeseer.framework.config.core import Option


class StringOption(Option):
    def is_valid(self, value):
        return isinstance(value, str) or hasattr(value, '__str__')

    def encode(self, value):
        return str(value)

    def decode(self, value):
        return str(value)


class IntegerOption(Option):
    def is_valid(self, value):
        return isinstance(value, int)

    def encode(self, value):
        return str(value)

    def decode(self, value):
        return int(value)


class FloatOption(Option):
    def is_valid(self, value):
        return isinstance(value, float)

    def encode(self, value):
        return str(value)

    def decode(self, value):
        return float(value)


class BooleanOption(Option):
    def is_valid(self, value):
        return isinstance(value, bool)

    def encode(self, value):
        return value and 'true' or 'false'

    def decode(self, value):
        return (value == 'true') and True or False


class FolderOption(StringOption):
    def __init__(self, default=Option.NotSpecified, auto_create=False):
        self.auto_create = auto_create
        super(StringOption, self).__init__(default)

    def is_valid(self, value):
        return self.auto_create or os.path.isdir(value)

    def presentation(self, value):
        realpath = os.path.expanduser(value)
        if self.auto_create:
            if not os.path.exists(realpath):
                os.makedirs(realpath)
        return realpath


class ChoiceOption(StringOption):
    def __init__(self, choices, default=Option.NotSpecified):
        self.choices = choices
        super(ChoiceOption, self).__init__(default)

    def is_valid(self, value):
        return value in self.choices
