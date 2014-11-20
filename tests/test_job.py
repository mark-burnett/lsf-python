from lsf import job
import lsf
import time
import unittest


_MAX_RETRIES = 10
_POLLING_PERIOD = 3


class JobStatusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.job = lsf.submit('ls',
                options={'numProcessors': 1, 'maxNumProcessors': 1},
                rlimits={'threads': 1},
                )

    def test_jobs_should_compare_by_ids(self):
        job2 = lsf.get_job(self.job.job_id)
        self.assertEqual(self.job, job2)

    def test_job_as_dict(self):
        job_dict = _get_job_dict(self.job)

        self._verify_job_dict_statuses(job_dict['statuses'])
        self._verify_job_dict_submit_portion(job_dict['submit'])

        self._verify_job_dict_additional_fields(job_dict)

    def _verify_job_dict_statuses(self, statuses):
        self.assertGreater(len(statuses), 0)
        possible_valid_statuses = {'DONE', 'PDONE', 'PEND', 'RUN'}
        for status in statuses:
            self.assertIn(status, possible_valid_statuses)

    def _verify_job_dict_submit_portion(self, request_data):
        self.assertEqual(request_data['command'], 'ls')

        expected_options = {
            'numProcessors': 1,
            'maxNumProcessors': 1,
        }
        self.assertDictContainsSubset(expected_options, request_data['options'])

        expected_rlimits = {
            'threads': 1,
        }
        self.assertDictContainsSubset(expected_rlimits, request_data['rlimits'])

    def _verify_job_dict_additional_fields(self, job_dict):
        expected_additional_fields = [
            'cwd',
            'fromHost',
            'jName',
            'jobId',
            'jobPriority',
            'subHomeDir',
            'submitTime',
            'umask',
        ]

        for expected_field in expected_additional_fields:
            self.assertIsNotNone(job_dict[expected_field])


    def test_translate_null_status(self):
        self.assertEqual(job.translate_status(0), ['NULL'])


class JobKillTests(unittest.TestCase):
    def test_kill_sleep_job(self):
        job = lsf.submit('sleep 100')

        job.kill()

        job_dict = _get_job_dict(job)
        self.assertIn('EXIT', job_dict['statuses'])


def _get_job_dict(job):
    for attempt in xrange(_MAX_RETRIES):
        try:
            return job.as_dict
        except lsf.exceptions.InvalidJob:
            time.sleep(_POLLING_PERIOD)
    raise RuntimeError('Failed to get job status')
