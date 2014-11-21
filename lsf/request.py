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

from . import bindings
from . import job
from .rlimits import set_rlimits
from .options import set_options
import logging


__all__ = ['submit']


LOG = logging.getLogger(__name__)


def submit(command, options=None, rlimits=None):
    request = bindings.create_empty_request()

    request.command = command

    set_options(request, options or {})
    set_rlimits(request, rlimits or {})

    return job.Job(bindings.submit_job(request))
