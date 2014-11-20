from .exceptions import InvalidJob, LSFBindingException
from pythonlsf import lsf as api
import logging
import os
import signal


__all__ = [
    'create_empty_request',
    'get_job_info',
    'kill_job',
    'submit_job',
]


LOG = logging.getLogger(__name__)


def create_empty_request():
    init()
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
    init()
    try:
        return api.submitReply()
    except:
        LOG.exception('Caught exception in submitReply')
        raise LSFBindingException('Failed to create LSB Reply object')


_ALREADY_INIT = False
def init():
    global _ALREADY_INIT
    if _ALREADY_INIT:
        return

    init_code = api.lsb_init(None)
    if init_code != 0:
        raise LSFBindingException('Failed lsb_init')
    _ALREADY_INIT = True


def kill_job(job_id, signum=signal.SIGKILL):
    init()

    if 0 != api.lsb_signaljob(job_id, signum):
        raise LSFBindingException('Failed to signal job %s with %s'
                % (job_id, signum))


def submit_job(request, quiet=True):
    init()
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


def get_job_info(job_id):
    init()

    _open_jobinfo(job_id)
    job_info = _read_jobinfo()
    _close_jobinfo()

    return job_info


def _read_jobinfo():
    try:
        return api.lsb_readjobinfo(None)

    except:
        _unconditionally_close_jobinfo()
        raise LSFBindingException('Caught exception in lsb_readjobinfo')


def _open_jobinfo(job_id):
    try:
        job_info_head = api.lsb_openjobinfo_a(job_id,
                None, None, None, None,
                api.ALL_JOB)
    except:
        LOG.exception('Caught exception in lsb_openjobinfo_a')
        _unconditionally_close_jobinfo()
        raise LSFBindingException('Caught exception in lsb_openjobinfo_a')

    if job_info_head is None:
        raise InvalidJob(job_id)
    elif job_info_head == -1:
        raise LSFBindingException('lsb_openjobinfo_a failed, returning -1')


def _unconditionally_close_jobinfo():
    try:
        api.lsb_closejobinfo()
    except:
        pass


def _close_jobinfo():
    try:
        api.lsb_closejobinfo()
    except:
        raise LSFBindingException('Caught exception in lsb_closejobinfo')
