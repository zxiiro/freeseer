from .core import Option


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