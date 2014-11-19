from . import bindings
import logging


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
        return {
            'command': jobinfo.submit.command,
            'statuses': _translate_status(jobinfo.status),
        }


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
def _translate_status(status_code):
    statuses = set()
    for bitmask, name in _STATUSES.iteritems():
        if bitmask & status_code:
            statuses.add(name)

    if statuses:
        return sorted(statuses)
    else:
        return ['NULL']
