from . import config
from .exceptions import LSFBindingException
from pythonlsf import lsf as api
import logging
import os


__all__ = [
    'create_empty_request',
    'init',
    'submit_job',
]


LOG = logging.getLogger(__name__)


def create_empty_request():
    try:
        request = api.submit()
    except:
        LOG.exception('Failed to create empty request')
        raise LSFBindingException('Caught exception in submit')

    request.options = 0
    request.options2 = 0
    request.options3 = 0

    return request


def create_reply():
    try:
        return api.submitReply()
    except:
        LOG.exception('Caught exception in submitReply')
        raise LSFBindingException('Failed to create LSB Reply object')


def init():
    init_code = api.lsb_init(None)
    if init_code != 0:
        raise LSFBindingException('Failed lsb_init')


def submit_job(request, quiet=True):
    reply = create_reply()

    try:
        if quiet:
            os.environ['BSUB_QUIET'] = '1'
        job_id = api.lsb_submit(request, reply)
    except:
        LOG.exception('Failed to submit LSF job')
        raise LSFBindingException('Caught exception in lsb_submit')
    finally:
        if 'BSUB_QUIET' in os.environ:
            del os.environ['BSUB_QUIET']

    if job_id > 0:
        LOG.debug('Successfully submitted LSF job: %s', job_id)
        return job_id

    else:
        LOG.debug('Failed to submit LSF job, return value = (%s)', job_id)
        raise LSFBindingException('Failed to submit LSF job')
