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
