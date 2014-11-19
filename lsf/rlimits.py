from . import config
from . import units
from pythonlsf import lsf as api
import logging


__all__ = ['set_rlimits']


LOG = logging.getLogger(__name__)


class Limit(object):
    def __init__(self, name, option_index, converter=None):
        self.name = name
        self.option_index = option_index
        if converter:
            self.converter = converter
        else:
            self.converter = units.NullConverter()

    def set_limit(self, rlimits, value):
        rlimits[self.option_index] = self.converter(value)


_RLIMITS = {
    o.name: o for o in [
        Limit('cpuTime', api.LSF_RLIMIT_CPU, units.NullConverter()),
        Limit('RSS', api.LSF_RLIMIT_RSS,
            units.MemoryConverter(from_=config.API_MEMORY_UNITS,
                to=config.LIMIT_RSS_UNITS)),
        Limit('openFiles', api.LSF_RLIMIT_NOFILE),
        Limit('processes', api.LSF_RLIMIT_PROCESS),
        Limit('stack', api.LSF_RLIMIT_STACK,
            units.MemoryConverter(from_=config.API_MEMORY_UNITS,
                to=config.LIMIT_STACK_UNITS)),
        Limit('threads', api.LSF_RLIMIT_THREAD),
        Limit('virtualMemory', api.LSF_RLIMIT_VMEM,
            units.MemoryConverter(from_=config.API_MEMORY_UNITS,
                to=config.LIMIT_VMEM_UNITS)),
    ]
}


def set_rlimits(request, rlimits):
    rlimits_array = [api.DEFAULT_RLIMIT] * api.LSF_RLIM_NLIMITS
    for name, value in rlimits.iteritems():
        try:
            _RLIMITS[name].set_limit(rlimits_array, value)
        except KeyError:
            raise RuntimeError('Could not find rlimit resource "%s"' % name)

    request.rLimits = rlimits_array
