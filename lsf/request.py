from . import bindings
from . import job
from .rlimits import set_rlimits
from .options import set_options
from .resources import set_resources
import logging


__all__ = ['submit']


LOG = logging.getLogger(__name__)


def submit(command_line, options=None, rlimits=None, rusage=None, select=None,
        span=None):
    request = bindings.create_empty_request()

    set_command(request, command_line)
    set_options(request, options or {})
    set_rlimits(request, rlimits or {})
    set_resources(request, rusage=rusage, select=select, span=span)

    return job.Job(bindings.submit_job(request))


def set_command(request, command_line):
    request.command = str(' '.join("'%s'" % word for word in command_line))
