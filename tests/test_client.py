import sys

import mock
import pytest

import traw
from traw import models
from traw.exceptions import TRAWClientError, UnknownCustomStatusError

USER = 'mock username'
PASS = 'mock password'
URL = 'mock url'

CONF1 = {'group_id': 1, 'id': 1, 'name': 'config 1 name'}
CONF2 = {'group_id': 1, 'id': 2, 'name': 'config 2 name'}
CONF3 = {'group_id': 2, 'id': 3, 'name': 'config 3 name'}
CONF4 = {'group_id': 2, 'id': 4, 'name': 'config 4 name'}
CONF5 = {'group_id': 3, 'id': 5, 'name': 'config 5 name'}
CONF6 = {'group_id': 3, 'id': 6, 'name': 'config 6 name'}
CG1 = {'name': 'configgroup1', 'id': 661, 'project_id': 15,
       'configs': [CONF1, CONF2]}
CG2 = {'name': 'configgroup2', 'id': 662, 'project_id': 15,
       'configs': [CONF3, CONF4]}
CG3 = {'name': 'configgroup3', 'id': 663, 'project_id': 15,
       'configs': [CONF5, CONF6]}
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
STAT3 = {'name': 'status3', 'id': 223, 'label': 'failed'}
STAT4 = {'name': 'status4', 'id': 8, 'label': 'custom-failed'}
SUIT1 = {'name': 'suite1', 'id': 551}
SUIT2 = {'name': 'suite2', 'id': 552}
SUIT3 = {'name': 'suite3', 'id': 553}
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


def test_add_config(client):
    CONFIG_ID = 15
    CONFIG_GROUP_ID = 15

    config_config = {traw.const.NAME: 'mock name',
                     'group_id': CONFIG_GROUP_ID}

    config = models.Config(client, dict(extra='extra', **config_config))

    client.api.config_add.return_value = dict(id=CONFIG_ID, **config_config)

    response = client.add(config)

    assert isinstance(response, models.Config)
    assert response.id == CONFIG_ID
    assert client.api.config_add.called
    assert 'mock name' in str(client.api.config_add.call_args)
    assert 'extra' not in str(client.api.config_add.call_args)


def test_add_config_group(client):
    CONFIG_GROUP_ID = 15
    PROJECT_ID = 15

    config_group_config = {traw.const.NAME: 'mock name',
                           'project_id': PROJECT_ID}

    con_grp = models.ConfigGroup(client, dict(extra='extra', **config_group_config))

    client.api.config_group_add.return_value = dict(id=CONFIG_GROUP_ID, **config_group_config)

    response = client.add(con_grp)

    assert isinstance(response, models.ConfigGroup)
    assert response.id == CONFIG_GROUP_ID
    assert client.api.config_group_add.called
    assert 'mock name' in str(client.api.config_group_add.call_args)
    assert 'extra' not in str(client.api.config_group_add.call_args)


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
    assert 'mock name' in str(client.api.milestone_add.call_args)
    assert 'extra' not in str(client.api.milestone_add.call_args)


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
    assert 'mock name' in str(client.api.project_add.call_args)
    assert 'extra' not in str(client.api.project_add.call_args)


def test_add_run_no_case_ids(client):
    RUN_ID = 111
    PROJECT_ID = 15

    run_config = {traw.const.NAME: 'mock name',
                  traw.const.DESCRIPTION: 'mock description',
                  traw.const.MILESTONE_ID: '22',
                  traw.const.ASSIGNEDTO_ID: '33',
                  traw.const.INCLUDE_ALL: True,
                  traw.const.CASE_IDS: list(),
                  traw.const.PROJECT_ID: PROJECT_ID}
    run = models.Run(client, dict(extra='extra', **run_config))

    client.api.run_add.return_value = dict(id=RUN_ID, **run_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.add(run)

    assert isinstance(response, models.Run)
    assert response.id == RUN_ID
    assert client.api.run_add.called
    assert 'mock name' in str(client.api.run_add.call_args)
    assert 'extra' not in str(client.api.run_add.call_args)


def test_add_run_with_case_ids(client):
    RUN_ID = 111
    PROJECT_ID = 15

    run_config = {traw.const.NAME: 'mock name',
                  traw.const.DESCRIPTION: 'mock description',
                  traw.const.MILESTONE_ID: '22',
                  traw.const.ASSIGNEDTO_ID: '33',
                  traw.const.INCLUDE_ALL: True,
                  traw.const.CASE_IDS: [1, 2, 3, 4],
                  traw.const.PROJECT_ID: PROJECT_ID}
    run = models.Run(client, dict(extra='extra', **run_config))

    client.api.run_add.return_value = dict(id=RUN_ID, **run_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.add(run)

    assert isinstance(response, models.Run)
    assert response.id == RUN_ID
    assert client.api.run_add.called
    assert 'mock name' in str(client.api.run_add.call_args)
    assert '1,2,3,4' in str(client.api.run_add.call_args)
    assert 'extra' not in str(client.api.run_add.call_args)


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
    assert 'mock name' in str(client.api.milestone_add.call_args)
    assert 'extra' not in str(client.api.milestone_add.call_args)


def test_add_suite(client):
    SUITE_ID = 111
    PROJECT_ID = 15

    suite_config = {traw.const.NAME: 'mock name',
                    traw.const.DESCRIPTION: 'mock description',
                    traw.const.PROJECT_ID: PROJECT_ID}
    suite = models.Suite(client, dict(extra='extra', **suite_config))

    client.api.suite_add.return_value = dict(id=SUITE_ID, **suite_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.add(suite)

    assert isinstance(response, models.Suite)
    assert response.id == SUITE_ID
    assert client.api.suite_add.called
    assert 'mock name' in str(client.api.suite_add.call_args)
    assert 'extra' not in str(client.api.suite_add.call_args)


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


def test_close_run(client):
    RUN_ID = 111
    PROJECT_ID = 15

    run_config = {traw.const.NAME: 'mock name',
                  traw.const.DESCRIPTION: 'mock description',
                  traw.const.MILESTONE_ID: '22',
                  traw.const.ASSIGNEDTO_ID: '33',
                  traw.const.INCLUDE_ALL: True,
                  traw.const.CASE_IDS: list(),
                  traw.const.PROJECT_ID: PROJECT_ID}
    run = models.Run(client, dict(extra='extra', **run_config))

    client.api.run_close.return_value = dict(id=RUN_ID, **run_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.close(run)

    assert isinstance(response, models.Run)
    assert response.id == RUN_ID
    assert client.api.run_close.called
    assert 'mock name' not in str(client.api.run_close.call_args)
    assert 'extra' not in str(client.api.run_close.call_args)


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


def test_delete_config(client):
    CONFIG_GROUP_ID = 456
    CONFIG_ID = 123
    PROJECT_ID = 15

    config_config = {traw.const.NAME: 'mock name',
                     traw.const.PROJECT_ID: PROJECT_ID,
                     'group_id': CONFIG_GROUP_ID}
    config = models.Config(client, dict(id=CONFIG_ID, **config_config))

    client.api.project_delete.return_value = dict()

    response = client.delete(config)

    assert response is None
    client.api.config_delete.assert_called_once_with(CONFIG_ID)


def test_delete_config_group(client):
    CONFIG_GROUP_ID = 456
    PROJECT_ID = 15

    config_group_config = {traw.const.NAME: 'mock name',
                           traw.const.PROJECT_ID: PROJECT_ID}
    con_grp = models.ConfigGroup(client, dict(id=CONFIG_GROUP_ID, **config_group_config))

    client.api.config_group_delete.return_value = dict()

    response = client.delete(con_grp)

    assert response is None
    client.api.config_group_delete.assert_called_once_with(CONFIG_GROUP_ID)


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


def test_delete_run(client):
    RUN_ID = 111
    PROJECT_ID = 15

    run_config = {traw.const.NAME: 'mock name',
                  traw.const.DESCRIPTION: 'mock description',
                  traw.const.MILESTONE_ID: '22',
                  traw.const.ASSIGNEDTO_ID: '33',
                  traw.const.INCLUDE_ALL: True,
                  traw.const.CASE_IDS: list(),
                  traw.const.PROJECT_ID: PROJECT_ID}
    run = models.Run(client, dict(id=RUN_ID, **run_config))

    client.api.run_delete.return_value = dict()

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.delete(run)

    assert response is None
    client.api.run_delete.assert_called_once_with(RUN_ID)


def test_delete_suite(client):
    SUITE_ID = 111
    PROJECT_ID = 15

    suite_config = {traw.const.NAME: 'mock name',
                    traw.const.DESCRIPTION: 'mock description',
                    traw.const.PROJECT_ID: PROJECT_ID}
    suite = models.Suite(client, dict(id=SUITE_ID, **suite_config))

    client.api.suite_delete.return_value = dict()

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.delete(suite)

    assert response is None
    client.api.suite_delete.assert_called_once_with(SUITE_ID)


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


def test_update_config(client):
    CONFIG_ID = 16
    CONFIG_GROUP_ID = 17

    config_config = {traw.const.NAME: 'mock name',
                     'group_id': CONFIG_GROUP_ID}

    config = models.Config(client, dict(extra='extra', **config_config))

    client.api.config_update.return_value = dict(id=CONFIG_ID, **config_config)

    response = client.update(config)

    assert isinstance(response, models.Config)
    assert response.id == CONFIG_ID
    assert client.api.config_update.called
    assert 'mock name' in str(client.api.config_update.call_args)
    assert 'extra' not in str(client.api.config_update.call_args)


def test_update_config_group(client):
    CONFIG_GROUP_ID = 17

    config_group_config = {traw.const.NAME: 'mock name'}

    con_grp = models.ConfigGroup(client, dict(extra='extra', **config_group_config))

    client.api.config_group_update.return_value = dict(id=CONFIG_GROUP_ID, **config_group_config)

    response = client.update(con_grp)

    assert isinstance(response, models.ConfigGroup)
    assert response.id == CONFIG_GROUP_ID
    assert client.api.config_group_update.called
    assert 'mock name' in str(client.api.config_group_update.call_args)
    assert 'extra' not in str(client.api.config_group_update.call_args)


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
    assert 'mock name' in str(client.api.milestone_update.call_args)
    assert 'extra' not in str(client.api.milestone_update.call_args)


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
    assert 'mock name' in str(client.api.project_update.call_args)
    assert 'extra' not in str(client.api.project_update.call_args)


def test_update_run_include_all(client):
    RUN_ID = 111
    PROJECT_ID = 15

    run_config = {traw.const.NAME: 'mock name',
                  traw.const.DESCRIPTION: 'mock description',
                  traw.const.MILESTONE_ID: '22',
                  traw.const.ASSIGNEDTO_ID: '33',
                  traw.const.INCLUDE_ALL: True,
                  traw.const.CASE_IDS: list(),
                  traw.const.PROJECT_ID: PROJECT_ID}
    run = models.Run(client, dict(extra='extra', **run_config))

    client.api.run_update.return_value = dict(id=RUN_ID, **run_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.update(run)

    assert isinstance(response, models.Run)
    assert response.id == RUN_ID
    assert client.api.run_update.called
    assert 'mock name' in str(client.api.run_update.call_args)
    assert 'extra' not in str(client.api.run_update.call_args)


def test_update_run_w_case_ids(client):
    RUN_ID = 111
    PROJECT_ID = 15

    run_config = {traw.const.NAME: 'mock name',
                  traw.const.DESCRIPTION: 'mock description',
                  traw.const.MILESTONE_ID: '22',
                  traw.const.ASSIGNEDTO_ID: '33',
                  traw.const.INCLUDE_ALL: True,
                  traw.const.CASE_IDS: [1, 2, 3],
                  traw.const.PROJECT_ID: PROJECT_ID}
    run = models.Run(client, dict(extra='extra', **run_config))

    client.api.run_update.return_value = dict(id=RUN_ID, **run_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.update(run)

    assert isinstance(response, models.Run)
    assert response.id == RUN_ID
    assert client.api.run_update.called
    assert 'mock name' in str(client.api.run_update.call_args)
    assert '1,2,3' in str(client.api.run_update.call_args)
    assert 'extra' not in str(client.api.run_update.call_args)


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
    assert 'mock name' in str(client.api.milestone_update.call_args)
    assert 'extra' not in str(client.api.milestone_update.call_args)


def test_update_suite(client):
    SUITE_ID = 111
    PROJECT_ID = 15

    suite_config = {traw.const.NAME: 'mock name',
                    traw.const.DESCRIPTION: 'mock description',
                    traw.const.PROJECT_ID: PROJECT_ID}
    suite = models.Suite(client, dict(extra='extra', **suite_config))

    client.api.suite_update.return_value = dict(id=SUITE_ID, **suite_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.update(suite)

    assert isinstance(response, models.Suite)
    assert response.id == SUITE_ID
    assert client.api.suite_update.called
    assert 'mock name' in str(client.api.suite_update.call_args)
    assert 'extra' not in str(client.api.suite_update.call_args)


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


def test_config(client):
    """ Verify config method returns a new models.Config instance if
        called without any parameters
    """
    config = client.config()

    assert isinstance(config, models.Config)
    assert config.name is None
    assert config.id is None
    assert config.config_group is None


def test_config_by_project(client):
    """ Verify calling ``client.config(project, 456)`` with a project with ID
        of 123 and config ID of 456 returns a config object
    """
    PROJECT_ID = 15
    PROJECT = models.Project(client, {'id': PROJECT_ID})
    CONFIG_ID = 4

    client.api.config_groups.return_value = [CG1, CG2, CG3]
    client.api.project_by_id.return_value = {'id': PROJECT_ID}

    config = client.config(PROJECT, CONFIG_ID)

    assert isinstance(config, models.Config)
    assert config.id == CONFIG_ID
    assert config.id == CONF4['id']
    assert config.name == CONF4['name']
    assert config.project.id == PROJECT_ID

    client.api.config_groups.assert_called_once_with(PROJECT_ID)


def test_config_by_project_id(client):
    """ Verify calling ``client.config(123, 456)`` with a project ID of 123
        and config ID of 456 returns a config object
    """
    PROJECT_ID = 15
    CONFIG_ID = 4

    client.api.config_groups.return_value = [CG1, CG2, CG3]
    client.api.project_by_id.return_value = {'id': PROJECT_ID}

    config = client.config(PROJECT_ID, CONFIG_ID)

    assert isinstance(config, models.Config)
    assert config.id == CONFIG_ID
    assert config.id == CONF4['id']
    assert config.name == CONF4['name']
    assert config.project.id == PROJECT_ID

    client.api.config_groups.assert_called_once_with(PROJECT_ID)


def test_config_by_project_exc(client):
    """ Verify calling ``client.config(project, 456)`` raises an exception
        if nothing matching the params is found
    """
    PROJECT_ID = 15
    PROJECT = models.Project(client, {'id': PROJECT_ID})
    CONFIG_ID = 444

    client.api.config_groups.return_value = [CG1, CG2, CG3]
    client.api.project_by_id.return_value = {'id': PROJECT_ID}

    with pytest.raises(TRAWClientError) as exc:
        client.config(PROJECT, CONFIG_ID)

    assert 'with id of 444' in str(exc)

    client.api.config_groups.assert_called_once_with(PROJECT_ID)


def test_config_group(client):
    """ Verify config group method returns a new models.ConfigGroup instance if
        called without any parameters
    """
    cg = client.config_group()

    assert isinstance(cg, models.ConfigGroup)
    assert cg.name is None
    assert cg.id is None
    assert cg.project is None
    assert list(cg.configs) == list()


def test_config_group_by_project(client):
    """ Verify calling ``client.config_group(123)`` with an ID returns
        a config group object
    """
    PROJECT_ID = 15
    PROJECT = models.Project(client, {'id': PROJECT_ID})
    CONFIG_GROUP_ID = 662

    client.api.config_groups.return_value = [CG1, CG2, CG3]
    client.api.project_by_id.return_value = {'id': PROJECT_ID}

    config_group = client.config_group(PROJECT, CONFIG_GROUP_ID)

    assert isinstance(config_group, models.ConfigGroup)
    assert config_group.id == CONFIG_GROUP_ID
    assert config_group.name == 'configgroup2'
    assert config_group.project.id == PROJECT_ID

    client.api.config_groups.assert_called_once_with(PROJECT_ID)


def test_config_group_by_project_id(client):
    """ Verify calling ``client.config_group(123)`` with an ID returns
        a config group object
    """
    PROJECT_ID = 15
    CONFIG_GROUP_ID = 662

    client.api.config_groups.return_value = [CG1, CG2, CG3]
    client.api.project_by_id.return_value = {'id': PROJECT_ID}

    config_group = client.config_group(PROJECT_ID, CONFIG_GROUP_ID)

    assert isinstance(config_group, models.ConfigGroup)
    assert config_group.id == CONFIG_GROUP_ID
    assert config_group.name == 'configgroup2'
    assert config_group.project.id == PROJECT_ID

    client.api.config_groups.assert_called_once_with(PROJECT_ID)


def test_config_group_exc(client):
    """ Verify calling ``client.config_group(123)`` with an ID throws an
        exception if called with an recognized Config Group ID
    """
    PROJECT_ID = 15
    CONFIG_GROUP_ID = 666

    client.api.config_groups.return_value = [CG1, CG2, CG3]
    client.api.project_by_id.return_value = {'id': PROJECT_ID}

    with pytest.raises(TRAWClientError) as exc:
        client.config_group(PROJECT_ID, CONFIG_GROUP_ID)

    assert "models.ConfigGroup" in str(exc)
    assert "id of 666" in str(exc)

    client.api.config_groups.assert_called_once_with(PROJECT_ID)


def test_config_groups_by_project(client):
    """ Verify calling ``client.config_groups(project)`` with an ID returns
        a config group generator
    """
    PROJECT_ID = 15
    PROJECT = models.Project(client, {'id': PROJECT_ID})
    client.api.config_groups.return_value = [CG1, CG2, CG3]
    config_groups = client.config_groups(PROJECT)

    cg1 = next(config_groups)
    assert isinstance(cg1, models.ConfigGroup)
    assert cg1.id == 661

    cg2 = next(config_groups)
    assert isinstance(cg2, models.ConfigGroup)
    assert cg2.id == 662

    cg3 = next(config_groups)
    assert isinstance(cg3, models.ConfigGroup)
    assert cg3.id == 663

    client.api.config_groups.assert_called_once_with(PROJECT_ID)


def test_config_groups_by_project_id(client):
    """ Verify calling ``client.config_groups(123)`` with an ID returns
        a config group generator
    """
    client.api.config_groups.return_value = [CG1, CG2, CG3]
    config_groups = client.config_groups(1234)

    cg1 = next(config_groups)
    assert isinstance(cg1, models.ConfigGroup)
    assert cg1.id == 661

    cg2 = next(config_groups)
    assert isinstance(cg2, models.ConfigGroup)
    assert cg2.id == 662

    cg3 = next(config_groups)
    assert isinstance(cg3, models.ConfigGroup)
    assert cg3.id == 663

    client.api.config_groups.assert_called_once_with(1234)


def test_config_groups(client):
    """ Verify an exception is thrown if config_groups is called with no
        parameters
    """
    with pytest.raises(NotImplementedError) as exc:
        client.config_groups()

    assert 'models.Project or int' in str(exc)


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


def test_plan(client):
    """ Verify plan method returns a new models.Plan instance if called without
        any parameters
    """
    plan = client.plan()

    assert isinstance(plan, models.Plan)
    # TODO: Complete when Run is more than a stub
    # assert proj.announcement is None
    # assert proj.completed_on is None
    # assert proj.is_completed is False
    # assert proj.show_announcement is False
    # assert proj.suite_mode is None
    # assert proj.url is None


def test_plan_by_id(client):
    """ Verify calling ``client.plan(123)`` with an ID returns that plan """
    client.api.plan_by_id.return_value = {'id': 1234}
    plan = client.plan(1234)

    assert isinstance(plan, models.Plan)
    assert plan.id == 1234
    client.api.plan_by_id.assert_called_once_with(1234)


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


def test_custom_status_exc(client):
    """ Verify the Client's ``custom_status`` method throws an exception
        if called
    """
    with pytest.raises(NotImplementedError) as exc:
        client.custom_status()

    assert 'You must pass in int object' in str(exc)
    assert not client.api.statuses.called


def test_custom_status_by_int(client):
    """ Verify the Client's ``custom_status`` method call with int"""
    client.api.statuses.return_value = [STAT1, STAT2, STAT3, STAT4]

    status = client.custom_status(3)

    assert isinstance(status, models.Status)
    assert status.id == 8
    assert client.api.statuses.called


def test_custom_status_by_int_exc(client):
    """ Verify the Client's ``custom_status`` method call with int"""
    client.api.statuses.return_value = [STAT1, STAT2, STAT3, STAT4]

    with pytest.raises(UnknownCustomStatusError) as exc:
        client.custom_status(30)

    assert 'with custom status ID 3' in str(exc)


def test_custom_status_by_name(client):
    """ Verify the Client's ``custom_status`` method call with a name """
    client.api.statuses.return_value = [STAT1, STAT2, STAT3, STAT4]

    status = client.custom_status('custom_status3')

    assert isinstance(status, models.Status)
    assert status.id == 8
    assert client.api.statuses.called


def test_custom_status_by_name_exc_1(client):
    """ Verify the Client's ``custom_status`` raises an exception """

    with pytest.raises(UnknownCustomStatusError) as exc:
        client.custom_status('bogus_custom_status3')

    assert "be of format 'custom_statusX'" in str(exc)
    assert not client.api.statuses.called


def test_custom_status_by_name_exc_2(client):
    """ Verify the Client's ``custom_status`` raises an exception """

    with pytest.raises(UnknownCustomStatusError) as exc:
        client.custom_status('custom_status9')

    assert "is between 1 and 7" in str(exc)
    assert not client.api.statuses.called


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

    status = client.status('failed', strict=True)

    assert isinstance(status, models.Status)
    assert status.id == STAT3['id']
    assert status.label == 'failed'
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


def test_suite(client):
    """ Verify the Client's ``suite`` method returns models.Suit object """
    suite = client.suite()

    assert isinstance(suite, models.Suite)
    assert suite.completed_on is None
    assert suite.description is None
    assert suite.is_baseline is False
    assert suite.is_completed is False
    assert suite.is_master is False
    assert suite.name is None
    assert suite.project is None
    assert suite.url is None


def test_suite_by_id(client):
    """ Verify calling ``client.suite(123)`` with an ID returns that suite """
    client.api.suite_by_id.return_value = {'id': 1234}
    suite = client.suite(1234)

    assert isinstance(suite, models.Suite)
    assert suite.id == 1234
    client.api.suite_by_id.assert_called_once_with(1234)


def test_suites_exc(client):
    """ Verify the Client's ``suites`` method throws an exception if called """
    with pytest.raises(NotImplementedError) as exc:
        client.suites()

    assert 'You must pass in models.Project or int object' in str(exc)
    assert not client.api.suites_by_project_id.called


def test_suites_by_project_id(client):
    """ Verify calling ``client.suites(123)`` with an ID returns suite generator """
    client.api.suites_by_project_id.return_value = [SUIT1, SUIT2, SUIT3]
    suites = client.suites(1234)

    suite1 = next(suites)
    assert isinstance(suite1, models.Suite)
    assert suite1.id == 551

    suite2 = next(suites)
    assert isinstance(suite2, models.Suite)
    assert suite2.id == 552

    suite3 = next(suites)
    assert isinstance(suite3, models.Suite)
    assert suite3.id == 553

    client.api.suites_by_project_id.assert_called_once_with(1234)


def test_suites_by_project(client):
    """ Verify calling ``client.suites(Project)`` with an ID returns suite generator """
    client.api.suites_by_project_id.return_value = [SUIT1, SUIT2, SUIT3]
    suites = client.suites(models.Project(client, {'id': 1234}))

    suite1 = next(suites)
    assert isinstance(suite1, models.Suite)
    assert suite1.id == 551

    suite2 = next(suites)
    assert isinstance(suite2, models.Suite)
    assert suite2.id == 552

    suite3 = next(suites)
    assert isinstance(suite3, models.Suite)
    assert suite3.id == 553

    client.api.suites_by_project_id.assert_called_once_with(1234)


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


def test_change_cache_timeout_single_change(client):
    """ Verify change_cache_timeout works for a single object type """
    client.api.cache_timeouts = dict()
    client.api.cache_timeouts[client.api] = dict()

    assert client.api.cache_timeouts[client.api] == dict()

    client.change_cache_timeout(30, models.Project)

    assert client.api.cache_timeouts[client.api][models.Project] == 30


def test_change_cache_timeout_change_all(client):
    """ Verify change_cache_timeout works for all object types """
    client.api.cache_timeouts = dict()
    client.api.cache_timeouts[client.api] = dict()

    assert client.api.cache_timeouts[client.api] == dict()

    client.change_cache_timeout(30)

    for cls_name in models.__all__:
        cls = getattr(models, cls_name)
        assert client.api.cache_timeouts[client.api][cls] == 30


def test_change_cache_timeout_exc(client):
    """ Verify change_cache_timeout raises an exception """
    with pytest.raises(TypeError) as exc:
        client.change_cache_timeout(30, type(1234))

    assert "found class of type {0}".format(type(1234)) in str(exc)


def test_clear_cache(client):
    """ Verify the Client's ``clear_cache`` method call """
    client.clear_cache()

    assert client.api.case_by_id.cache.clear.called
    assert client.api.case_types.cache.clear.called
    assert client.api.config_groups.cache.clear.called
    assert client.api.milestone_by_id.cache.clear.called
    assert client.api.milestones.cache.clear.called
    assert client.api.plan_by_id.cache.clear.called
    assert client.api.priorities.cache.clear.called
    assert client.api.project_by_id.cache.clear.called
    assert client.api.projects.cache.clear.called
    assert client.api.run_by_id.cache.clear.called
    assert client.api.statuses.cache.clear.called
    assert client.api.suite_by_id.cache.clear.called
    assert client.api.suites_by_project_id.cache.clear.called
    assert client.api.templates.cache.clear.called
    assert client.api.test_by_id.cache.clear.called
    assert client.api.tests_by_run_id.cache.clear.called
    assert client.api.user_by_email.cache.clear.called
    assert client.api.user_by_id.cache.clear.called
    assert client.api.users.cache.clear.called
