import re
from datetime import datetime as dt, timedelta
from functools import update_wrapper, wraps

from singledispatch import singledispatch


def cacheable_generator(obj_type):
    def _cacheable_generator(func):
        """ """
        cache = func.cache = {}

        @wraps(func)
        def cacheable_func(inst, *args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in cache or cache[key]['expires'] < dt.now():
                timeout = inst._CACHE_TIMEOUTS[inst][obj_type]  # pylint: disable=protected-access
                cache[key] = dict()
                cache[key]['value'] = list()
                cache[key]['expires'] = dt.now() + timedelta(seconds=timeout)
                for val in func(inst, *args, **kwargs):
                    cache[key]['value'].append(val)
                    yield val
            else:
                for val in cache[key]['value']:
                    yield val

        return cacheable_func
    return _cacheable_generator


def cacheable(obj_type):
    def cacheable_func(func):
        """ """
        cache = func.cache = {}

        @wraps(func)
        def _cacheable_func(inst, *args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in cache or cache[key]['expires'] < dt.now():
                timeout = inst._CACHE_TIMEOUTS[inst][obj_type]  # pylint: disable=protected-access
                cache[key] = dict()
                cache[key]['value'] = func(inst, *args, **kwargs)
                cache[key]['expires'] = dt.now() + timedelta(seconds=timeout)

            return cache[key]['value']

        return _cacheable_func
    return cacheable_func


def clear_cache(method):
    def target(func):
        @wraps(func)
        def _func(*args, **kwargs):
            response = func(*args, **kwargs)
            method.cache.clear()
            return response
        return _func
    return target


def dispatchmethod(func):
    """ singledispatch for class methods

    This provides for a way to use ``functools.singledispatch`` inside of a class.
    It has the same basic interface that ``singledispatch`` does.
    """
    # This implementation builds on the following gist:
    # https://gist.github.com/adamnew123456/9218f99ba35da225ca11
    dispatcher = singledispatch(func)

    def register(type):  # pylint: disable=redefined-builtin
        def _register(func):
            return dispatcher.register(type)(func)

        return _register

    def dispatch(type):  # pylint: disable=redefined-builtin
        return dispatcher.dispatch(type)

    def wrapper(inst, *args, **kwargs):
        cls = args[0].__class__ if len(args) > 0 else inst.__class__
        impl = dispatch(cls)
        return impl(inst, *args, **kwargs)

    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = dispatcher.registry
    wrapper._clear_cache = dispatcher._clear_cache  # pylint: disable=protected-access
    update_wrapper(wrapper, func)
    return wrapper


def duration_to_timedelta(duration):
    def timespan(segment):
        return int(segment.group(0)[:-1]) if segment else 0

    timedelta_map = {
        'weeks': timespan(re.search('\d+w', duration)),
        'days': timespan(re.search('\d+d', duration)),
        'hours': timespan(re.search('\d+h', duration)),
        'minutes': timespan(re.search('\d+m', duration)),
        'seconds': timespan(re.search('\d+s', duration))
    }
    return timedelta(**timedelta_map)
