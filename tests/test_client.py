import sys

import mock
import pytest

import traw
from traw import models
from traw.exceptions import TRAWClientError

USER = 'mock username'
PASS = 'mock password'
URL = 'mock url'

CT1 = {'name': 'casetype1', 'id': 331}
CT2 = {'name': 'casetype2', 'id': 332}
CT3 = {'name': 'casetype3', 'id': 333}
MILE1 = {'name': 'milestone1'}
MILE2 = {'name': 'milestone2'}
MILE3 = {'name': 'milestone3'}
PRIO1 = {'name': 'priority1', 'id': 111}
PRIO2 = {'name': 'priority2', 'id': 112}
PRIO3 = {'name': 'priority3', 'id': 113}
PROJ1 = {'name': 'project1'}
PROJ2 = {'name': 'project2'}
PROJ3 = {'name': 'project3'}
STAT1 = {'name': 'status1', 'id': 221, 'label': 'Passed'}
STAT2 = {'name': 'status2', 'id': 222, 'label': 'Failed'}
STAT3 = {'name': 'status3', 'id': 223, 'label': 'Blocked'}
TEMP1 = {'name': 'template1'}
TEMP2 = {'name': 'template2'}
TEMP3 = {'name': 'template3'}
TEST1 = {'name': 'test1', 'id': 441}
TEST2 = {'name': 'test2', 'id': 442}
TEST3 = {'name': 'test3', 'id': 443}
USER1 = {'name': 'user1'}
USER2 = {'name': 'user2'}
USER3 = {'name': 'user3'}


def test___init__():
    client = traw.Client(username=USER, password=PASS, url=URL)
    assert hasattr(client, 'api')
    assert isinstance(client.api, traw.api.API)


def test_add_exception_no_obj(client):
    """ Verify the Client raises an exception if add is called directly """
    with pytest.raises(TypeError) as exc:
        client.add()

    if sys.version_info.major == 2:
        assert "takes exactly 2 arguments (1 given)" in str(exc)
    else:
        assert "required positional argument: 'obj'" in str(exc)


def test_add_exception_w_obj(client):
    """ Verify the Client raises an exception if add is called with unsupported type """
    with pytest.raises(TypeError) as exc:
        client.add(1)

    assert "support adding objects of type" in str(exc)


def test_add_milestone(client):
    MILESTONE_ID = 111
    PROJECT_ID = 15

    milestone_config = {traw.const.NAME: 'mock name',
                        traw.const.DESCRIPTION: 'mock description',
                        traw.const.DUE_ON: 123456,
                        traw.const.START_ON: 12345,
                        traw.const.PROJECT_ID: PROJECT_ID}
    milestone = models.Milestone(client, dict(extra='extra', **milestone_config))

    client.api.milestone_add.return_value = dict(id=MILESTONE_ID, **milestone_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.add(milestone)

    assert isinstance(response, models.Milestone)
    assert response.id == MILESTONE_ID
    assert client.api.milestone_add.called
    assert 'extra' not in str(client.api.milestone.call_args)


def test_add_project(client):
    PROJECT_ID = 15

    project_config = {traw.const.NAME: 'mock name',
                      traw.const.ANNOUNCEMENT: 'mock announcement',
                      traw.const.SHOW_ANNOUNCEMENT: False,
                      traw.const.SUITE_MODE: 1}
    project = models.Project(client, dict(extra='extra', **project_config))

    client.api.project_add.return_value = dict(id=PROJECT_ID, **project_config)

    response = client.add(project)

    assert isinstance(response, models.Project)
    assert response.id == PROJECT_ID
    assert client.api.project_add.called
    assert 'extra' not in str(client.api.project.call_args)


def test_add_sub_milestone(client):
    SUB_MILESTONE_ID = 111
    PARENT_ID = 222
    PROJECT_ID = 15

    milestone_config = {traw.const.NAME: 'mock name',
                        traw.const.DESCRIPTION: 'mock description',
                        traw.const.DUE_ON: 123456,
                        traw.const.START_ON: 12345,
                        traw.const.PROJECT_ID: PROJECT_ID}
    milestone = models.Milestone(client, dict(extra='extra', **milestone_config))
    sub_milestone = milestone.add_parent(models.Milestone(client, {'id': PARENT_ID}))

    client.api.milestone_add.return_value = dict(id=SUB_MILESTONE_ID,
                                                 parent_id=PARENT_ID,
                                                 **milestone_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.add(sub_milestone)

    assert isinstance(response, models.SubMilestone)
    assert response.id == SUB_MILESTONE_ID
    assert client.api.milestone_add.called
    assert 'extra' not in str(client.api.milestone.call_args)


def test_close_exception_no_obj(client):
    """ Verify the Client raises an exception if close is called directly """
    with pytest.raises(TypeError) as exc:
        client.close()

    if sys.version_info.major == 2:
        assert "takes exactly 2 arguments (1 given)" in str(exc)
    else:
        assert "required positional argument: 'obj'" in str(exc)


def test_close_exception_w_obj(client):
    """ Verify the Client raises an exception if close is called with unsupporte type """
    with pytest.raises(TypeError) as exc:
        client.close(1)

    assert "support closing objects of type" in str(exc)


def test_delete_exception_no_obj(client):
    """ Verify the Client raises an exception if delete is called directly """
    with pytest.raises(TypeError) as exc:
        client.delete()

    if sys.version_info.major == 2:
        assert "takes exactly 2 arguments (1 given)" in str(exc)
    else:
        assert "required positional argument: 'obj'" in str(exc)


def test_delete_exception_w_obj(client):
    """ Verify the Client raises an exception if delete is called with unsupporte type """
    with pytest.raises(TypeError) as exc:
        client.delete(1)

    assert "support deleting objects of type" in str(exc)


def test_delete_milestone(client):
    MILESTONE_ID = 111
    PROJECT_ID = 15

    milestone_config = {traw.const.NAME: 'mock name',
                        traw.const.DESCRIPTION: 'mock description',
                        traw.const.DUE_ON: 123456,
                        traw.const.START_ON: 12345,
                        traw.const.PROJECT_ID: PROJECT_ID}
    milestone = models.Milestone(client, dict(id=MILESTONE_ID, **milestone_config))

    client.api.milestone_delete.return_value = dict()

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.delete(milestone)

    assert response is None
    client.api.milestone_delete.assert_called_once_with(MILESTONE_ID)


def test_delete_project(client):
    PROJECT_ID = 15

    project_config = {traw.const.NAME: 'mock name',
                      traw.const.ANNOUNCEMENT: 'mock announcement',
                      traw.const.SHOW_ANNOUNCEMENT: False,
                      traw.const.SUITE_MODE: 1}
    project = models.Project(client, dict(id=PROJECT_ID, **project_config))

    client.api.project_delete.return_value = dict()

    response = client.delete(project)

    assert response is None
    client.api.project_delete.assert_called_once_with(PROJECT_ID)


def test_update_exception_no_obj(client):
    """ Verify the Client raises an exception if update is called directly """
    with pytest.raises(TypeError) as exc:
        client.update()

    if sys.version_info.major == 2:
        assert "takes exactly 2 arguments (1 given)" in str(exc)
    else:
        assert "required positional argument: 'obj'" in str(exc)


def test_update_exception_w_obj(client):
    """ Verify the Client raises an exception if update is called with unsupporte type """
    with pytest.raises(TypeError) as exc:
        client.update(1)

    assert "support updating objects of type" in str(exc)


def test_update_milestone(client):
    MILESTONE_ID = 111
    PROJECT_ID = 15

    milestone_config = {traw.const.NAME: 'mock name',
                        traw.const.DESCRIPTION: 'mock description',
                        traw.const.DUE_ON: 123456,
                        traw.const.START_ON: 12345,
                        traw.const.PROJECT_ID: PROJECT_ID}
    milestone = models.Milestone(client, dict(extra='extra', **milestone_config))

    client.api.milestone_update.return_value = dict(id=MILESTONE_ID, **milestone_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.update(milestone)

    assert isinstance(response, models.Milestone)
    assert response.id == MILESTONE_ID
    assert client.api.milestone_update.called
    assert 'extra' not in str(client.api.milestone.call_args)


def test_update_project(client):
    PROJECT_ID = 15

    project_config = {traw.const.NAME: 'mock name',
                      traw.const.ANNOUNCEMENT: 'mock announcement',
                      traw.const.SHOW_ANNOUNCEMENT: False,
                      traw.const.SUITE_MODE: 1,
                      traw.const.ID: PROJECT_ID}
    project = models.Project(client, dict(extra='extra', **project_config))

    client.api.project_update.return_value = project_config

    response = client.update(project)

    assert isinstance(response, models.Project)
    assert response.id == PROJECT_ID
    assert client.api.project_update.called
    assert 'extra' not in str(client.api.project.call_args)


def test_update_sub_milestone(client):
    SUB_MILESTONE_ID = 111
    PARENT_ID = 222
    PROJECT_ID = 15

    milestone_config = {traw.const.NAME: 'mock name',
                        traw.const.DESCRIPTION: 'mock description',
                        traw.const.DUE_ON: 123456,
                        traw.const.START_ON: 12345,
                        traw.const.PROJECT_ID: PROJECT_ID}
    milestone = models.Milestone(client, dict(extra='extra', **milestone_config))
    sub_milestone = milestone.add_parent(models.Milestone(client, {'id': PARENT_ID}))

    client.api.milestone_update.return_value = dict(id=SUB_MILESTONE_ID,
                                                    parent_id=PARENT_ID,
                                                    **milestone_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.update(sub_milestone)

    assert isinstance(response, models.SubMilestone)
    assert response.id == SUB_MILESTONE_ID
    assert client.api.milestone_update.called
    assert 'extra' not in str(client.api.milestone.call_args)


def test_case(client):
    """ Verify case method returns a new models.Case instance if called without
        any parameters
    """
    case = client.case()

    assert isinstance(case, models.Case)
    # TODO: Complete when Case is more than a stub
    # assert proj.announcement is None
    # assert proj.completed_on is None
    # assert proj.is_completed is False
    # assert proj.show_announcement is False
    # assert proj.suite_mode is None
    # assert proj.url is None


def test_case_by_id(client):
    """ Verify calling ``client.case(123)`` with an ID returns that case """
    client.api.case_by_id.return_value = {'id': 1234}
    case = client.case(1234)

    assert isinstance(case, models.Case)
    assert case.id == 1234
    client.api.case_by_id.assert_called_once_with(1234)


def test_case_type_exc(client):
    """ Verify the Client's ``case_type`` method throws an exception if called """
    with pytest.raises(NotImplementedError) as exc:
        client.case_type()

    assert 'You must pass in int object' in str(exc)
    assert not client.api.case_types.called


def test_case_type_by_int(client):
    """ Verify the Client's ``case_type`` method call with int"""
    client.api.case_types.return_value = [CT1, CT2, CT3]

    case_type = client.case_type(332)

    assert isinstance(case_type, models.CaseType)
    assert case_type.id == 332
    assert client.api.case_types.called


def test_case_type_by_int_exc(client):
    """ Verify the Client's ``case_type`` method throws an exception if unmatched id """
    client.api.case_types.return_value = [CT1, CT2, CT3]

    with pytest.raises(TRAWClientError) as exc:
        client.case_type(334)

    assert 'id of 334' in str(exc)
    assert client.api.case_types.called


def test_case_types(client):
    """ Verify the Client's ``case_types`` method call """
    client.api.case_types.return_value = [CT1, CT2, CT3]

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

    assert client.api.case_types.call_args == mock.call()


def test_milestone(client):
    """ Verify calling ``client.milestone()`` with no args returns an empty Milestone """
    milestone = client.milestone()

    assert isinstance(milestone, models.Milestone)
    assert milestone._content == dict()


def test_milestone_by_id(client):
    """ Verify calling ``client.milestone(123)`` with an ID returns that milestone """
    client.api.milestone_by_id.return_value = {'id': 1234}
    milestone = client.milestone(1234)

    assert isinstance(milestone, models.Milestone)
    assert milestone.id == 1234
    client.api.milestone_by_id.assert_called_once_with(1234)


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
    client.api.milestones.return_value = [MILE1, MILE2, MILE3]

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

    assert client.api.milestones.call_args == mock.call(PROJECT.id, None, None)


def test_milestones_by_project_w_params(client):
    """ Verify milestones method returns milestones if called with
        a models.Project object and method parameters
    """
    PROJECT_ID = 15
    PROJECT = models.Project(client, {'id': PROJECT_ID})
    client.api.milestones.return_value = [MILE1, MILE2, MILE3]

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

    assert client.api.milestones.call_args == mock.call(PROJECT.id, False, True)


def test_milestones_by_project_id_w_defaults(client):
    """ Verify milestones method returns milestones if called with
        an project ID (an int)
    """
    PROJECT_ID = 15
    client.api.milestones.return_value = [MILE1, MILE2, MILE3]

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

    assert client.api.milestones.call_args == mock.call(PROJECT_ID, None, None)


def test_milestones_by_project_id_w_params(client):
    """ Verify milestones method returns milestones if called with
        an project ID (an int)
    """
    PROJECT_ID = 15
    client.api.milestones.return_value = [MILE1, MILE2, MILE3]

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

    assert client.api.milestones.call_args == mock.call(PROJECT_ID, True, False)


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


def test_priority_exc(client):
    """ Verify the Client's ``priority`` method throws an exception if called """
    with pytest.raises(NotImplementedError) as exc:
        client.priority()

    assert 'You must pass in int object' in str(exc)
    assert not client.api.priorities.called


def test_priority_by_int(client):
    """ Verify the Client's ``priority`` method call with int"""
    client.api.priorities.return_value = [PRIO1, PRIO2, PRIO3]

    priority = client.priority(112)

    assert isinstance(priority, models.Priority)
    assert priority.id == 112
    assert client.api.priorities.called


def test_priority_by_int_exc(client):
    """ Verify the Client's ``priority`` method throws an exception if unmatched id """
    client.api.priorities.return_value = [PRIO1, PRIO2, PRIO3]

    with pytest.raises(TRAWClientError) as exc:
        client.priority(114)

    assert 'id of 114' in str(exc)
    assert client.api.priorities.called


def test_priorities(client):
    """ Verify the Client's ``priorities`` method call """
    client.api.priorities.return_value = (p for p in [PRIO1, PRIO2, PRIO3])

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

    assert client.api.priorities.call_args == mock.call()


def test_project(client):
    """ Verify project method returns a new project instance if called without
        any parameters
    """
    proj = client.project()

    assert isinstance(proj, models.Project)
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

    client.api.project_by_id.return_value = PROJ_1234
    proj = client.project(PROJ_ID)

    assert isinstance(proj, models.Project)
    assert proj.id == PROJ_ID
    client.api.project_by_id.assert_called_once_with(PROJ_ID)


def test_projects_exception(client):
    """ Verify ``projects`` throws an exception if all args are True """
    with pytest.raises(TypeError) as exc:
        next(client.projects(active_only=True, completed_only=True))

    assert 'but not both' in str(exc)


def test_projects(client):
    """ Verify the Client's ``projects`` method call """
    client.api.projects.side_effect = [[PROJ1], [PROJ2], [PROJ3]]

    project1 = next(client.projects())
    assert isinstance(project1, models.Project)
    assert project1.name == 'project1'
    assert client.api.projects.call_args == mock.call(None)

    project2 = next(client.projects(active_only=True))
    assert isinstance(project2, models.Project)
    assert project2.name == 'project2'
    assert client.api.projects.call_args == mock.call(0)

    project3 = next(client.projects(completed_only=True))
    assert isinstance(project3, models.Project)
    assert project3.name == 'project3'
    assert client.api.projects.call_args == mock.call(1)


def test_run(client):
    """ Verify run method returns a new models.Run instance if called without
        any parameters
    """
    run = client.run()

    assert isinstance(run, models.Run)
    # TODO: Complete when Run is more than a stub
    # assert proj.announcement is None
    # assert proj.completed_on is None
    # assert proj.is_completed is False
    # assert proj.show_announcement is False
    # assert proj.suite_mode is None
    # assert proj.url is None


def test_run_by_id(client):
    """ Verify calling ``client.run(123)`` with an ID returns that run """
    client.api.run_by_id.return_value = {'id': 1234}
    run = client.run(1234)

    assert isinstance(run, models.Run)
    assert run.id == 1234
    client.api.run_by_id.assert_called_once_with(1234)


def test_status_exc(client):
    """ Verify the Client's ``status`` method throws an exception if called """
    with pytest.raises(NotImplementedError) as exc:
        client.status()

    assert 'You must pass in int object' in str(exc)
    assert not client.api.statuses.called


def test_status_by_int(client):
    """ Verify the Client's ``status`` method call with int"""
    client.api.statuses.return_value = [STAT1, STAT2, STAT3]

    status = client.status(222)

    assert isinstance(status, models.Status)
    assert status.id == 222
    assert client.api.statuses.called


def test_status_by_int_exc(client):
    """ Verify the Client's ``status`` method throws an exception if unmatched id """
    client.api.statuses.return_value = [STAT1, STAT2, STAT3]

    with pytest.raises(TRAWClientError) as exc:
        client.status(224)

    assert 'id of 224' in str(exc)
    assert client.api.statuses.called


def test_status_by_label_not_strict(client):
    """ Verify the Client's ``status`` method call with a label """
    client.api.statuses.return_value = [STAT1, STAT2, STAT3]

    status = client.status('failed')

    assert isinstance(status, models.Status)
    assert status.id == STAT2['id']
    assert status.label != 'failed'
    assert status.label.lower() == 'failed'
    assert client.api.statuses.called


def test_status_by_label_exc(client):
    """ Verify the Client's ``status`` method throws an exception if unmatched label """
    client.api.statuses.return_value = [STAT1, STAT2, STAT3]

    with pytest.raises(TRAWClientError) as exc:
        client.status('bad status')

    assert 'label of bad status' in str(exc)
    assert client.api.statuses.called


def test_status_by_label_strict(client):
    """ Verify the Client's ``status`` method call with a label """
    client.api.statuses.return_value = [STAT1, STAT2, STAT3]

    status = client.status('Failed', strict=True)

    assert isinstance(status, models.Status)
    assert status.id == STAT2['id']
    assert status.label == 'Failed'
    assert client.api.statuses.called


def test_statuses(client):
    """ Verify the Client's ``statuses`` method call """
    client.api.statuses.return_value = [STAT1, STAT2, STAT3]

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

    assert client.api.statuses.call_args == mock.call()


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
    PROJECT = models.Project(client, {'id': PROJECT_ID})
    client.api.templates.return_value = [TEMP1, TEMP2, TEMP3]

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

    assert client.api.templates.call_args == mock.call(PROJECT.id)


def test_templates_by_project_id(client):
    """ Verify templates method returns a templates if called with
        an project ID (an int)
    """
    PROJECT_ID = 15
    client.api.templates.return_value = [TEMP1, TEMP2, TEMP3]

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

    assert client.api.templates.call_args == mock.call(PROJECT_ID)


def test_test_exc(client):
    """ Verify the Client's ``test`` method throws an exception if called """
    with pytest.raises(NotImplementedError) as exc:
        client.test()

    assert 'You must pass in int object' in str(exc)
    assert not client.api.test.called


def test_test_by_id(client):
    """ Verify calling ``client.test(123)`` with an ID returns that test """
    client.api.test_by_id.return_value = {'id': 1234}
    test = client.test(1234)

    assert isinstance(test, models.Test)
    assert test.id == 1234
    client.api.test_by_id.assert_called_once_with(1234)


def test_tests_exc(client):
    """ Verify the Client's ``tests`` method throws an exception if called """
    with pytest.raises(NotImplementedError) as exc:
        client.tests()

    assert 'You must pass in models.Run or int object' in str(exc)
    assert not client.api.tests_by_run_id.called


def test_tests_by_run_id(client):
    """ Verify calling ``client.tests(123)`` with an ID returns test generator """
    client.api.tests_by_run_id.return_value = [TEST1, TEST2, TEST3]
    tests = client.tests(1234)

    test1 = next(tests)
    assert isinstance(test1, models.Test)
    assert test1.id == 441

    test2 = next(tests)
    assert isinstance(test2, models.Test)
    assert test2.id == 442

    test3 = next(tests)
    assert isinstance(test3, models.Test)
    assert test3.id == 443

    client.api.tests_by_run_id.assert_called_once_with(1234, None)


def test_tests_by_run_id_with_status(client):
    """ Verify calling ``client.tests(123)`` with an ID returns test generator """
    client.api.tests_by_run_id.return_value = [TEST1, ]
    status = models.Status(client, {'id': 234})

    tests = client.tests(1234, with_status=status)

    test1 = next(tests)
    assert isinstance(test1, models.Test)
    assert test1.id == 441

    client.api.tests_by_run_id.assert_called_once_with(1234, '234')


def test_tests_by_run_id_with_2_status(client):
    """ Verify calling ``client.tests(123)`` with an ID returns test generator """
    client.api.tests_by_run_id.return_value = [TEST1, ]
    status1 = models.Status(client, {'id': 234})
    status2 = models.Status(client, {'id': 345})

    tests = client.tests(1234, with_status=(status1, status2))

    test1 = next(tests)
    assert isinstance(test1, models.Test)
    assert test1.id == 441

    client.api.tests_by_run_id.assert_called_once_with(1234, '234,345')


def test_tests_by_run_id_exc_1(client):
    """ Verify calling ``client.tests(123, status)`` throws an exception """
    with pytest.raises(TypeError) as exc:
        next(client.tests(1234, with_status=111))

    assert "None, models.Status" in str(exc)
    assert "iterable of models.Status objects" in str(exc)
    assert str(int) in str(exc)
    assert not client.api.tests_by_run_id.called


def test_tests_by_run_id_exc_2(client):
    """ Verify calling ``client.tests(123, status)`` throws an exception """
    status1 = models.Status(client, {'id': 234})
    status2 = models.Status(client, {'id': 345})

    with pytest.raises(TypeError) as exc:
        next(client.tests(1234, with_status=(status1, 111, status2)))

    assert "None, models.Status" in str(exc)
    assert "iterable of models.Status objects" in str(exc)
    assert str(int) in str(exc)
    assert not client.api.tests_by_run_id.called


def test_tests_by_run(client):
    """ Verify calling ``client.tests(Run)`` with an ID returns test generator """
    client.api.tests_by_run_id.return_value = [TEST1, TEST2, TEST3]
    tests = client.tests(models.Run(client, {'id': 1234}))

    test1 = next(tests)
    assert isinstance(test1, models.Test)
    assert test1.id == 441

    test2 = next(tests)
    assert isinstance(test2, models.Test)
    assert test2.id == 442

    test3 = next(tests)
    assert isinstance(test3, models.Test)
    assert test3.id == 443

    client.api.tests_by_run_id.assert_called_once_with(1234, None)


def test_tests_by_run_with_status(client):
    """ Verify calling ``client.tests(123)`` with an ID returns test generator """
    client.api.tests_by_run_id.return_value = [TEST1, ]
    status = models.Status(client, {'id': 234})

    tests = client.tests(models.Run(client, {'id': 1234}), with_status=status)

    test1 = next(tests)
    assert isinstance(test1, models.Test)
    assert test1.id == 441

    client.api.tests_by_run_id.assert_called_once_with(1234, '234')


def test_tests_by_run_with_2_status(client):
    """ Verify calling ``client.tests(123)`` with an ID returns test generator """
    client.api.tests_by_run_id.return_value = [TEST1, ]
    status1 = models.Status(client, {'id': 234})
    status2 = models.Status(client, {'id': 345})

    tests = client.tests(models.Run(client, {'id': 1234}), with_status=(status1, status2))

    test1 = next(tests)
    assert isinstance(test1, models.Test)
    assert test1.id == 441

    client.api.tests_by_run_id.assert_called_once_with(1234, '234,345')


def test_tests_by_run_exc_1(client):
    """ Verify calling ``client.tests(123, status)`` throws an exception """
    with pytest.raises(TypeError) as exc:
        next(client.tests(models.Run(client, {'id': 1234}), with_status=111))

    assert "None, models.Status" in str(exc)
    assert "iterable of models.Status objects" in str(exc)
    assert str(int) in str(exc)
    assert not client.api.tests_by_run_id.called


def test_tests_by_run_exc_2(client):
    """ Verify calling ``client.tests(123, status)`` throws an exception """
    status1 = models.Status(client, {'id': 234})
    status2 = models.Status(client, {'id': 345})
    run = models.Run(client, {'id': 1234})

    with pytest.raises(TypeError) as exc:
        next(client.tests(run, with_status=(status1, 111, status2)))

    assert "None, models.Status" in str(exc)
    assert "iterable of models.Status objects" in str(exc)
    assert str(int) in str(exc)
    assert not client.api.tests_by_run_id.called


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

    client.api.user_by_email.return_value = USER_DICT
    user = client.user(USER_EMAIL)

    assert isinstance(user, models.User)
    assert user.email == USER_EMAIL
    client.api.user_by_email.assert_called_once_with(USER_EMAIL)


def test_user_by_email_exc(client):
    """ Verify user method throws an exception if a non-email str is used """
    USER_EMAIL = 'not valid'
    USER_DICT = {"email": USER_EMAIL}

    client.api.user_by_email.return_value = USER_DICT
    with pytest.raises(ValueError) as exc:
        client.user(USER_EMAIL)

    assert 'must be a string that includes an "@"' in str(exc)
    assert not client.api.user_by_email.called


def test_user_by_id(client):
    """ Verify user method returns a specific user instance if called with
        an int
    """
    USER_ID = 1234
    USER_1234 = {"id": USER_ID}

    client.api.user_by_id.return_value = USER_1234
    user = client.user(USER_ID)

    assert isinstance(user, models.User)
    assert user.id == USER_ID
    client.api.user_by_id.assert_called_once_with(USER_ID)


def test_users(client):
    """ Verify the Client's ``users`` method call """
    client.api.users.return_value = [USER1, USER2, USER3]

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

    assert client.api.users.call_args == mock.call()
