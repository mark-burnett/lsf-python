from . import bindings
from . import job
from .options import set_options
from .resources import set_resources
import logging


__all__ = ['submit']


LOG = logging.getLogger(__name__)


def submit(command_line, options=None, resources=None):
    reply = bindings.create_reply()
    request = bindings.create_empty_request()

    request.command = str(' '.join("'%s'" % word for word in command_line))

    set_options(request, options)
    set_resources(request, resources)

    return job.Job(bindings.submit_job(request, reply))
