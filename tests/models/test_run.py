from copy import deepcopy
import datetime

from mock import call
import pytest

from traw.models import Case, Config, Milestone, Plan, Project, Run, Suite, User

CONF1_ID = 3
CONF2_ID = 4
CG1_ID = 17

ASSIGNED_TO_ID = 1
BLOCKED_COUNT = 2
COMPLETED_ON = 1469726522
CONFIGS = [CONF1_ID, CONF2_ID]
CREATED_BY_ID = 5
CREATED_ON = 1469725522
DESCRIPTION = "mock run description"
FAILED_COUNT = 6
ID = 7
MILESTONE_ID = 8
NAME = 'mock name'
PASSED_COUNT = 9
PLAN_ID = 10
PROJECT_ID = 11
RETEST_COUNT = 12
SUITE_ID = 13
UNTESTED_COUNT = 14
URL = 'mock url'

CASE1_ID = 15
CASE2_ID = 16
CASE1 = {'id': CASE1_ID}
CASE2 = {'id': CASE2_ID}

CONF3 = {'id': 3}
CONF4 = {'id': 4}

CG1 = {'id': CG1_ID, 'configs': [CONF3, CONF4]}


@pytest.fixture()
def new_run(client):
    return Run(client)


@pytest.fixture()
def run(client):
    content = {'assignedto_id': ASSIGNED_TO_ID,
               'blocked_count': BLOCKED_COUNT,
               'case_ids': [CASE1_ID, CASE2_ID],
               'completed_on': COMPLETED_ON,
               'config': None,
               'config_ids': CONFIGS,
               'created_by': CREATED_BY_ID,
               'created_on': CREATED_ON,
               'custom_status1_count': 11,
               'custom_status2_count': 22,
               'custom_status3_count': 33,
               'custom_status4_count': 44,
               'custom_status5_count': 55,
               'custom_status6_count': 66,
               'custom_status7_count': 77,
               'description': DESCRIPTION,
               'failed_count': FAILED_COUNT,
               'id': ID,
               'include_all': False,
               'is_completed': True,
               'milestone_id': MILESTONE_ID,
               'name': NAME,
               'passed_count': PASSED_COUNT,
               'plan_id': PLAN_ID,
               'project_id': PROJECT_ID,
               'retest_count': RETEST_COUNT,
               'suite_id': SUITE_ID,
               'untested_count': UNTESTED_COUNT,
               'url': URL}
    return Run(client, deepcopy(content))


def test_assigned_to_get(new_run, run):
    run.client.api.user_by_id.return_value = {'id': ASSIGNED_TO_ID}

    assert new_run.assigned_to is None
    assert isinstance(run.assigned_to, User)
    assert run.assigned_to.id == ASSIGNED_TO_ID

    run.client.api.user_by_id.assert_called_with(ASSIGNED_TO_ID)


def test_assigned_to_set(client, new_run, run):
    user1 = User(client, {'id': ASSIGNED_TO_ID})
    user2 = User(client, {'id': ASSIGNED_TO_ID + 1})

    run.client.api.user_by_id.return_value = {'id': ASSIGNED_TO_ID}

    assert new_run.assigned_to is None
    new_run.assigned_to = user1
    assert new_run._content['assignedto_id'] == ASSIGNED_TO_ID

    assert run.assigned_to.id == ASSIGNED_TO_ID
    run.assigned_to = user2
    assert run._content['assignedto_id'] == ASSIGNED_TO_ID + 1

    run.client.api.user_by_id.assert_called_with(ASSIGNED_TO_ID)


def test_assigned_to_set_exc(client, new_run, run):

    assert new_run.assigned_to is None

    with pytest.raises(TypeError) as exc:
        new_run.assigned_to = 1234

    assert str(User) in str(exc)
    assert str(int) in str(exc)


def test_blocked_count(new_run, run):
    assert new_run.blocked_count is None
    assert run.blocked_count == BLOCKED_COUNT


def test_cases_get(new_run, run):
    run.client.api.case_by_id.side_effect = [CASE1, CASE2]

    assert list(new_run.cases) == list()

    cases = run.cases
    case1 = next(cases)
    assert isinstance(case1, Case)
    assert case1.id == CASE1_ID

    case2 = next(cases)
    assert isinstance(case2, Case)
    assert case2.id == CASE2_ID

    assert call(CASE1_ID) in run.client.api.case_by_id.call_args_list
    assert call(CASE2_ID) in run.client.api.case_by_id.call_args_list


def test_cases_set_list(new_run):
    assert list(new_run.cases) == list()
    new_run.cases = list()
    assert list(new_run.cases) == list()
    new_run.cases = [Case(None, CASE1), Case(None, CASE2)]
    assert new_run._content['case_ids'] == [CASE1_ID, CASE2_ID]


def test_cases_set_set(new_run):
    assert set(new_run.cases) == set()
    new_run.cases = set()
    assert set(new_run.cases) == set()
    new_run.cases = {Case(None, CASE1), Case(None, CASE2)}
    assert new_run._content['case_ids'].count(CASE1_ID) == 1
    assert new_run._content['case_ids'].count(CASE2_ID) == 1


def test_cases_set_tuple(new_run):
    assert tuple(new_run.cases) == tuple()
    new_run.cases = tuple()
    assert tuple(new_run.cases) == tuple()
    new_run.cases = (Case(None, CASE1), Case(None, CASE2))
    assert new_run._content['case_ids'] == [CASE1_ID, CASE2_ID]


def test_cases_set_generator(new_run):
    assert list(new_run.cases) == list()
    new_run.cases = (x for x in range(1) if x == 'a')  # an empty generator
    assert list(new_run.cases) == list()
    new_run.cases = (c for c in [Case(None, CASE1), Case(None, CASE2)])
    assert new_run._content['case_ids'] == [CASE1_ID, CASE2_ID]


def test_cases_set_list_exc(new_run):
    assert list(new_run.cases) == list()

    with pytest.raises(TypeError) as exc:
        new_run.cases = "1, 2"

    assert 'generator). Found {0}'.format(str) in str(exc)


def test_cases_set_type_exc(new_run):
    assert list(new_run.cases) == list()

    with pytest.raises(TypeError) as exc:
        new_run.cases = [Case(None, CASE1), '2']

    assert 'Found at least one {0}'.format(str) in str(exc)


def test_cases_set_type_exc_2(new_run):
    assert list(new_run.cases) == list()

    with pytest.raises(TypeError) as exc:
        new_run.cases = [CASE1_ID, CASE2]

    assert 'Found at least one {0}'.format(dict) in str(exc)


def test_completed_on(new_run, run):
    assert new_run.completed_on is None
    assert isinstance(run.completed_on, datetime.datetime)


def test_configs(new_run, run):
    assert list(new_run.configs) == list()

    run.client.api.project_by_id.return_value = {'id': PROJECT_ID}
    run.client.api.config_groups.return_value = [CG1]

    configs = run.configs

    conf1 = next(configs)
    assert isinstance(conf1, Config)
    assert conf1.id == CONF1_ID

    conf2 = next(configs)
    assert isinstance(conf2, Config)
    assert conf2.id == CONF2_ID

    run.client.api.project_by_id.assert_called_with(PROJECT_ID)
    run.client.api.config_groups.assert_called_with(PROJECT_ID)


def test_created_by(new_run, run):
    run.client.api.user_by_id.return_value = {'id': CREATED_BY_ID}

    assert new_run.assigned_to is None
    assert isinstance(run.created_by, User)
    assert run.created_by.id == CREATED_BY_ID

    run.client.api.user_by_id.assert_called_with(CREATED_BY_ID)


def test_created_on(new_run, run):
    assert new_run.created_on is None
    assert isinstance(run.created_on, datetime.datetime)


def test_description_get(new_run, run):
    assert new_run.description is None
    assert run.description == DESCRIPTION


def test_description_set(new_run, run):
    new_run.description = "New description 1"
    assert new_run.description == "New description 1"

    run.description = "New description 2"
    assert run.description == "New description 2"


def test_description_set_exc(new_run):
    with pytest.raises(TypeError) as exc:
        new_run.description = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_failed_count(new_run, run):
    assert new_run.failed_count is None
    assert run.failed_count == FAILED_COUNT


def test_include_all(new_run, run):
    assert new_run.include_all is True
    assert run.include_all is False


def test_include_all_set(run):
    assert run.include_all is False

    run.include_all = True

    assert run.include_all is True


def test_include_all_set_exc(new_run):
    with pytest.raises(TypeError) as exc:
        new_run.include_all = 1234

    assert str(bool) in str(exc)
    assert str(int) in str(exc)


def test_is_completed(new_run, run):
    assert new_run.is_completed is False
    assert run.is_completed is True


def test_milestone_get(new_run, run):
    assert new_run.milestone is None

    run.client.api.milestone_by_id.return_value = {'id': MILESTONE_ID}

    assert isinstance(run.milestone, Milestone)
    assert run.milestone.id == MILESTONE_ID
    run.client.api.milestone_by_id.assert_called_with(MILESTONE_ID)


def test_milestone_set(new_run):
    assert new_run.milestone is None

    new_run.milestone = Milestone(None, {'id': MILESTONE_ID})

    assert new_run._content['milestone_id'] == MILESTONE_ID


def test_milestone_set_exc(new_run):
    assert new_run.milestone is None

    with pytest.raises(TypeError) as exc:
        new_run.milestone = 1234

    assert str(Milestone) in str(exc)
    assert str(int) in str(exc)


def test_name_get(new_run, run):
    assert new_run.name is None
    assert run.name is NAME


def test_name_set(new_run, run):
    new_run.name = NAME
    assert new_run.name == NAME

    run.name = NAME + " addition"
    assert run.name == NAME + " addition"


def test_name_set_exc(new_run):
    with pytest.raises(TypeError) as exc:
        new_run.name = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_passed_count(new_run, run):
    assert new_run.passed_count is None
    assert run.passed_count == PASSED_COUNT


def test_plan(new_run, run):
    assert new_run.plan is None

    run.client.api.plan_by_id.return_value = {'id': PLAN_ID}

    assert isinstance(run.plan, Plan)
    assert run.plan.id == PLAN_ID
    run.client.api.plan_by_id.assert_called_with(PLAN_ID)


def test_project_get(new_run, run):
    run.client.api.project_by_id.return_value = {'id': PROJECT_ID}

    assert new_run.project is None
    assert isinstance(run.project, Project)

    assert run.project.id == PROJECT_ID
    run.client.api.project_by_id.assert_called_with(PROJECT_ID)


def test_project_set(new_run):
    project = Project(None, {'id': PROJECT_ID})
    new_run.project = project

    assert new_run._content['project_id'] == PROJECT_ID


def test_project_set_exc(new_run):
    with pytest.raises(TypeError) as exc:
        new_run.project = 1234

    assert str(Project) in str(exc)
    assert str(int) in str(exc)


def test_retest_count(new_run, run):
    assert new_run.retest_count is None
    assert run.retest_count == RETEST_COUNT


def test_suite_get(new_run, run):
    run.client.api.suite_by_id.return_value = {'id': SUITE_ID}

    assert new_run.suite is None
    assert isinstance(run.suite, Suite)

    assert run.suite.id == SUITE_ID
    run.client.api.suite_by_id.assert_called_with(SUITE_ID)


def test_suite_set(new_run):
    suite = Suite(None, {'id': SUITE_ID})
    new_run.suite = suite

    assert new_run._content['suite_id'] == SUITE_ID


def test_suite_set_exc(new_run):
    with pytest.raises(TypeError) as exc:
        new_run.suite = 1234

    assert str(Suite) in str(exc)
    assert str(int) in str(exc)


def test_untested_count(new_run, run):
    assert new_run.untested_count is None
    assert run.untested_count == UNTESTED_COUNT


def test_url(new_run, run):
    assert new_run.url is None
    assert isinstance(run.url, str)
    assert run.url == URL
