import datetime
from copy import deepcopy

import pytest

from traw.models import Project

ANNOUNCEMENT = 'mock announcement'
COMPLETED_ON = 1469726522
ID = 123
NAME = 'mock name'
URL = 'mock url'


@pytest.fixture()
def empty_proj(client):
    return Project(client)


@pytest.fixture()
def in_progress_proj(client):
    content = {"announcement": ANNOUNCEMENT,
               "completed_on": None,
               "id": ID,
               "is_completed": False,
               "name": NAME,
               "show_announcement": True,
               "suite_mode": 1,
               "url": URL}
    return Project(client, deepcopy(content))


@pytest.fixture()
def complete_proj(client):
    content = {"announcement": None,
               "completed_on": COMPLETED_ON,
               "id": ID,
               "is_completed": True,
               "name": NAME,
               "show_announcement": False,
               "suite_mode": 2,
               "url": URL}
    return Project(client, content)


def test_announcement_get(empty_proj, in_progress_proj, complete_proj):
    assert empty_proj.announcement is None
    assert in_progress_proj.announcement == ANNOUNCEMENT
    assert complete_proj.announcement is None


def test_announcement_set(empty_proj, in_progress_proj, complete_proj):
    empty_proj.announcement = "New announcement 1"
    assert empty_proj.announcement == "New announcement 1"

    in_progress_proj.announcement = "New announcement 2"
    assert in_progress_proj.announcement == "New announcement 2"

    complete_proj.announcement = "New announcement 3"
    assert complete_proj.announcement == "New announcement 3"


def test_announcement_set_exc(empty_proj):
    with pytest.raises(TypeError) as exc:
        empty_proj.announcement = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_completed_on(empty_proj, in_progress_proj, complete_proj):
    assert empty_proj.completed_on is None
    assert in_progress_proj.completed_on is None
    assert isinstance(complete_proj.completed_on, datetime.datetime)


def test_id(empty_proj, in_progress_proj, complete_proj):
    assert empty_proj.id is None
    assert in_progress_proj.id is ID
    assert complete_proj.id is ID


def test_is_completed(empty_proj, in_progress_proj, complete_proj):
    assert empty_proj.is_completed is False
    assert in_progress_proj.is_completed is False
    assert complete_proj.is_completed is True


def test_is_completed_set(empty_proj, in_progress_proj, complete_proj):
    assert empty_proj.is_completed is False
    empty_proj.is_completed = False
    assert empty_proj.is_completed is False
    empty_proj.is_completed = True
    assert empty_proj.is_completed is True

    assert in_progress_proj.is_completed is False
    in_progress_proj.is_completed = True
    assert in_progress_proj.is_completed is True

    assert in_progress_proj.is_completed is True
    in_progress_proj.is_completed = False
    assert in_progress_proj.is_completed is False


def test_is_completed_set_exc(empty_proj):
    with pytest.raises(TypeError) as exc:
        empty_proj.is_completed = 1234

    assert str(bool) in str(exc)
    assert str(int) in str(exc)


def test_name_get(empty_proj, in_progress_proj, complete_proj):
    assert empty_proj.name is None
    assert in_progress_proj.name is NAME
    assert complete_proj.name is NAME


def test_name_set(empty_proj, in_progress_proj, complete_proj):
    empty_proj.name = NAME
    assert empty_proj.name == NAME

    in_progress_proj.name == NAME
    assert in_progress_proj.name is NAME

    complete_proj.name = NAME
    assert complete_proj.name is NAME


def test_name_set_exc(empty_proj):
    with pytest.raises(TypeError) as exc:
        empty_proj.name = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_show_announcement(empty_proj, in_progress_proj, complete_proj):
    assert empty_proj.show_announcement is False
    assert in_progress_proj.show_announcement is True
    assert complete_proj.show_announcement is False


def test_show_announcement_set(empty_proj, in_progress_proj, complete_proj):
    empty_proj.show_announcement = True
    assert empty_proj.show_announcement is True

    in_progress_proj.show_announcement = False
    assert in_progress_proj.show_announcement is False

    complete_proj.show_announcement = True
    assert complete_proj.show_announcement is True


def test_show_announcement_set_exc(empty_proj):
    with pytest.raises(TypeError) as exc:
        empty_proj.show_announcement = 1234

    assert str(bool) in str(exc)
    assert str(int) in str(exc)


def test_suite_mode_get(empty_proj, in_progress_proj, complete_proj):
    assert empty_proj.suite_mode is None
    assert in_progress_proj.suite_mode is 1
    assert complete_proj.suite_mode is 2


def test_suite_mode_set(empty_proj, in_progress_proj, complete_proj):
    empty_proj.suite_mode = 2
    assert empty_proj.suite_mode is 2

    in_progress_proj.suite_mode = 3
    assert in_progress_proj.suite_mode is 3

    complete_proj.suite_mode = 1
    assert complete_proj.suite_mode is 1


def test_suite_mode_typeerror_exc(empty_proj):
    with pytest.raises(TypeError) as exc:
        empty_proj.suite_mode = 'asdf'

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_suite_mode_valueerror_exc(empty_proj):
    with pytest.raises(ValueError) as exc:
        empty_proj.suite_mode = 4

    assert '1, 2, or 3' in str(exc)


def test_url(empty_proj, in_progress_proj, complete_proj):
    assert empty_proj.url is None
    assert in_progress_proj.url is URL
    assert complete_proj.url is URL
