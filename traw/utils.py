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

    def wrapper(inst, dispatch_data, *args, **kwargs):
        cls = type(dispatch_data)
        impl = dispatch(cls)
        return impl(inst, dispatch_data, *args, **kwargs)

    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = dispatcher.registry
    wrapper._clear_cache = dispatcher._clear_cache  # pylint: disable=protected-access
    update_wrapper(wrapper, func)
    return wrapper
