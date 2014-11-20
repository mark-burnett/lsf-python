from lsf import rlimits
from pythonlsf import lsf as api
import mock
import unittest


class RLimitsTest(unittest.TestCase):
    def test_limits(self):
        request = self.mock_request()

        rlimits.set_rlimits(request, {'RSS': 1024})

        self.assertEqual(request.rLimits[api.LSF_RLIMIT_RSS], 1024)

        for i, v in enumerate(request.rLimits):
            if i != api.LSF_RLIMIT_RSS:
                self.assertEqual(v, api.DEFAULT_RLIMIT)

    def test_default_rlimits(self):
        request = self.mock_request()
        rlimits.set_rlimits(request, {})

        for v in request.rLimits:
            self.assertEqual(v, api.DEFAULT_RLIMIT)

    def mock_request(self):
        request = mock.Mock()
        request.options = 0
        request.options2 = 0
        request.options3 = 0

        return request
