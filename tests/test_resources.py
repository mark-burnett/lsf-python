from lsf import resources
from pythonlsf import lsf as api
import mock
import unittest


class ResourceTest(unittest.TestCase):
    def test_make_rusage(self):
        expected_string = 'rusage[mem=1024] select[mem>=1024] span[hosts=1]'
        self.assertEqual(resources.make_rusage_string(
            select={'mem': 1}, rusage={'mem': 1}, span={'hosts': 1}),
                expected_string)

    def test_set_resources(self):
        request = self.mock_request()
        resources.set_resources(request,
            select={'mem': 1},
            rusage={'mem': 1},
        )

        self.assertEqual(request.resReq, 'rusage[mem=1024] select[mem>=1024]')
        self.assertTrue(request.options & api.SUB_RES_REQ)

    def test_set_resources_missing_request_rusage(self):
        request = self.mock_request()
        resources.set_resources(request, span={'hosts': 1})

        self.assertEqual(request.resReq, 'span[hosts=1]')
        self.assertTrue(request.options & api.SUB_RES_REQ)

    def mock_request(self):
        request = mock.Mock()
        request.options = 0
        request.options2 = 0
        request.options3 = 0

        return request
