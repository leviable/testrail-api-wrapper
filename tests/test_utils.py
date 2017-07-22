import mock
import pytest

import traw
from traw.utils import dispatchmethod

MOCK_USERNAME = 'mock username'
MOCK_USER_API_KEY = 'mock user api key'
MOCK_PASSWORD = 'mock password'
MOCK_URL = 'mock url'


class Foo(object):
    def __init__(self):
        self.mock_obj = mock.MagicMock()

    @dispatchmethod
    def method_base(self):
        self.mock_obj.method_base(1)

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


@pytest.fixture()
def dt():
    with mock.patch('traw.utils.dt') as dt_mock:
        yield dt_mock


@pytest.fixture()
def timedelta():
    with mock.patch('traw.utils.timedelta') as timedelta_mock:
        yield timedelta_mock


@pytest.fixture()
def api():
    with mock.patch('traw.api.Session') as Session:
        Session.return_value = Session
        yield traw.api.API(username=MOCK_USERNAME,
                           user_api_key=MOCK_USER_API_KEY,
                           password=MOCK_PASSWORD,
                           url=MOCK_URL)


def test_cacheable_caching(timedelta, dt, api):
    dt.now.return_value = 1
    timedelta.return_value = 2
    api.user_by_id.cache.clear()
    for _ in range(20):
        api.user_by_id(1)

    assert api._session.call_count == 1


def test_cacheable_generator_caching(timedelta, dt, api):
    dt.now.return_value = 1
    timedelta.return_value = 2
    api.users.cache.clear()
    for _ in range(20):
        list(api.users())

    assert api._session.call_count == 1


def test_cacheable_caching_expire(timedelta, dt, api):
    dt.now.side_effect = [0, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9, 9]
    timedelta.return_value = 3
    api._session.request.side_effect = range(3)
    api.user_by_id.cache.clear()
    vals = list()
    for _ in range(11):
        vals.append(api.user_by_id(1))

    assert api._session.request.call_count == 3
    assert vals == [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2]


def test_cacheable_generator_caching_expire(timedelta, dt, api):
    dt.now.side_effect = [0, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9, 9]
    timedelta.return_value = 3
    api._session.request.side_effect = [[0], [1], [2]]
    api.users.cache.clear()
    vals = list()
    for _ in range(11):
        vals.extend(api.users())

    assert api._session.request.call_count == 3
    assert vals == [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2]


def test_cacheable_clear_cache(timedelta, dt, api):
    dt.now.return_value = 1
    timedelta.return_value = 2
    api._session.request.side_effect = [3, [4], 5]
    api.milestone_by_id.cache.clear()
    api.milestones.cache.clear()

    api.milestone_by_id(1)
    list(api.milestones(123))

    assert len(api.milestone_by_id.cache) == 1
    assert len(api.milestones.cache) == 1

    api.milestone_add(123, dict())

    assert len(api.milestone_by_id.cache) == 0
    assert len(api.milestones.cache) == 0


def test_dispatchmethod_default(dm):
    """ Verify the base method gets called if you call with an
        unregistered type
    """
    dm.method_base()

    assert dm.mock_obj.method_base.called
    assert not dm.mock_obj.method_int.called
    assert not dm.mock_obj.method_str.called
    assert not dm.mock_obj.method_list.called
    assert not dm.mock_obj.method_dict.called
    dm.mock_obj.method_base.assert_called_once_with(1)


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
