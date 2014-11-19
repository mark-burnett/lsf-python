from .exceptions import InvalidUnit
import abc


__all__ = [
    'MemoryConverter',
    'NullConverter',
]


class Converter(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, value):
        pass  # pragma: no cover


class MemoryConverter(Converter):
    def __init__(self, from_, to):
        self.from_ = from_
        self.to = to

    def __call__(self, value):
        return _convert_memory_value(value, self.from_, self.to)


class NullConverter(Converter):
    def __call__(self, value):
        return value


_MEMORY_UNITS = [
    'B',
    'KiB',
    'MiB',
    'GiB',
    'TiB',
    'PiB',
    'EiB',
    'ZiB',
]


def _convert_memory_value(src_value, src_units, dest_units):
    try:
        dest_index = _MEMORY_UNITS.index(dest_units)
    except ValueError:
        raise InvalidUnit(dest_units)

    try:
        src_index = _MEMORY_UNITS.index(src_units)
    except ValueError:
        raise InvalidUnit(src_units)

    if src_index > dest_index:
        dest_value = int(src_value) << (10 * (src_index - dest_index))
    elif dest_index > src_index:
        dest_value = int(src_value) >> (10 * (dest_index - src_index))
    else:
        dest_value = int(src_value)

    return dest_value
