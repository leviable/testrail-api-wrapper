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

CT1 = {'name': 'casetype1'}
CT2 = {'name': 'casetype2'}
CT3 = {'name': 'casetype3'}
MILE1 = {'name': 'milestone1'}
MILE2 = {'name': 'milestone2'}
MILE3 = {'name': 'milestone3'}
PRIO1 = {'name': 'priority1'}
PRIO2 = {'name': 'priority2'}
PRIO3 = {'name': 'priority3'}
PROJ1 = {'name': 'project1'}
PROJ2 = {'name': 'project2'}
PROJ3 = {'name': 'project3'}
STAT1 = {'name': 'status1'}
STAT2 = {'name': 'status2'}
STAT3 = {'name': 'status3'}
TEMP1 = {'name': 'template1'}
TEMP2 = {'name': 'template2'}
TEMP3 = {'name': 'template3'}
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


def test_case_types(client):
    """ Verify the Client's ``case_types`` method call """
    client._api.case_types.return_value = [CT1, CT2, CT3]

    ct_gen = client.case_types()
    ct1 = next(ct_gen)
    assert isinstance(ct1, models.CaseType)
    assert ct1.name == 'casetype1'

    ct2 = next(ct_gen)
    assert isinstance(ct2, models.CaseType)
    assert ct2.name == 'casetype2'

    ct3 = next(ct_gen)
    assert isinstance(ct3, models.CaseType)
    assert ct3.name == 'casetype3'

    assert client._api.case_types.call_args == mock.call()


def test_milestone(client):
    """ Verify calling ``client.milestone()`` with no args returns an empty Milestone """
    milestone = client.milestone()

    assert isinstance(milestone, models.Milestone)
    assert milestone._content == dict()


def test_milestone_by_id(client):
    """ Verify calling ``client.milestone(123)`` with an ID returns that milestone """
    client._api.milestone_by_id.return_value = {'id': 1234}
    milestone = client.milestone(1234)

    assert isinstance(milestone, models.Milestone)
    assert milestone.id == 1234
    assert client._api.milestone_by_id.called_once_with(1234)


def test_milestones_exception(client):
    """ Verify an exception is thrown if milestones is called with no parameters """
    with pytest.raises(NotImplementedError) as exc:
        client.milestones()

    assert 'models.Project or int' in str(exc)


def test_milestones_by_project_w_defaults(client):
    """ Verify milestones method returns milestones if called with
        a models.Project object
    """
    PROJECT_ID = 15
    PROJECT = models.Project(client, {'id': PROJECT_ID})
    client._api.milestones.return_value = [MILE1, MILE2, MILE3]

    mile_gen = client.milestones(PROJECT)

    mile1 = next(mile_gen)
    assert isinstance(mile1, models.Milestone)
    assert mile1.name == 'milestone1'

    mile2 = next(mile_gen)
    assert isinstance(mile2, models.Milestone)
    assert mile2.name == 'milestone2'

    mile3 = next(mile_gen)
    assert isinstance(mile3, models.Milestone)
    assert mile3.name == 'milestone3'

    assert client._api.milestones.call_args == mock.call(PROJECT.id, None, None)


def test_milestones_by_project_w_params(client):
    """ Verify milestones method returns milestones if called with
        a models.Project object and method parameters
    """
    PROJECT_ID = 15
    PROJECT = models.Project(client, {'id': PROJECT_ID})
    client._api.milestones.return_value = [MILE1, MILE2, MILE3]

    mile_gen = client.milestones(PROJECT, is_completed=False, is_started=True)

    mile1 = next(mile_gen)
    assert isinstance(mile1, models.Milestone)
    assert mile1.name == 'milestone1'

    mile2 = next(mile_gen)
    assert isinstance(mile2, models.Milestone)
    assert mile2.name == 'milestone2'

    mile3 = next(mile_gen)
    assert isinstance(mile3, models.Milestone)
    assert mile3.name == 'milestone3'

    assert client._api.milestones.call_args == mock.call(PROJECT.id, False, True)


def test_milestones_by_project_id_w_defaults(client):
    """ Verify milestones method returns milestones if called with
        an project ID (an int)
    """
    PROJECT_ID = 15
    client._api.milestones.return_value = [MILE1, MILE2, MILE3]

    mile_gen = client.milestones(PROJECT_ID)

    mile1 = next(mile_gen)
    assert isinstance(mile1, models.Milestone)
    assert mile1.name == 'milestone1'

    mile2 = next(mile_gen)
    assert isinstance(mile2, models.Milestone)
    assert mile2.name == 'milestone2'

    mile3 = next(mile_gen)
    assert isinstance(mile3, models.Milestone)
    assert mile3.name == 'milestone3'

    assert client._api.milestones.call_args == mock.call(PROJECT_ID, None, None)


def test_milestones_by_project_id_w_params(client):
    """ Verify milestones method returns milestones if called with
        an project ID (an int)
    """
    PROJECT_ID = 15
    client._api.milestones.return_value = [MILE1, MILE2, MILE3]

    mile_gen = client.milestones(PROJECT_ID, True, False)

    mile1 = next(mile_gen)
    assert isinstance(mile1, models.Milestone)
    assert mile1.name == 'milestone1'

    mile2 = next(mile_gen)
    assert isinstance(mile2, models.Milestone)
    assert mile2.name == 'milestone2'

    mile3 = next(mile_gen)
    assert isinstance(mile3, models.Milestone)
    assert mile3.name == 'milestone3'

    assert client._api.milestones.call_args == mock.call(PROJECT_ID, True, False)


def test_milestones_by_project_id_is_completed_exception(client):
    """ Verify milestones raises an exception if is_completed is the wrong type """
    with pytest.raises(TypeError) as exc:
        next(client.milestones(15, 1234, False))

    assert '1234' in str(exc)
    assert 'is_completed' in str(exc)


def test_milestones_by_project_id_is_started_exception(client):
    """ Verify milestones raises an exception if is_started is the wrong type """
    with pytest.raises(TypeError) as exc:
        next(client.milestones(15, False, 'asdf'))

    assert 'asdf' in str(exc)
    assert 'is_started' in str(exc)


def test_milestones_by_project_is_completed_exception(client):
    """ Verify milestones raises an exception if is_completed is the wrong type """
    with pytest.raises(TypeError) as exc:
        next(client.milestones(models.Project(client, {'id': 15}), 1234, False))

    assert '1234' in str(exc)
    assert 'is_completed' in str(exc)


def test_milestones_by_project_is_started_exception(client):
    """ Verify milestones raises an exception if is_started is the wrong type """
    with pytest.raises(TypeError) as exc:
        next(client.milestones(models.Project(client, {'id': 15}), False, 'asdf'))

    assert 'asdf' in str(exc)
    assert 'is_started' in str(exc)


def test_priorities(client):
    """ Verify the Client's ``priorities`` method call """
    client._api.priorities.return_value = [PRIO1, PRIO2, PRIO3]

    prio_gen = client.priorities()
    prio1 = next(prio_gen)
    assert isinstance(prio1, models.Priority)
    assert prio1.name == 'priority1'

    prio2 = next(prio_gen)
    assert isinstance(prio2, models.Priority)
    assert prio2.name == 'priority2'

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


def test_statuses(client):
    """ Verify the Client's ``statuses`` method call """
    client._api.statuses.return_value = [STAT1, STAT2, STAT3]

    stat_gen = client.statuses()
    stat1 = next(stat_gen)
    assert isinstance(stat1, models.Status)
    assert stat1.name == 'status1'

    stat2 = next(stat_gen)
    assert isinstance(stat2, models.Status)
    assert stat2.name == 'status2'

    stat3 = next(stat_gen)
    assert isinstance(stat3, models.Status)
    assert stat3.name == 'status3'

    assert client._api.statuses.call_args == mock.call()


def test_templates_exception(client):
    """ Verify an exception is thrown if templates is called with no parameters """
    with pytest.raises(NotImplementedError) as exc:
        client.templates()

    assert 'models.Project or int' in str(exc)


def test_templates_by_project(client):
    """ Verify templates method returns a templates if called with
        a models.Project object
    """
    PROJECT_ID = 15
    PROJECT = models.Project({'id': PROJECT_ID})
    client._api.templates.return_value = [TEMP1, TEMP2, TEMP3]

    temp_gen = client.templates(PROJECT)
    temp1 = next(temp_gen)
    assert isinstance(temp1, models.Template)
    assert temp1.name == 'template1'

    temp2 = next(temp_gen)
    assert isinstance(temp2, models.Template)
    assert temp2.name == 'template2'

    temp3 = next(temp_gen)
    assert isinstance(temp3, models.Template)
    assert temp3.name == 'template3'

    assert client._api.templates.call_args == mock.call(PROJECT.id)


def test_templates_by_project_id(client):
    """ Verify templates method returns a templates if called with
        an project ID (an int)
    """
    PROJECT_ID = 15
    client._api.templates.return_value = [TEMP1, TEMP2, TEMP3]

    temp_gen = client.templates(PROJECT_ID)
    temp1 = next(temp_gen)
    assert isinstance(temp1, models.Template)
    assert temp1.name == 'template1'

    temp2 = next(temp_gen)
    assert isinstance(temp2, models.Template)
    assert temp2.name == 'template2'

    temp3 = next(temp_gen)
    assert isinstance(temp3, models.Template)
    assert temp3.name == 'template3'

    assert client._api.templates.call_args == mock.call(PROJECT_ID)


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

    user2 = next(users_gen)
    assert isinstance(user2, models.User)
    assert user2.name == 'user2'

    user3 = next(users_gen)
    assert isinstance(user3, models.User)
    assert user3.name == 'user3'

    assert client._api.users.call_args == mock.call()
