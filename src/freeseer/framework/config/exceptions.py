class OptionError(Exception):
    def __init__(self, name, option):
        super(OptionError, self).__init__(name)


class InvalidOptionValueError(OptionError):
    pass


class InvalidOptionDefaultValueError(OptionError):
    pass


class OptionValueNotSetError(OptionError):
    pass
