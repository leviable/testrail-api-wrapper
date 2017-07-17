from copy import deepcopy
from datetime import datetime as dt

import pytest

from traw.models import Project, Suite

COMPLETED_ON = 1469726522
DESCRIPTION = "mock suite description"
ID = 123
NAME = 'mock name'
PROJECT_ID = 15
URL = 'mock url'


@pytest.fixture()
def new_suite(client):
    return Suite(client)


@pytest.fixture()
def suite(client):
    content = {"completed_on": COMPLETED_ON,
               "description": DESCRIPTION,
               "id": ID,
               "is_baseline": False,
               "is_completed": False,
               "is_master": False,
               "name": NAME,
               "project_id": PROJECT_ID,
               "url": URL}
    return Suite(client, deepcopy(content))


def test_completed_on(new_suite, suite):
    assert new_suite.completed_on is None
    assert isinstance(suite.completed_on, dt)
    assert suite.completed_on == dt.fromtimestamp(COMPLETED_ON)


def test_description_get(new_suite, suite):
    assert new_suite.description is None
    assert suite.description == DESCRIPTION


def test_description_set(new_suite, suite):
    new_suite.description = "New description 1"
    assert new_suite.description == "New description 1"

    suite.description = "New description 2"
    assert suite.description == "New description 2"


def test_description_set_exc(new_suite):
    with pytest.raises(TypeError) as exc:
        new_suite.description = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_is_baseline(new_suite, suite):
    assert new_suite.is_baseline is False
    assert suite.is_baseline is False


def test_is_completed(new_suite, suite):
    assert new_suite.is_completed is False
    assert suite.is_completed is False


def test_is_master(new_suite, suite):
    assert new_suite.is_master is False
    assert suite.is_master is False


def test_name_get(new_suite, suite):
    assert new_suite.name is None
    assert suite.name == NAME


def test_name_set(new_suite, suite):
    assert new_suite.name is None
    new_suite.name = "New Suite Name"
    assert new_suite.name == "New Suite Name"

    assert suite.name == NAME
    suite.name = "New Suite Name"
    assert suite.name == "New Suite Name"


def test_name_set_exc(new_suite):
    with pytest.raises(TypeError) as exc:
        new_suite.name = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_project_get(new_suite, suite):
    assert new_suite.project is None
    assert isinstance(suite.project, Project)

    suite.client.api.project_by_id.return_value = {'id': PROJECT_ID}

    assert suite.project.id == PROJECT_ID
    suite.client.api.project_by_id.assert_called_with(PROJECT_ID)


def test_project_set(new_suite):
    project = Project(None, {'id': PROJECT_ID})
    new_suite.project = project

    assert new_suite._content['project_id'] == PROJECT_ID


def test_project_set_exc(new_suite):
    with pytest.raises(TypeError) as exc:
        new_suite.project = 1234

    assert str(Project) in str(exc)
    assert str(int) in str(exc)


def test_url(new_suite, suite):
    assert new_suite.url is None
    assert isinstance(suite.url, str)
    assert suite.url == URL
