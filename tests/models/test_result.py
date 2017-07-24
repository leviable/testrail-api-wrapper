from copy import deepcopy
from datetime import datetime as dt, timedelta

import pytest

from traw.models import Result, Status, User, Test as _Test  # Avoid tox test collection warning


ASSIGNED_TO_ID = 1
COMMENT = "mock result comment"
CREATED_BY_ID = 2
CREATED_ON = 1469726522
DEF1 = "DEFECT1"
DEF2 = "DEFECT2"
DEF3 = "DEFECT3"
ELAPSED = "10m 5s"
ID = 3
STATUS_ID = 4
TEST_ID = 5
VERSION = "1.0RC1"


@pytest.fixture()
def empty_result(client):
    return Result(client)


@pytest.fixture()
def result(client):
    content = {"assignedto_id": ASSIGNED_TO_ID,
               "comment": COMMENT,
               "created_by": CREATED_BY_ID,
               "created_on": CREATED_ON,
               "defects": ",".join([DEF1, DEF2, DEF3]),
               "elapsed": ELAPSED,
               "id": ID,
               "status_id": STATUS_ID,
               "test_id": TEST_ID,
               "version": VERSION}
    return Result(client, deepcopy(content))


def test_assigned_to_get(empty_result, result):
    assert empty_result.assigned_to is None

    result.client.api.user_by_id.return_value = {'id': ASSIGNED_TO_ID}

    assert isinstance(result.assigned_to, User)
    assert result.assigned_to.id == ASSIGNED_TO_ID
    result.client.api.user_by_id.assert_called_with(ASSIGNED_TO_ID)


def test_assigned_to_set(client, empty_result, result):
    user1 = User(client, {'id': ASSIGNED_TO_ID})
    user2 = User(client, {'id': ASSIGNED_TO_ID + 1})

    result.client.api.user_by_id.return_value = {'id': ASSIGNED_TO_ID}

    assert empty_result.assigned_to is None
    empty_result.assigned_to = user1
    assert empty_result._content['assignedto_id'] == ASSIGNED_TO_ID

    assert result.assigned_to.id == ASSIGNED_TO_ID
    result.assigned_to = user2
    assert result._content['assignedto_id'] == ASSIGNED_TO_ID + 1

    result.client.api.user_by_id.assert_called_with(ASSIGNED_TO_ID)


def test_assigned_to_set_exc(client, empty_result):

    assert empty_result.assigned_to is None

    with pytest.raises(TypeError) as exc:
        empty_result.assigned_to = 1234

    assert str(User) in str(exc)
    assert str(int) in str(exc)


def test_comment_get(empty_result, result):
    assert empty_result.comment is None
    assert result.comment == COMMENT


def test_comment_set(empty_result, result):
    empty_result.comment = COMMENT
    assert empty_result.comment == COMMENT

    result.comment = COMMENT + " addition"
    assert result.comment == COMMENT + " addition"


def test_comment_set_exc(empty_result):
    with pytest.raises(TypeError) as exc:
        empty_result.comment = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_created_by(empty_result, result):
    result.client.api.user_by_id.return_value = {'id': CREATED_BY_ID}

    assert empty_result.assigned_to is None
    assert isinstance(result.created_by, User)
    assert result.created_by.id == CREATED_BY_ID

    result.client.api.user_by_id.assert_called_with(CREATED_BY_ID)


def test_created_on(empty_result, result):
    assert empty_result.created_on is None
    assert isinstance(result.created_on, dt)


def test_defects_get(empty_result, result):
    assert list(empty_result.defects) == list()
    assert len(list(result.defects)) == 3
    assert all(map(lambda x: isinstance(x, str), result.defects))
    assert DEF1 in result.defects
    assert DEF2 in result.defects
    assert DEF3 in result.defects


def test_defects_set_str_1(empty_result):
    assert list(empty_result.defects) == list()

    empty_result.defects = str(DEF1)

    assert empty_result._content['defects'] == DEF1


def test_defects_set_str_2(empty_result):
    assert list(empty_result.defects) == list()

    empty_result.defects = ','.join([DEF1, DEF2])

    assert empty_result._content['defects'] == '{0},{1}'.format(DEF1, DEF2)


def test_defects_set_list(empty_result):
    assert list(empty_result.defects) == list()

    empty_result.defects = [DEF1, DEF2]

    assert empty_result._content['defects'] == '{0},{1}'.format(DEF1, DEF2)


def test_defects_set_exc_1(empty_result):
    assert list(empty_result.defects) == list()

    with pytest.raises(TypeError) as exc:
        empty_result.defects = 1234

    assert 'Found 1234' in str(exc)
    assert 'DEFECT1,DEFECT2' in str(exc)


def test_defects_set_exc_2(empty_result):
    assert list(empty_result.defects) == list()

    with pytest.raises(TypeError) as exc:
        empty_result.defects = [1234, 5678]

    assert 'Found [1234, 5678]' in str(exc)
    assert 'DEFECT1,DEFECT2' in str(exc)


def test_elapsed_get(empty_result, result):
    assert empty_result.elapsed is None
    assert isinstance(result.elapsed, timedelta)
    assert result.elapsed == timedelta(seconds=605)


def test_elapsed_set(empty_result):
    assert empty_result.elapsed is None

    empty_result.elapsed = timedelta(seconds=123)

    assert empty_result._content['elapsed'] == 123


def test_elapsed_exc(empty_result):
    assert empty_result.elapsed is None

    with pytest.raises(TypeError) as exc:
        empty_result.elapsed = 'asdf'

    assert str(timedelta) in str(exc)
    assert str(str) in str(exc)


def test_status_get(empty_result, result):
    assert empty_result.status is None

    result.client.api.statuses.return_value = [{'id': STATUS_ID - 1},
                                               {'id': STATUS_ID},
                                               {'id': STATUS_ID + 1}]

    assert isinstance(result.status, Status)
    assert result.status.id == STATUS_ID
    result.client.api.statuses.assert_called_with()


def test_status_set(client, empty_result, result):
    status1 = Status(client, {'id': STATUS_ID})
    status2 = Status(client, {'id': STATUS_ID + 1})

    result.client.api.statuses.return_value = [{'id': STATUS_ID - 1},
                                               {'id': STATUS_ID},
                                               {'id': STATUS_ID + 1}]

    assert empty_result.status is None
    empty_result.status = status1
    assert empty_result._content['status_id'] == STATUS_ID

    assert result.status.id == STATUS_ID
    result.status = status2
    assert result._content['status_id'] == STATUS_ID + 1

    result.client.api.statuses.assert_called_with()


def test_status_set_exc(client, empty_result):

    assert empty_result.status is None

    with pytest.raises(TypeError) as exc:
        empty_result.status = 1234

    assert str(Status) in str(exc)
    assert str(int) in str(exc)


def test_test_get(empty_result, result):
    assert empty_result.test is None

    result.client.api.test_by_id.return_value = {'id': TEST_ID}

    assert isinstance(result.test, _Test)
    assert result.test.id == TEST_ID
    result.client.api.test_by_id.assert_called_with(TEST_ID)


def test_test_set(client, empty_result, result):
    test1 = _Test(client, {'id': TEST_ID})
    test2 = _Test(client, {'id': TEST_ID + 1})

    result.client.api.test_by_id.return_value = {'id': TEST_ID}

    assert empty_result.test is None
    empty_result.test = test1
    assert empty_result._content['test_id'] == TEST_ID

    assert result.test.id == TEST_ID
    result.test = test2
    assert result._content['test_id'] == TEST_ID + 1

    result.client.api.test_by_id.assert_called_with(TEST_ID)


def test_test_set_exc(client, empty_result):

    assert empty_result.test is None

    with pytest.raises(TypeError) as exc:
        empty_result.test = 1234

    assert str(_Test) in str(exc)
    assert str(int) in str(exc)


def test_version_get(empty_result, result):
    assert empty_result.version is None
    assert result.version == VERSION


def test_version_set(empty_result, result):
    empty_result.version = VERSION
    assert empty_result.version == VERSION

    result.version = VERSION + " addition"
    assert result.version == VERSION + " addition"


def test_version_set_exc(empty_result):
    with pytest.raises(TypeError) as exc:
        empty_result.version = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)
