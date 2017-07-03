import pytest

try:
    import mock
except ImportError:
    from unittest import mock

import traw
from traw import models

USER = 'mock username'
PASS = 'mock password'
URL = 'mock url'

CF1 = {'name': 'case_field_1'}
CF2 = {'name': 'case_field_2'}
CF3 = {'name': 'case_field_3'}
PRIO1 = {'name': 'priority1'}
PRIO2 = {'name': 'priority2'}
PRIO3 = {'name': 'priority3'}
PROJ1 = {'name': 'project1'}
PROJ2 = {'name': 'project2'}
PROJ3 = {'name': 'project3'}
USER1 = {'name': 'user1'}
USER2 = {'name': 'user2'}
USER3 = {'name': 'user3'}


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


def test_case_fields(client):
    """ Verify the Client's ``case_fields`` method call """
    client._api.case_fields.return_value = [CF1, CF2, CF3]

    cf_gen = client.case_fields()
    cf1 = next(cf_gen)
    assert isinstance(cf1, models.CaseField)
    assert cf1.name == 'case_field_1'
    assert client._api.case_fields.call_args == mock.call()

    cf2 = next(cf_gen)
    assert isinstance(cf2, models.CaseField)
    assert cf2.name == 'case_field_2'
    assert client._api.case_fields.call_args == mock.call()

    cf3 = next(cf_gen)
    assert isinstance(cf3, models.CaseField)
    assert cf3.name == 'case_field_3'
    assert client._api.case_fields.call_args == mock.call()


def test_priorities(client):
    """ Verify the Client's ``priorities`` method call """
    client._api.priorities.return_value = [PRIO1, PRIO2, PRIO3]

    prio_gen = client.priorities()
    prio1 = next(prio_gen)
    assert isinstance(prio1, models.Priority)
    assert prio1.name == 'priority1'
    assert client._api.priorities.call_args == mock.call()

    prio2 = next(prio_gen)
    assert isinstance(prio2, models.Priority)
    assert prio2.name == 'priority2'
    assert client._api.priorities.call_args == mock.call()

    prio3 = next(prio_gen)
    assert isinstance(prio3, models.Priority)
    assert prio3.name == 'priority3'
    assert client._api.priorities.call_args == mock.call()


def test_project(client):
    """ Verify project method returns a new project instance if called without
        any parameters
    """
    proj = client.project()

    assert proj.announcement is None
    assert proj.completed_on is None
    assert proj.is_completed is False
    assert proj.show_announcement is False
    assert proj.suite_mode is None
    assert proj.url is None


def test_project_by_id(client):
    """ Verify project method returns a specific project instance if called with
        an int
    """
    PROJ_1234 = {"announcement": "mock announcement",
                 "completed_on": None,
                 "id": 1234,
                 "is_completed": False,
                 "name": "Project 1234",
                 "show_announcement": False,
                 "url": "http://<server>/index.php?/projects/overview/1234",
                 "suite_mode": 1}
    PROJ_ID = 1234

    client._api.project_by_id.return_value = PROJ_1234
    proj = client.project(PROJ_ID)

    assert isinstance(proj, models.Project)
    assert proj.id == PROJ_ID
    client._api.project_by_id.assert_called_once_with(PROJ_ID)


def test_projects_exception(client):
    """ Verify ``projects`` throws an exception if all args are True """
    with pytest.raises(TypeError) as exc:
        next(client.projects(active_only=True, completed_only=True))

    assert 'but not both' in str(exc)


def test_projects(client):
    """ Verify the Client's ``projects`` method call """
    client._api.projects.side_effect = [[PROJ1], [PROJ2], [PROJ3]]

    project1 = next(client.projects())
    assert isinstance(project1, models.Project)
    assert project1.name == 'project1'
    assert client._api.projects.call_args == mock.call(None)

    project2 = next(client.projects(active_only=True))
    assert isinstance(project2, models.Project)
    assert project2.name == 'project2'
    assert client._api.projects.call_args == mock.call(0)

    project3 = next(client.projects(completed_only=True))
    assert isinstance(project3, models.Project)
    assert project3.name == 'project3'
    assert client._api.projects.call_args == mock.call(1)


def test_user(client):
    """ Verify user method returns a new user instance if called without
        any parameters
    """
    user = client.user()

    assert user.email is None
    assert user.id is None
    assert user.is_active is None
    assert user.name is None


def test_user_by_email(client):
    """ Verify user method returns a specific user instance if called with
        an email address
    """
    USER_EMAIL = 'mock.user@mock.com'
    USER_DICT = {"email": USER_EMAIL}

    client._api.user_by_email.return_value = USER_DICT
    user = client.user(USER_EMAIL)

    assert isinstance(user, models.User)
    assert user.email == USER_EMAIL
    client._api.user_by_email.assert_called_once_with(USER_EMAIL)


def test_user_by_email_exc(client):
    """ Verify user method throws an exception if a non-email str is used """
    USER_EMAIL = 'not valid'
    USER_DICT = {"email": USER_EMAIL}

    client._api.user_by_email.return_value = USER_DICT
    with pytest.raises(ValueError) as exc:
        client.user(USER_EMAIL)

    assert 'must be a string that includes an "@"' in str(exc)
    assert not client._api.user_by_email.called


def test_user_by_id(client):
    """ Verify user method returns a specific user instance if called with
        an int
    """
    USER_ID = 1234
    USER_1234 = {"id": USER_ID}

    client._api.user_by_id.return_value = USER_1234
    user = client.user(USER_ID)

    assert isinstance(user, models.User)
    assert user.id == USER_ID
    client._api.user_by_id.assert_called_once_with(USER_ID)


def test_users(client):
    """ Verify the Client's ``users`` method call """
    client._api.users.return_value = [USER1, USER2, USER3]

    users_gen = client.users()
    user1 = next(users_gen)
    assert isinstance(user1, models.User)
    assert user1.name == 'user1'
    assert client._api.users.call_args == mock.call()

    user2 = next(users_gen)
    assert isinstance(user2, models.User)
    assert user2.name == 'user2'
    assert client._api.users.call_args == mock.call()

    user3 = next(users_gen)
    assert isinstance(user3, models.User)
    assert user3.name == 'user3'
    assert client._api.users.call_args == mock.call()
