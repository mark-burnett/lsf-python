import lsf
import unittest


class SubmitTests(unittest.TestCase):
    def test_submit_to_default_queue(self):
        job = lsf.submit([u'ls'])
        self.assertGreater(job.job_id, 0)

    def test_submit_to_illegal_queue(self):
        with self.assertRaises(RuntimeError):
            lsf.submit([u'ls'], options={'queue': 'nonexistantqueuefortesting'})
