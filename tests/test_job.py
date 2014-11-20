from lsf import job
import lsf
import time
import unittest


_MAX_RETRIES = 10
_INITIAL_WAIT = 5
_POLLING_PERIOD = 3


class JobTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.job = lsf.submit('ls',
                options={'numProcessors': 1, 'maxNumProcessors': 1},
                rlimits={'cpuTime': 1, 'threads': 1},
                )

    def test_jobs_should_compare_by_ids(self):
        job2 = lsf.get_job(self.job.job_id)
        self.assertEqual(self.job, job2)

    def test_job_as_dict(self):
        job_dict = None
        time.sleep(_INITIAL_WAIT)
        for attempt in xrange(_MAX_RETRIES):
            try:
                job_dict = self.job.as_dict
                break
            except lsf.exceptions.InvalidJob:
                time.sleep(_POLLING_PERIOD)

        self.assertEqual(job_dict['command'], 'ls')

        self.assertGreater(len(job_dict['statuses']), 0)
        possible_valid_statuses = {'DONE', 'PDONE', 'PEND', 'RUN'}
        for status in job_dict['statuses']:
            self.assertIn(status, possible_valid_statuses)

        expected_options = {
            'numProcessors': 1,
            'maxNumProcessors': 1,
        }
        self.assertDictContainsSubset(expected_options, job_dict['options'])

        expected_rlimits = {
            'cpuTime': 1,
            'threads': 1,
        }
        self.assertDictContainsSubset(expected_rlimits, job_dict['rlimits'])

    def test_translate_null_status(self):
        self.assertEqual(job.translate_status(0), ['NULL'])
