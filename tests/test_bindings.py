import lsf
import mock
import unittest


class BindingErrorTests(unittest.TestCase):
    def test_create_empty_request_raises_binding_exception(self):
        with mock.patch('lsf.bindings.api.submit') as p:
            p.side_effect = RuntimeError('Unknown Error')
            with self.assertRaises(lsf.exceptions.LSFBindingException):
                lsf.bindings.create_empty_request()

    def test_create_reply_raises_binding_exception(self):
        with mock.patch('lsf.bindings.api.submitReply') as p:
            p.side_effect = RuntimeError('Unknown Error')
            with self.assertRaises(lsf.exceptions.LSFBindingException):
                lsf.bindings.create_reply()

    def test_init_raises_binding_exception(self):
        lsf.bindings._ALREADY_INIT = False  # We must force init to run again

        with mock.patch('lsf.bindings.api.lsb_init') as p:
            p.return_value = -1
            with self.assertRaises(lsf.exceptions.LSFBindingException):
                lsf.bindings.init()

    def test_submit_job_raises_binding_exception_if_lsb_submit_errors(self):
        with mock.patch('lsf.bindings.api.lsb_submit') as p:
            p.side_effect = RuntimeError('Unknown Error')
            with self.assertRaises(lsf.exceptions.LSFBindingException):
                lsf.bindings.submit_job(None)

    def test_submit_job_raises_binding_exception_if_lsb_submit_fails(self):
        with mock.patch('lsf.bindings.api.lsb_submit') as p:
            p.return_value = 0
            with self.assertRaises(lsf.exceptions.LSFBindingException):
                lsf.bindings.submit_job(None)

    def test_get_job_info_raises_binding_exception_on_open_errors(self):
        with mock.patch('lsf.bindings.api.lsb_openjobinfo_a') as p:
            p.side_effect = RuntimeError('Unknown Error')
            with self.assertRaises(lsf.exceptions.LSFBindingException):
                lsf.bindings.get_job_info(1)

    def test_get_job_info_raises_binding_exception_on_open_fails(self):
        with mock.patch('lsf.bindings.api.lsb_openjobinfo_a') as p:
            p.return_value = -1
            with self.assertRaises(lsf.exceptions.LSFBindingException):
                lsf.bindings.get_job_info(1)

    def test_get_job_info_raises_invalid_job_exception_on_open_ret_none(self):
        with mock.patch('lsf.bindings.api.lsb_openjobinfo_a') as p:
            p.return_value = None
            with self.assertRaises(lsf.exceptions.InvalidJob):
                lsf.bindings.get_job_info(1)

    def test_get_job_info_raises_binding_exception_on_read_error(self):
        with mock.patch('lsf.bindings.api.lsb_openjobinfo_a') as p:
            p.return_value = 1
            with mock.patch('lsf.bindings.api.lsb_readjobinfo') as read_patch:
                read_patch.side_effect = RuntimeError('Unknown Error')
                with self.assertRaises(lsf.exceptions.LSFBindingException):
                    lsf.bindings.get_job_info(1)

    def test_get_job_info_raises_binding_exception_on_close_error(self):
        with mock.patch('lsf.bindings.api.lsb_openjobinfo_a') as p:
            p.return_value = 1
            with mock.patch('lsf.bindings.api.lsb_closejobinfo') as close_patch:
                close_patch.side_effect = RuntimeError('Unknown Error')
                with self.assertRaises(lsf.exceptions.LSFBindingException):
                    lsf.bindings.get_job_info(1)

    def test_unconditionally_close_jobinfo_does_not_raise(self):
        with mock.patch('lsf.bindings.api.lsb_openjobinfo_a') as p:
            p.side_effect = RuntimeError('Unknown Error')
            with mock.patch('lsf.bindings.api.lsb_closejobinfo') as close_patch:
                close_patch.side_effect = RuntimeError('Unknown Error')
                with self.assertRaises(lsf.exceptions.LSFBindingException):
                    lsf.bindings.get_job_info(1)

    def test_non_quiet_submit_branch_with_error(self):
        with mock.patch('lsf.bindings.api.lsb_submit') as p:
            p.side_effect = RuntimeError('Unknown Error')
            with self.assertRaises(lsf.exceptions.LSFBindingException):
                lsf.bindings.submit_job(None, quiet=False)

    def test_non_quiet_submit_branch_with_success(self):
        with mock.patch('lsf.bindings.api.lsb_submit') as p:
            p.return_value = 1
            self.assertEqual(lsf.bindings.submit_job(None, quiet=False), 1)
