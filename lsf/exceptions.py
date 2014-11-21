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

from pythonlsf import lsf as api
import abc


__all__ = [
    'InvalidData',
    'InvalidJob',
    'InvalidOption',
    'InvalidRlimit',
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


class InvalidRlimit(InvalidData):
    header_text = 'rLimit'


class LSFBindingException(LSFException):
    def __init__(self, msg, *args, **kwargs):
        super(LSFException, self).__init__(self, add_err_info(msg),
                *args, **kwargs)


def add_err_info(msg):
    return '%s:  %s' % (msg, api.lsb_sysmsg())
