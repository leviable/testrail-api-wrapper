from copy import deepcopy

import pytest

from traw.models import Priority

ID = 1234
IS_DEFAULT = True
NAME = '1 - mock priority'
PRIORITY = 1
SHORT_NAME = '1 - mock'


@pytest.fixture()
def priority(client):
    content = {"id": ID,
               "is_default": IS_DEFAULT,
               "name": NAME,
               'priority': PRIORITY,
               'short_name': SHORT_NAME}
    return Priority(client, deepcopy(content))


def test_id(priority):
    assert priority.id == ID


def test_is_default(priority):
    assert priority.is_default is True


def test_name(priority):
    assert priority.name == NAME


def test_priority(priority):
    assert priority.priority == PRIORITY


def test_short_name(priority):
    assert priority.short_name == SHORT_NAME
