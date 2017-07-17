from copy import deepcopy

import pytest

from traw.models import User

EMAIL = 'user.email@mock.com'
ID = 1234
NAME = 'mock name'


@pytest.fixture()
def user(client):
    content = {"email": EMAIL,
               "id": ID,
               "is_active": True,
               "name": NAME}
    return User(client, deepcopy(content))


def test_email(user):
    assert user.email == EMAIL


def test_id(user):
    assert user.id == ID


def test_is_active(user):
    assert user.is_active is True


def test_name(user):
    assert user.name == NAME
