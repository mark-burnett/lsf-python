from . import bindings
from .options import get_options
from .rlimits import get_rlimits
import logging
import signal
import string


__all__ = ['get_job']


LOG = logging.getLogger(__name__)


def get_job(job_id):
    return Job(job_id)


class Job(object):
    def __init__(self, job_id):
        self.job_id = job_id

    def __eq__(self, other):
        return self.job_id == other.job_id

    @property
    def as_dict(self):
        jobinfo = bindings.get_job_info(self.job_id)
        assert self.job_id == jobinfo.jobId

        result = {
            'statuses': translate_status(jobinfo.status),
            'submit': _request_info(jobinfo.submit),
        }

        result.update(_get_additional_lsf_supplied_fields(jobinfo))

        return result

    def kill(self, signum=signal.SIGKILL):
        bindings.kill_job(self.job_id, signum)


_STATUSES = {
        0x1: 'PEND',
        0x2: 'PSUSP',
        0x4: 'RUN',
        0x8: 'SSUSP',
       0x10: 'USUSP',
       0x20: 'EXIT',
       0x40: 'DONE',
       0x80: 'PDONE',
      0x100: 'PERR',
      0x200: 'WAIT',
     0x8000: 'RUNKWN',
    0x10000: 'UNKWN',
}
def translate_status(status_code):
    statuses = set()
    for bitmask, name in _STATUSES.iteritems():
        if bitmask & status_code:
            statuses.add(name)

    if statuses:
        return sorted(statuses)
    else:
        return ['NULL']


def _request_info(submit):
    result = {
        'command': submit.command,
    }

    result['options'] = get_options(submit)
    result['rlimits'] = get_rlimits(submit)

    return result


_DIRECT_COPY_FIELDS = [
    'cwd',
    'fromHost',
    'jName',
    'jobId',
    'jobPriority',
    'subHomeDir',
    'submitTime',
]
_TRANSFORM_FIELDS = {
    'umask': lambda x: string.zfill(x, 4),
}
_GREATER_ZERO_FIELDS = [
    'cpuTime',
    'endTime',
    'jobPid',
    'predictedStartTime',
    'runTime',
    'startTime',
]
_EXEC_FIELDS = [
    'exHosts',
    'execCwd',
    'execHome',
    'execRusage',
    'execUid',
    'execUsername',
]
def _get_additional_lsf_supplied_fields(jobinfo):
    result = {
        field: getattr(jobinfo, field) for field in _DIRECT_COPY_FIELDS
    }

    result.update({
        field: transform(getattr(jobinfo, field))
            for field, transform in _TRANSFORM_FIELDS.iteritems()
    })


    result.update({
        field: getattr(jobinfo, field)
            for field in _GREATER_ZERO_FIELDS
            if getattr(jobinfo, field) > 0
    })

    if _exec_available(jobinfo):
        result.update({
            field: getattr(jobinfo, field)
                for field in _EXEC_FIELDS
        })

    return result


def _exec_available(jobinfo):
    return jobinfo.execCwd
