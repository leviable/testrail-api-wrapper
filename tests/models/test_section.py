from copy import deepcopy

import pytest

from traw.models import Project, Section, Suite

DEPTH = 1
DESCRIPTION = "mock section description"
DISPLAY_ORDER = 2
ID = 3
PARENT_ID = 4
NAME = 'mock name'
PROJECT_ID = 5
SECTION_ID = 6
SUITE_ID = 7


@pytest.fixture()
def new_section(client):
    return Section(client)


@pytest.fixture()
def section(client):
    content = {"depth": DEPTH,
               "description": DESCRIPTION,
               "display_order": DISPLAY_ORDER,
               "id": ID,
               "name": NAME,
               "parent_id": PARENT_ID,
               "project_id": PROJECT_ID,
               "suite_id": SUITE_ID}
    return Section(client, deepcopy(content))


def test_depth(new_section, section):
    assert new_section.depth is None
    assert section.depth == DEPTH


def test_description(new_section, section):
    assert new_section.description is None
    assert section.description == DESCRIPTION


def test_description_set(new_section, section):
    assert new_section.description is None
    new_section.description = "New section Description"
    assert new_section.description == "New section Description"

    assert section.description == DESCRIPTION
    section.description = "New section Description"
    assert section.description == "New section Description"


def test_description_set_exc(new_section):
    with pytest.raises(TypeError) as exc:
        new_section.description = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_display_order(new_section, section):
    assert new_section.display_order is None
    assert section.display_order == DISPLAY_ORDER


def test_name_get(new_section, section):
    assert new_section.name is None
    assert section.name == NAME


def test_name_set(new_section, section):
    assert new_section.name is None
    new_section.name = "New section Name"
    assert new_section.name == "New section Name"

    assert section.name == NAME
    section.name = "New section Name"
    assert section.name == "New section Name"


def test_name_set_exc(new_section):
    with pytest.raises(TypeError) as exc:
        new_section.name = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_parent_get(new_section, section):
    assert new_section.parent is None

    section.client.api.section_by_id.return_value = {'id': PARENT_ID}

    assert isinstance(section.parent, Section)
    assert section.parent.id == PARENT_ID
    section.client.api.section_by_id.assert_called_with(PARENT_ID)


def test_parent_set(new_section):
    assert new_section.parent is None

    new_section.parent = Section(None, {'id': PARENT_ID})

    assert new_section._content['parent_id'] == PARENT_ID


def test_parent_set_exc(new_section):
    assert new_section.parent is None

    with pytest.raises(TypeError) as exc:
        new_section.parent = 1234

    assert str(Section) in str(exc)
    assert str(int) in str(exc)


def test_project_get(new_section, section):
    assert new_section.project is None

    section.client.api.project_by_id.return_value = {'id': PROJECT_ID}

    assert isinstance(section.project, Project)
    assert section.project.id == PROJECT_ID
    section.client.api.project_by_id.assert_called_with(PROJECT_ID)


def test_project_set(new_section):
    assert new_section.project is None

    new_section.project = Project(None, {'id': PROJECT_ID})

    assert new_section._content['project_id'] == PROJECT_ID


def test_project_set_exc(new_section):
    assert new_section.project is None

    with pytest.raises(TypeError) as exc:
        new_section.project = 1234

    assert str(Project) in str(exc)
    assert str(int) in str(exc)


def test_suite_get(new_section, section):
    assert new_section.suite is None

    section.client.api.suite_by_id.return_value = {'id': SUITE_ID}

    assert isinstance(section.suite, Suite)
    assert section.suite.id == SUITE_ID
    section.client.api.suite_by_id.assert_called_with(SUITE_ID)


def test_suite_set(new_section):
    assert new_section.suite is None

    new_section.suite = Suite(None, {'id': SUITE_ID})

    assert new_section._content['suite_id'] == SUITE_ID


def test_suite_set_exc(new_section):
    assert new_section.suite is None

    with pytest.raises(TypeError) as exc:
        new_section.suite = 1234

    assert str(Suite) in str(exc)
    assert str(int) in str(exc)
