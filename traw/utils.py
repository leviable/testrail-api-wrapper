import re
from datetime import timedelta
from functools import update_wrapper

from singledispatch import singledispatch


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
