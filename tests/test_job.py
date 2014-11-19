import lsf
import time
import unittest


_MAX_RETRIES = 10


class JobTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.job = lsf.submit('ls')

    def test_jobs_should_compare_by_ids(self):
        job2 = lsf.get_job(self.job.job_id)
        self.assertEqual(self.job, job2)

    def test_job_as_dict(self):
        job_dict = None
        for attempt in xrange(_MAX_RETRIES):
            try:
                job_dict = self.job.as_dict
                break
            except lsf.exceptions.InvalidJob:
                time.sleep(5)

        self.assertGreater(len(job_dict['statuses']), 0)

        possible_valid_statuses = {'DONE', 'PDONE', 'PEND', 'RUN'}
        for status in job_dict['statuses']:
            self.assertIn(status, possible_valid_statuses)

        self.assertEqual(job_dict['command'], 'ls')
