from . import bindings
from . import job
import logging


__all__ = ['submit']


LOG = logging.getLogger(__name__)


def submit(command_line, options=None, resources=None):
    reply = bindings.create_reply()
    request = bindings.create_empty_request()

    request.command = str(' '.join("'%s'" % word for word in command_line))

    _set_options(request, options)
    _set_resources(request, resources)

    return job.Job(bindings.submit_job(request, reply))


def _set_options(request, options):
    pass


def _set_resources(request, resources):
    pass
