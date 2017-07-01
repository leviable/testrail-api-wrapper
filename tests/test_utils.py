try:
    import mock
except ImportError:
    from unittest import mock

import pytest

from traw.utils import dispatchmethod


class Foo(object):
    def __init__(self):
        self.mock_obj = mock.MagicMock()

    @dispatchmethod
    def method_base(self, var):
        self.mock_obj.method_base(var)

    @method_base.register(int)
    def method_int(self, var):
        self.mock_obj.method_int(var)

    @method_base.register(str)
    def method_str(self, var):
        self.mock_obj.method_str(var)

    @method_base.register(list)
    def method_list(self, var, *args):
        self.mock_obj.method_list(var + list(args))

    @method_base.register(dict)
    def method_dict(self, var, **kwargs):
        self.mock_obj.method_dict(dict(var, **kwargs))


@pytest.fixture()
def dm():
    yield Foo()


def test_dispatchmethod_default(dm):
    """ Verify the base method gets called if you call with an
        unregistered type
    """
    obj = mock.MagicMock()
    dm.method_base(obj)

    assert dm.mock_obj.method_base.called
    assert not dm.mock_obj.method_int.called
    assert not dm.mock_obj.method_str.called
    assert not dm.mock_obj.method_list.called
    assert not dm.mock_obj.method_dict.called
    dm.mock_obj.method_base.assert_called_once_with(obj)


def test_dispatchmethod_int(dm):
    """ Verify the int registered method gets called if you call with an int """
    obj = 1234
    dm.method_base(obj)

    assert not dm.mock_obj.method_base.called
    assert dm.mock_obj.method_int.called
    assert not dm.mock_obj.method_str.called
    assert not dm.mock_obj.method_list.called
    assert not dm.mock_obj.method_dict.called
    dm.mock_obj.method_int.assert_called_once_with(obj)


def test_dispatchmethod_str(dm):
    """ Verify the str registered method gets called if you call with a string """
    obj = 'asdf'
    dm.method_base(obj)

    assert not dm.mock_obj.method_base.called
    assert not dm.mock_obj.method_int.called
    assert dm.mock_obj.method_str.called
    assert not dm.mock_obj.method_list.called
    assert not dm.mock_obj.method_dict.called
    dm.mock_obj.method_str.assert_called_once_with(obj)


def test_dispatchmethod_list_with_args(dm):
    """ Verify args can be passed through """
    obj = ['a', 'b', 'c']
    args = [1, 2, 3]
    dm.method_base(obj, *args)

    assert not dm.mock_obj.method_base.called
    assert not dm.mock_obj.method_int.called
    assert not dm.mock_obj.method_str.called
    assert dm.mock_obj.method_list.called
    assert not dm.mock_obj.method_dict.called
    dm.mock_obj.method_list.assert_called_once_with(obj + args)


def test_dispatchmethod_dict_with_kwargs(dm):
    """ Verify key word args can be passed through """
    obj = dict(a='a', b='b')
    kwargs = dict(one=1, two=2)

    dm.method_base(obj, **kwargs)

    assert not dm.mock_obj.method_base.called
    assert not dm.mock_obj.method_int.called
    assert not dm.mock_obj.method_str.called
    assert not dm.mock_obj.method_list.called
    assert dm.mock_obj.method_dict.called
    dm.mock_obj.method_dict.assert_called_once_with(dict(obj, **kwargs))
