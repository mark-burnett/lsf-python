from .exceptions import InvalidRlimit
from pythonlsf import lsf as api
import logging


__all__ = ['set_rlimits']


LOG = logging.getLogger(__name__)


class Limit(object):
    def __init__(self, name, option_index):
        self.name = name
        self.option_index = option_index

    def set_limit(self, rlimits, value):
        rlimits[self.option_index] = value


_RLIMITS = {
    o.name: o for o in [
        Limit('cpuTime', api.LSF_RLIMIT_CPU),
        Limit('RSS', api.LSF_RLIMIT_RSS),
        Limit('openFiles', api.LSF_RLIMIT_NOFILE),
        Limit('processes', api.LSF_RLIMIT_PROCESS),
        Limit('stack', api.LSF_RLIMIT_STACK),
        Limit('threads', api.LSF_RLIMIT_THREAD),
        Limit('virtualMemory', api.LSF_RLIMIT_VMEM),
    ]
}


def set_rlimits(request, rlimits):
    rlimits_array = [api.DEFAULT_RLIMIT] * api.LSF_RLIM_NLIMITS
    for name, value in rlimits.iteritems():
        try:
            _RLIMITS[name].set_limit(rlimits_array, value)
        except KeyError:
            raise InvalidRlimit(name)

    request.rLimits = rlimits_array
