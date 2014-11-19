from .exceptions import InvalidOption
from pythonlsf import lsf as api
import logging


__all__ = ['set_options']


LOG = logging.getLogger(__name__)


class Option(object):
    def __init__(self, name, cast_with=str, flag=None, flag_group='options'):
        self.name = str(name)
        self.cast_with = cast_with
        self.flag = flag
        self.flag_group = flag_group

    def set_option(self, request, value):
        if value is None:
            return

        cast_value = self.cast_with(value)
        setattr(request, self.name, cast_value)

        if self.flag is not None:
            options = getattr(request, self.flag_group)
            setattr(request, self.flag_group, options | int(self.flag))


_OPTIONS = {o.name: o for o in
    [
        Option('beginTime', cast_with=int),
        Option('errFile', flag=api.SUB_ERR_FILE),
        Option('group', flag=api.SUB2_JOB_GROUP, flag_group='options2'),
        Option('inFile', flag=api.SUB_IN_FILE),
        Option('jobName', flag=api.SUB_JOB_NAME),
        Option('mail_user', flag=api.SUB_MAIL_USER),
        Option('maxNumProcessors', cast_with=int),
        Option('numProcessors', cast_with=int),
        Option('outFile', flag=api.SUB_OUT_FILE),
        Option('projectName', flag=api.SUB_PROJECT_NAME),
        Option('queue', flag=api.SUB_QUEUE),
        Option('termTime', cast_with=int),
    ]
}


def set_options(request, options):
    if not options:
        return

    for name, value in options.iteritems():
        option = _OPTIONS.get(name)
        if not option:
            raise InvalidOption(name)

        option.set_option(request, value)
