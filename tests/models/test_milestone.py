from copy import deepcopy
from datetime import datetime as dt

import pytest

from traw.models import Milestone, Project, SubMilestone

COMPLETED_ON = 1469726522
DESCRIPTION = "mock milestone description"
DUE_ON = 1469726333
ID = 123
NAME = 'mock name'
PARENT_ID = 1234
PROJECT_ID = 15
START_ON = 1469726444
STARTED_ON = 1469726555
URL = 'mock url'


@pytest.fixture()
def new_milestone(client):
    return Milestone(client)


@pytest.fixture()
def milestone(client):
    content = {"completed_on": COMPLETED_ON,
               "description": DESCRIPTION,
               "due_on": DUE_ON,
               "id": ID,
               "is_completed": False,
               "is_started": False,
               "name": NAME,
               "project_id": PROJECT_ID,
               "start_on": START_ON,
               "started_on": STARTED_ON,
               "url": URL}
    return Milestone(client, deepcopy(content))


@pytest.fixture()
def sub_milestone(client):
    content = {"completed_on": COMPLETED_ON,
               "description": DESCRIPTION,
               "due_on": DUE_ON,
               "id": ID,
               "is_completed": False,
               "is_started": False,
               "is_completed": False,
               "name": NAME,
               "parent_id": PARENT_ID,
               "project_id": PROJECT_ID,
               "start_on": START_ON,
               "started_on": STARTED_ON,
               "url": URL}
    return SubMilestone(client, deepcopy(content))


def test_completed_on(new_milestone, milestone):
    assert new_milestone.completed_on is None
    assert isinstance(milestone.completed_on, dt)
    assert milestone.completed_on == dt.fromtimestamp(COMPLETED_ON)


def test_description_get(new_milestone, milestone):
    assert new_milestone.description is None
    assert milestone.description == DESCRIPTION


def test_description_set(new_milestone, milestone):
    new_milestone.description = "New description 1"
    assert new_milestone.description == "New description 1"

    milestone.description = "New description 2"
    assert milestone.description == "New description 2"


def test_description_set_exc(new_milestone):
    with pytest.raises(TypeError) as exc:
        new_milestone.description = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_due_on_get(new_milestone, milestone):
    assert new_milestone.due_on is None
    assert isinstance(milestone.due_on, dt)
    assert milestone.due_on == dt.fromtimestamp(DUE_ON)


def test_due_on_set(new_milestone):
    assert new_milestone.due_on is None

    new_milestone.due_on = dt.fromtimestamp(DUE_ON)

    assert isinstance(new_milestone.due_on, dt)
    assert new_milestone.due_on == dt.fromtimestamp(DUE_ON)


def test_due_on_set_exc(new_milestone):
    with pytest.raises(TypeError) as exc:
        new_milestone.due_on = 1234

    assert str(dt) in str(exc)
    assert str(int) in str(exc)


def test_is_completed_get(new_milestone, milestone):
    assert new_milestone.is_completed is False
    assert milestone.is_completed is False


def test_is_completed_set(milestone):
    assert milestone.is_completed is False

    milestone.is_completed = True

    assert milestone.is_completed is True


def test_is_completed_set_exc(new_milestone):
    with pytest.raises(TypeError) as exc:
        new_milestone.is_completed = 1234

    assert str(bool) in str(exc)
    assert str(int) in str(exc)


def test_is_started_get(new_milestone, milestone):
    assert new_milestone.is_started is False
    assert milestone.is_started is False


def test_is_started_set(milestone):
    assert milestone.is_started is False

    milestone.is_started = True

    assert milestone.is_started is True


def test_is_started_set_exc(new_milestone):
    with pytest.raises(TypeError) as exc:
        new_milestone.is_started = 1234

    assert str(bool) in str(exc)
    assert str(int) in str(exc)


def test_name_get(new_milestone, milestone):
    assert new_milestone.name is None
    assert milestone.name is NAME


def test_name_set(new_milestone, milestone):
    new_milestone.name = NAME
    assert new_milestone.name == NAME

    milestone.name = NAME
    assert milestone.name == NAME


def test_name_set_exc(new_milestone):
    with pytest.raises(TypeError) as exc:
        new_milestone.name = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_project_get(new_milestone, milestone):
    assert new_milestone.project is None
    assert isinstance(milestone.project, Project)

    milestone.client.api.project_by_id.return_value = {'id': PROJECT_ID}

    assert milestone.project.id == PROJECT_ID
    milestone.client.api.project_by_id.assert_called_with(PROJECT_ID)


def test_project_set(new_milestone):
    project = Project(None, {'id': PROJECT_ID})
    new_milestone.project = project

    assert new_milestone._content['project_id'] == PROJECT_ID


def test_project_set_exc(new_milestone):
    with pytest.raises(TypeError) as exc:
        new_milestone.project = 1234

    assert str(Project) in str(exc)
    assert str(int) in str(exc)


def test_start_on_get(new_milestone, milestone):
    assert new_milestone.start_on is None
    assert isinstance(milestone.start_on, dt)
    assert milestone.start_on == dt.fromtimestamp(START_ON)


def test_start_on_set(new_milestone):
    assert new_milestone.start_on is None

    new_milestone.start_on = dt.fromtimestamp(START_ON)

    assert isinstance(new_milestone.start_on, dt)
    assert new_milestone.start_on == dt.fromtimestamp(START_ON)


def test_start_on_set_exc(new_milestone):
    with pytest.raises(TypeError) as exc:
        new_milestone.start_on = 1234

    assert str(dt) in str(exc)
    assert str(int) in str(exc)


def test_started_on_get(new_milestone, milestone):
    assert new_milestone.started_on is None
    assert isinstance(milestone.started_on, dt)
    assert milestone.started_on == dt.fromtimestamp(STARTED_ON)


def test_started_on_set(new_milestone):
    assert new_milestone.started_on is None

    new_milestone.started_on = dt.fromtimestamp(STARTED_ON)

    assert isinstance(new_milestone.started_on, dt)
    assert new_milestone.started_on == dt.fromtimestamp(STARTED_ON)


def test_started_on_set_exc(new_milestone):
    with pytest.raises(TypeError) as exc:
        new_milestone.started_on = 1234

    assert str(dt) in str(exc)
    assert str(int) in str(exc)


def test_url(new_milestone, milestone):
    assert new_milestone.url is None
    assert isinstance(milestone.url, str)
    assert milestone.url == URL


def test_add_parent_milestone_by_id(new_milestone):
    sub_milestone = new_milestone.add_parent(PARENT_ID)

    assert isinstance(sub_milestone, SubMilestone)
    assert sub_milestone._content['parent_id'] == PARENT_ID


def test_add_parent_milestone_by_milestone(new_milestone, milestone):
    sub_milestone = new_milestone.add_parent(milestone)

    assert isinstance(sub_milestone, SubMilestone)
    assert sub_milestone._content['parent_id'] == milestone.id


def test_add_parent_exc(new_milestone):
    with pytest.raises(TypeError) as exc:
        new_milestone.add_parent('asdf')

    assert str(int) in str(exc)
    assert str(str) in str(exc)
    assert str(Milestone) in str(exc)


def test_sub_milestone_parent_get(sub_milestone):
    sub_milestone.client.api.milestone_by_id.return_value = {'id': PARENT_ID}

    assert isinstance(sub_milestone.parent, Milestone)
    assert sub_milestone.parent.id == PARENT_ID
    sub_milestone.client.api.milestone_by_id.assert_called_with(PARENT_ID)


def test_sub_milestone_parent_set_type_error_exc(sub_milestone):
    with pytest.raises(TypeError) as exc:
        sub_milestone.parent = 1234

    assert str(Milestone) in str(exc)
    assert str(int) in str(exc)


def test_sub_milestone_parent_set_value_error_exc(sub_milestone, milestone):
    sub_milestone._content['project_id'] = None
    with pytest.raises(ValueError) as exc:
        sub_milestone.parent = milestone

    assert 'existing project first' in str(exc)


def test_sub_milestone_parent_set_value_error_project_mismatch_exc(sub_milestone, milestone):
    sub_milestone.client.api.project_by_id.side_effect = [
        {'id': 12345}, {'id': 12345}, {'id': PROJECT_ID}, {'id': 12345}, {'id': PROJECT_ID}]
    sub_milestone._content['project_id'] = 12345
    with pytest.raises(ValueError) as exc:
        sub_milestone.parent = milestone

    assert str(12345) in str(exc)
    assert str(PROJECT_ID) in str(exc)


def test_sub_milestone_parent_set(sub_milestone, milestone):
    milestone._content['id'] = 9876
    sub_milestone.client.api.project_by_id.side_effect = [
        {'id': PROJECT_ID}, {'id': PROJECT_ID}, {'id': PROJECT_ID}]
    sub_milestone.parent = milestone

    assert sub_milestone._content['parent_id'] == 9876


def test_sub_milestones_no_extra_api_call(milestone):
    milestone._content['milestones'] = [{'id': 333}, {'id': 444}]

    assert all([isinstance(sub, SubMilestone) for sub in milestone.sub_milestones])
    assert len(list(milestone.sub_milestones)) == 2
    assert not milestone.client.api.milestone_by_id.called


def test_sub_milestones_with_api_call(milestone):
    milestone.client.api.milestone_by_id.side_effect = [{'milestones': [{'id': 333}, {'id': 444}]}]

    assert all([isinstance(sub, SubMilestone) for sub in milestone.sub_milestones])
    assert len(list(milestone.sub_milestones)) == 2
    milestone.client.api.milestone_by_id.assert_called_once_with(milestone.id)
