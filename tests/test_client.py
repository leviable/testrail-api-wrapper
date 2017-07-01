import pytest

try:
    import mock
except ImportError:
    from unittest import mock

import traw
from traw.models import Project

USER = 'mock username'
PASS = 'mock password'
URL = 'mock url'
PROJ1 = {'name': 'project1'}
PROJ2 = {'name': 'project2'}
PROJ3 = {'name': 'project3'}


@pytest.fixture()
def client():
    with mock.patch('traw.client.API') as api_mock:
        api_mock.return_value = api_mock

        yield traw.Client(username=USER, password=PASS, url=URL)


def test___init__():
    client = traw.Client(username=USER, password=PASS, url=URL)
    assert hasattr(client, '_api')
    assert isinstance(client._api, traw.api.API)


def test_add_exception(client):
    """ Verify the Client raises an exception if add is called directly """
    with pytest.raises(TypeError):
        client.add()


def test_close_exception(client):
    """ Verify the Client raises an exception if close is called directly """
    with pytest.raises(TypeError):
        client.close()


def test_delete_exception(client):
    """ Verify the Client raises an exception if delete is called directly """
    with pytest.raises(TypeError):
        client.delete()


def test_update_exception(client):
    """ Verify the Client raises an exception if update is called directly """
    with pytest.raises(TypeError):
        client.update()


def test_projects_exception(client):
    """ Verify ``projects`` throws an exception if all args are True """
    with pytest.raises(TypeError) as exc:
        next(client.projects(active_only=True, completed_only=True))

    assert 'but not both' in str(exc)


def test_projects(client):
    """ Verify the Client's ``projects`` method call """
    client._api.projects.side_effect = [[PROJ1], [PROJ2], [PROJ3]]

    project1 = next(client.projects())
    assert isinstance(project1, Project)
    assert project1.name == 'project1'
    assert client._api.projects.call_args == mock.call(None)

    project2 = next(client.projects(active_only=True))
    assert isinstance(project2, Project)
    assert project2.name == 'project2'
    assert client._api.projects.call_args == mock.call(0)

    project3 = next(client.projects(completed_only=True))
    assert isinstance(project3, Project)
    assert project3.name == 'project3'
    assert client._api.projects.call_args == mock.call(1)
