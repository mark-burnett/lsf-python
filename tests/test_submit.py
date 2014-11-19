import lsf
import unittest


class SubmitTests(unittest.TestCase):
    def test_submit_to_default_queue(self):
        job = lsf.submit('ls')
        self.assertGreater(job.job_id, 0)

    def test_submit_to_illegal_queue(self):
        with self.assertRaises(lsf.exceptions.LSFBindingException):
            lsf.submit('ls', options={'queue': 'nonexistantqueuefortesting'})
