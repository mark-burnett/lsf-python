# Copyright (C) 2014 The Genome Institute, Washington University Medical School
#
# This file is part of lsf-python.
#
# lsf-python is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# lsf-python is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lsf-python.  If not, see <http://www.gnu.org/licenses/>.

from .exceptions import InvalidRlimit
from pythonlsf import lsf as api
import logging


__all__ = ['get_rlimits', 'set_rlimits']


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


_REVERSE_RLIMITS = {
    o.option_index: o.name for o in _RLIMITS.itervalues()
}


def get_rlimits(request):
    rlimits = {}
    for index, rlim_val in enumerate(request.rLimits):
        if rlim_val != api.DEFAULT_RLIMIT:
            name = _REVERSE_RLIMITS[index]
            rlimits[name] = rlim_val

    return rlimits


def set_rlimits(request, rlimits):
    rlimits_array = [api.DEFAULT_RLIMIT] * api.LSF_RLIM_NLIMITS
    for name, value in rlimits.iteritems():
        try:
            _RLIMITS[name].set_limit(rlimits_array, value)
        except KeyError:
            raise InvalidRlimit(name)

    request.rLimits = rlimits_array
