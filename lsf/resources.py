from . import config
from . import units
from .exceptions import InvalidResource
from pythonlsf import lsf as api
import logging


__all__ = ['set_resources']


class Resource(object):
    def __init__(self, name, operator='=', converter=None):
        self.name = name
        if converter:
            self.converter = converter
        else:
            self.converter = units.NullConverter()
        self.operator = operator

    def string_for(self, value):
        return '%s%s%s' % (self.name, self.operator, self.converter(value))


_RUSAGE = {
    o.name: o for o in [
        Resource('mem', converter=units.MemoryConverter(
            from_=config.API_MEMORY_UNITS, to=config.REQUEST_MEMORY_UNITS)),
        # XXX Plus user-defined properties
    ]
}


_SELECT = {
    o.name: o for o in [
        Resource('mem', operator='>=',
            converter=units.MemoryConverter(from_=config.API_MEMORY_UNITS,
                to=config.REQUEST_MEMORY_UNITS)),
        # XXX Plus user-defined properties
    ]
}


_SPAN = {
    o.name: o for o in [
        Resource('hosts', converter=int),
    ]
}


def set_resources(request, rusage=None, select=None, span=None):
    rusage_string = make_rusage_string(rusage or {}, select or {}, span or {})
    if rusage_string:
        request.options |= api.SUB_RES_REQ
        request.resReq = rusage_string


def make_rusage_string(rusage, select, span):
    components = []

    components.extend(get_res_req_component(rusage, 'rusage[%s]', _RUSAGE))
    components.extend(get_res_req_component(select, 'select[%s]', _SELECT))
    components.extend(get_res_req_component(span, 'span[%s]', _SPAN))

    return str(' '.join(components))


def get_res_req_component(data, template, available_components):
    components = []
    for name, value in data.iteritems():
        try:
            components.append(available_components[name].string_for(value))
        except KeyError:
            raise InvalidResource(name)

    if components:
        return [template % ''.join(components)]
    else:
        return []
