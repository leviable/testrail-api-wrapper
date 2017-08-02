from datetime import timedelta as td
import mock
import pytest

import traw
from traw.const import GET, API_PATH as AP
from traw.utils import dispatchmethod, duration_to_timedelta

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


def test_paginate_w_no_limit(api):
    api.results_by_test_id.cache.clear()
    api._session.request.side_effect = [[1] * 250, [2] * 250, [3] * 50]

    TEST_ID = 1

    results = list(api.results_by_test_id(TEST_ID))

    exp_call_1 = mock.call(method=GET,
                           path=AP['get_results'].format(test_id=TEST_ID),
                           params={'offset': 0})

    exp_call_2 = mock.call(method=GET,
                           path=AP['get_results'].format(test_id=TEST_ID),
                           params={'offset': 250})

    exp_call_3 = mock.call(method=GET,
                           path=AP['get_results'].format(test_id=TEST_ID),
                           params={'offset': 500})

    assert len(results) == 550
    assert results == [1] * 250 + [2] * 250 + [3] * 50
    assert api._session.request.call_args_list == [exp_call_1, exp_call_2, exp_call_3]


def test_paginate_w_limit(api):
    api.results_by_test_id.cache.clear()
    api._session.request.side_effect = [[1] * 250, [2] * 250, [3] * 50]

    TEST_ID = 1

    results = list(api.results_by_test_id(TEST_ID, limit=525))

    exp_call_1 = mock.call(method=GET,
                           path=AP['get_results'].format(test_id=TEST_ID),
                           params={'offset': 0, 'limit': 250})

    exp_call_2 = mock.call(method=GET,
                           path=AP['get_results'].format(test_id=TEST_ID),
                           params={'offset': 250, 'limit': 250})

    exp_call_3 = mock.call(method=GET,
                           path=AP['get_results'].format(test_id=TEST_ID),
                           params={'offset': 500, 'limit': 25})

    assert len(results) == 525
    assert results == [1] * 250 + [2] * 250 + [3] * 25
    assert api._session.request.call_args_list == [exp_call_1, exp_call_2, exp_call_3]


def test_cacheable_caching(timedelta, dt, full_client):
    dt.now.return_value = 1
    timedelta.return_value = 2
    full_client.api.user_by_id.cache.clear()
    for _ in range(20):
        full_client.user(1)

    assert full_client.api._session.call_count == 1


def test_cacheable_generator_caching(timedelta, dt, full_client):
    dt.now.return_value = 1
    timedelta.return_value = 2
    full_client.api.users.cache.clear()
    for _ in range(20):
        list(full_client.users())

    assert full_client.api._session.call_count == 1


def test_cacheable_caching_expire(timedelta, dt, full_client):
    dt.now.side_effect = [0, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9, 9]
    timedelta.return_value = 3
    full_client.api._session.request.side_effect = [{'id': 0}, {'id': 1}, {'id': 2}]
    full_client.api.user_by_id.cache.clear()
    vals = list()
    for _ in range(11):
        vals.append(full_client.user(1).id)

    assert full_client.api._session.request.call_count == 3
    assert vals == [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2]


def test_cacheable_generator_caching_expire(timedelta, dt, full_client):
    dt.now.side_effect = [0, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9, 9]
    timedelta.return_value = 3
    user_dicts = [[{'id': 0}], [{'id': 1}], [{'id': 2}]]
    full_client.api._session.request.side_effect = user_dicts
    full_client.api.users.cache.clear()
    vals = list()
    for _ in range(11):
        vals.append(list(full_client.users())[0].id)

    assert full_client.api._session.request.call_count == 3
    assert vals == [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2]


def test_cacheable_clear_cache(timedelta, dt, full_client):
    dt.now.return_value = 1
    timedelta.return_value = 2
    side_effects = [{'id': 3},    # full_client.milestone(1)
                    [{'id': 4}],  # full_client.milestones(123)
                    {'id': 5},    # full_client.add -> milestone.project.id
                    {'id': 6}]    # full_client.add -> response
    full_client.api._session.request.side_effect = side_effects
    full_client.api.milestone_by_id.cache.clear()
    full_client.api.milestones.cache.clear()

    full_client.milestone(1)
    list(full_client.milestones(123))

    assert len(full_client.api.milestone_by_id.cache) == 1
    assert len(full_client.api.milestones.cache) == 1

    full_client.add(traw.models.Milestone(full_client, {'id': 456, 'project_id': 5}))

    assert len(full_client.api.milestone_by_id.cache) == 0
    assert len(full_client.api.milestones.cache) == 0


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


def test_duration_to_timedelta():
    """ Verify the duration to timedelta conversion """
    duration = '1w 2d 3h 4m 5s'
    d2td = duration_to_timedelta(duration)

    total_days = 7 + 2
    total_seconds = (3 * 60 * 60) + (4 * 60) + 5

    assert isinstance(d2td, td)
    assert d2td == td(days=total_days, seconds=total_seconds)
