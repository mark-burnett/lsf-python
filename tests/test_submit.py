import lsf
import unittest


class SubmitTests(unittest.TestCase):
    def test_submit_to_default_queue(self):
        job = lsf.submit([u'ls'])
        self.assertGreater(job.job_id, 0)
