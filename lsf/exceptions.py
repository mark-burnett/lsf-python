from pythonlsf import lsf as api
import abc


__all__ = [
    'InvalidData',
    'InvalidJob',
    'InvalidOption',
    'InvalidResource',
    'InvalidRlimit',
    'InvalidUnit',
    'LSFBindingException',
    'LSFException',
]


class LSFException(Exception): pass


class InvalidData(LSFException):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, *args, **kwargs):
        super(InvalidData, self).__init__(self._msg(name), *args, **kwargs)

    def _msg(self, name):
        return 'Invalid %s: "%s"' % (self.header_text, name)

    @abc.abstractproperty
    def header_text(cls):
        pass  # pragma: no cover


class InvalidJob(InvalidData):
    header_text = 'job'


class InvalidOption(InvalidData):
    header_text = 'option'


class InvalidResource(InvalidData):
    header_text = 'resource'


class InvalidRlimit(InvalidData):
    header_text = 'rLimit'


class InvalidUnit(InvalidData):
    header_text = 'unit'


class LSFBindingException(LSFException):
    def __init__(self, msg, *args, **kwargs):
        super(LSFException, self).__init__(self, add_err_info(msg),
                *args, **kwargs)


def add_err_info(msg):
    return '%s:  %s' % (msg, api.lsb_sysmsg())
