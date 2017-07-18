from copy import deepcopy
from datetime import timedelta

import pytest

from traw.models import Test as _Test  # To avoid tox test collection warning
from traw.models import Case, CaseType, Milestone, Priority, Run, Status, User

CASE_ID = 11
CUSTOM_EXP_COND = "mock custom expected condition"
CUSTOM_PRECOND = "mock custom precondition"
ID = 123
MILESTONE_ID = 66
PRIORITY_ID = 22
REF1 = 'REF1'
REF2 = 'REF2'
REF3 = 'REF3'
REF4 = 'REF4'
RUN_ID = 33
STATUS_ID = 44
TITLE = "mock test title"
TYPE_ID = 55
USER_ID = 99


@pytest.fixture()
def empty_test(client):
    return _Test(client)


@pytest.fixture()
def test(client):
    content = {"assignedto_id": USER_ID,
               "case_id": CASE_ID,
               "custom_expected": CUSTOM_EXP_COND,
               "custom_preconds": CUSTOM_PRECOND,
               "custom_steps_separated": [
                   {
                       "content": "Step 1",
                       "expected": "Expected Result 1"
                   },
                   {
                       "content": "Step 2",
                       "expected": "Expected Result 2"
                   }
               ],
               "estimate": "1m 5s",
               "estimate_forecast": "10d 11h",
               "id": ID,
               "milestone_id": MILESTONE_ID,
               "priority_id": PRIORITY_ID,
               "refs": ",".join([REF1, REF2, REF3, REF4]),
               "run_id": RUN_ID,
               "status_id": STATUS_ID,
               "title": TITLE,
               "type_id": TYPE_ID}
    return _Test(client, deepcopy(content))


def test_assigned_to(empty_test, test):
    assert empty_test.assigned_to is None

    test.client.api.user_by_id.return_value = {'id': USER_ID}

    assert isinstance(test.assigned_to, User)
    assert test.assigned_to.id == USER_ID
    test.client.api.user_by_id.assert_called_with(USER_ID)


def test_case(empty_test, test):
    with pytest.raises(KeyError) as exc:
        empty_test.case

    assert 'case_id' in str(exc)

    test.client.api.case_by_id.return_value = {'id': CASE_ID}

    assert isinstance(test.case, Case)
    assert test.case.id == CASE_ID
    test.client.api.case_by_id.assert_called_with(CASE_ID)


def test_estimate(empty_test, test):
    assert empty_test.estimate is None
    assert isinstance(test.estimate, timedelta)
    assert test.estimate == timedelta(seconds=65)


def test_estimate_forecast(empty_test, test):
    assert empty_test.estimate_forecast is None
    assert isinstance(test.estimate_forecast, timedelta)
    assert test.estimate_forecast == timedelta(days=10, seconds=39600)


def test_milestone(empty_test, test):
    assert empty_test.milestone is None

    test.client.api.milestone_by_id.return_value = {'id': MILESTONE_ID}

    assert isinstance(test.milestone, Milestone)
    assert test.milestone.id == MILESTONE_ID
    test.client.api.milestone_by_id.assert_called_with(MILESTONE_ID)


def test_priority(empty_test, test):
    with pytest.raises(KeyError) as exc:
        empty_test.priority

    assert 'priority_id' in str(exc)

    test.client.api.priorities.return_value = [{'id': 998}, {'id': PRIORITY_ID}, {'id': 999}]

    assert isinstance(test.priority, Priority)
    assert test.priority.id == PRIORITY_ID
    assert test.client.api.priorities.call_count == 2


def test_refs(empty_test, test):
    assert list(empty_test.refs) == list()
    assert len(list(test.refs)) == 4
    assert all(map(lambda x: isinstance(x, str), test.refs))
    assert REF1 in test.refs
    assert REF2 in test.refs
    assert REF3 in test.refs
    assert REF4 in test.refs


def test_run(empty_test, test):
    with pytest.raises(KeyError) as exc:
        empty_test.run

    assert 'run_id' in str(exc)

    test.client.api.run_by_id.return_value = {'id': RUN_ID}

    assert isinstance(test.run, Run)
    assert test.run.id == RUN_ID
    test.client.api.run_by_id.assert_called_with(RUN_ID)


def test_status(empty_test, test):
    with pytest.raises(KeyError) as exc:
        empty_test.status

    assert 'status_id' in str(exc)

    test.client.api.statuses.return_value = [{'id': 998}, {'id': STATUS_ID}, {'id': 999}]

    assert isinstance(test.status, Status)
    assert test.status.id == STATUS_ID
    assert test.client.api.statuses.call_count == 2


def test_title(empty_test, test):
    with pytest.raises(KeyError) as exc:
        empty_test.title

    assert 'title' in str(exc)

    assert isinstance(test.title, str)
    assert test.title == TITLE


def test_type(empty_test, test):
    with pytest.raises(KeyError) as exc:
        empty_test.type

    assert 'type_id' in str(exc)

    test.client.api.case_types.return_value = [{'id': 998}, {'id': TYPE_ID}, {'id': 999}]

    assert isinstance(test.type, CaseType)
    assert test.type.id == TYPE_ID
    assert test.client.api.case_types.call_count == 2
