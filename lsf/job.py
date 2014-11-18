import logging


__all__ = ['get_job']


LOG = logging.getLogger(__name__)


def get_job(job_id):
    return Job(job_id)


class Job(object):
    def __init__(self, job_id):
        self.job_id = job_id
