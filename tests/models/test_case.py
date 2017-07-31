from copy import deepcopy
import datetime

import pytest

from traw.models import (Case, CaseType, Milestone, Priority, Section, Suite,
                         Template, User)


CREATED_BY_ID = 1
CREATED_ON = 1469725522
ID = 2
MILESTONE_ID = 3
PRIORITY_ID = 4
PROJECT_ID = 5
REF1 = 'REF1'
REF2 = 'REF2'
REF3 = 'REF3'
REF4 = 'REF4'
SECTION_ID = 6
SUITE_ID = 7
TEMPLATE_ID = 8
TITLE = 'mock title'
CASE_TYPE_ID = 9
UPDATED_BY_ID = 10
UPDATED_ON = 1469726522


@pytest.fixture()
def new_case(client):
    return Case(client)


@pytest.fixture()
def case(client):
    content = {'created_by': CREATED_BY_ID,
               'created_on': CREATED_ON,
               "estimate": "1m 5s",
               "estimate_forecast": "10d 11h",
               'id': ID,
               'milestone_id': MILESTONE_ID,
               'priority_id': PRIORITY_ID,
               "refs": ",".join([REF1, REF2, REF3, REF4]),
               'section_id': SECTION_ID,
               'suite_id': SUITE_ID,
               'template_id': TEMPLATE_ID,
               'title': TITLE,
               'type_id': CASE_TYPE_ID,
               'updated_by': UPDATED_BY_ID,
               'updated_on': UPDATED_ON}
    return Case(client, deepcopy(content))


def test_created_by(new_case, case):
    case.client.api.user_by_id.return_value = {'id': CREATED_BY_ID}

    assert new_case.created_by is None
    assert isinstance(case.created_by, User)
    assert case.created_by.id == CREATED_BY_ID

    case.client.api.user_by_id.assert_called_with(CREATED_BY_ID)


def test_created_on(new_case, case):
    assert new_case.created_on is None
    assert isinstance(case.created_on, datetime.datetime)


def test_estimate_get(new_case, case):
    assert new_case.estimate is None
    assert isinstance(case.estimate, datetime.timedelta)
    assert case.estimate == datetime.timedelta(seconds=65)


def test_estimate_set(new_case):
    assert new_case.estimate is None

    new_case.estimate = datetime.timedelta(seconds=123)

    assert new_case._content['estimate'] == 123


def test_estimate_exc(new_case):
    assert new_case.estimate is None

    with pytest.raises(TypeError) as exc:
        new_case.estimate = 'asdf'

    assert str(datetime.timedelta) in str(exc)
    assert str(str) in str(exc)


def test_estimate_forecast(new_case, case):
    assert new_case.estimate_forecast is None
    assert isinstance(case.estimate_forecast, datetime.timedelta)
    assert case.estimate_forecast == datetime.timedelta(days=10, seconds=39600)


def test_milestone_get(new_case, case):
    assert new_case.milestone is None

    case.client.api.milestone_by_id.return_value = {'id': MILESTONE_ID}

    assert isinstance(case.milestone, Milestone)
    assert case.milestone.id == MILESTONE_ID
    case.client.api.milestone_by_id.assert_called_with(MILESTONE_ID)


def test_milestone_set(new_case):
    assert new_case.milestone is None

    new_case.milestone = Milestone(None, {'id': MILESTONE_ID})

    assert new_case._content['milestone_id'] == MILESTONE_ID


def test_milestone_set_exc(new_case):
    assert new_case.milestone is None

    with pytest.raises(TypeError) as exc:
        new_case.milestone = 1234

    assert str(Milestone) in str(exc)
    assert str(int) in str(exc)


def test_priority_get(new_case, case):
    assert new_case.priority is None

    case.client.api.priorities.return_value = [{'id': PRIORITY_ID}, ]

    assert isinstance(case.priority, Priority)
    assert case.priority.id == PRIORITY_ID
    case.client.api.priorities.assert_called_with()


def test_priority_set(new_case):
    assert new_case.priority is None

    new_case.priority = Priority(None, {'id': PRIORITY_ID})

    assert new_case._content['priority_id'] == PRIORITY_ID


def test_priority_set_exc(new_case):
    assert new_case.priority is None

    with pytest.raises(TypeError) as exc:
        new_case.priority = 1234

    assert str(Priority) in str(exc)
    assert str(int) in str(exc)


def test_refs_get(new_case, case):
    assert list(new_case.refs) == list()
    assert len(list(case.refs)) == 4
    assert all(map(lambda x: isinstance(x, str), case.refs))
    assert REF1 in case.refs
    assert REF2 in case.refs
    assert REF3 in case.refs
    assert REF4 in case.refs


def test_refs_set_str_1(new_case):
    assert list(new_case.refs) == list()

    new_case.refs = str(REF1)

    assert new_case._content['refs'] == REF1


def test_refs_set_str_2(new_case):
    assert list(new_case.refs) == list()

    new_case.refs = ','.join([REF1, REF2])

    assert new_case._content['refs'] == '{0},{1}'.format(REF1, REF2)


def test_refs_set_list(new_case):
    assert list(new_case.refs) == list()

    new_case.refs = [REF1, REF2]

    assert new_case._content['refs'] == '{0},{1}'.format(REF1, REF2)


def test_refs_set_exc_1(new_case):
    assert list(new_case.refs) == list()

    with pytest.raises(TypeError) as exc:
        new_case.refs = 1234

    assert 'Found 1234' in str(exc)
    assert 'REF01,REF02' in str(exc)


def test_refs_set_exc_2(new_case):
    assert list(new_case.refs) == list()

    with pytest.raises(TypeError) as exc:
        new_case.refs = [1234, 5678]

    assert 'Found [1234, 5678]' in str(exc)
    assert 'REF01,REF02' in str(exc)


def test_section_get(new_case, case):
    assert new_case.section is None

    case.client.api.section_by_id.return_value = {'id': SECTION_ID}

    assert isinstance(case.section, Section)
    assert case.section.id == SECTION_ID
    case.client.api.section_by_id.assert_called_with(SECTION_ID)


def test_section_set(new_case):
    assert new_case.section is None

    new_case.section = Section(None, {'id': SECTION_ID})

    assert new_case._content['section_id'] == SECTION_ID


def test_section_set_exc(new_case):
    assert new_case.section is None

    with pytest.raises(TypeError) as exc:
        new_case.section = 1234

    assert str(Section) in str(exc)
    assert str(int) in str(exc)


def test_suite_get(new_case, case):
    case.client.api.suite_by_id.return_value = {'id': SUITE_ID}

    assert new_case.suite is None
    assert isinstance(case.suite, Suite)

    assert case.suite.id == SUITE_ID
    case.client.api.suite_by_id.assert_called_with(SUITE_ID)


def test_suite_set(new_case):
    suite = Suite(None, {'id': SUITE_ID})
    new_case.suite = suite

    assert new_case._content['suite_id'] == SUITE_ID


def test_suite_set_exc(new_case):
    with pytest.raises(TypeError) as exc:
        new_case.suite = 1234

    assert str(Suite) in str(exc)
    assert str(int) in str(exc)


def test_template_get(new_case, case):
    case.client.api.projects.return_value = [{'id': PROJECT_ID}, ]
    case.client.api.templates.return_value = [{'id': TEMPLATE_ID}, ]

    assert new_case.template is None
    assert isinstance(case.template, Template)

    assert case.template.id == TEMPLATE_ID
    case.client.api.templates.assert_called_with(PROJECT_ID)


def test_template_set(new_case):
    template = Template(None, {'id': TEMPLATE_ID})
    new_case.template = template

    assert new_case._content['template_id'] == TEMPLATE_ID


def test_template_set_exc(new_case):
    with pytest.raises(TypeError) as exc:
        new_case.template = 1234

    assert str(Template) in str(exc)
    assert str(int) in str(exc)


def test_title(new_case, case):
    assert new_case.title is None
    assert case.title is TITLE


def test_title_set(new_case, case):
    new_case.title = TITLE
    assert new_case.title == TITLE

    case.title = TITLE + " addition"
    assert case.title == TITLE + " addition"


def test_title_set_exc(new_case):
    with pytest.raises(TypeError) as exc:
        new_case.title = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_case_type_get(new_case, case):
    assert new_case.case_type is None

    case.client.api.case_types.return_value = [{'id': CASE_TYPE_ID}, ]

    assert isinstance(case.case_type, CaseType)
    assert case.case_type.id == CASE_TYPE_ID
    case.client.api.case_types.assert_called_with()


def test_case_type_set(new_case):
    assert new_case.case_type is None

    new_case.case_type = CaseType(None, {'id': CASE_TYPE_ID})

    assert new_case._content['type_id'] == CASE_TYPE_ID


def test_case_type_set_exc(new_case):
    assert new_case.case_type is None

    with pytest.raises(TypeError) as exc:
        new_case.case_type = 1234

    assert str(CaseType) in str(exc)
    assert str(int) in str(exc)


def test_updated_by(new_case, case):
    case.client.api.user_by_id.return_value = {'id': UPDATED_BY_ID}

    assert new_case.updated_by is None
    assert isinstance(case.updated_by, User)
    assert case.updated_by.id == UPDATED_BY_ID

    case.client.api.user_by_id.assert_called_with(UPDATED_BY_ID)


def test_updated_on(new_case, case):
    assert new_case.updated_on is None
    assert isinstance(case.updated_on, datetime.datetime)
