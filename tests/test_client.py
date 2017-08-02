from datetime import datetime as dt
import sys

import mock
import pytest

import traw
from traw import models
from traw.exceptions import TRAWClientError, UnknownCustomStatusError

USER = 'mock username'
PASS = 'mock password'
URL = 'mock url'

CASE1 = {'name': 'case1', 'id': 991}
CASE2 = {'name': 'case2', 'id': 992}
CASE3 = {'name': 'case3', 'id': 993}
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
RESU1 = {'name': 'result1', 'id': 771}
RESU2 = {'name': 'result2', 'id': 772}
RESU3 = {'name': 'result3', 'id': 773}
RUN1 = {'name': 'run1', 'id': 881}
RUN2 = {'name': 'run2', 'id': 882}
RUN3 = {'name': 'run3', 'id': 883}
RUN4 = {'name': 'run4', 'id': 884}
SECT1 = {'name': 'section1', 'id': 991}
SECT2 = {'name': 'section2', 'id': 992}
SECT3 = {'name': 'section3', 'id': 993}
STAT1 = {'name': 'status1', 'id': 221, 'label': 'Passed'}
STAT2 = {'name': 'status2', 'id': 222, 'label': 'Failed'}
STAT3 = {'name': 'status3', 'id': 223, 'label': 'failed'}
STAT4 = {'name': 'status4', 'id': 8, 'label': 'custom-failed'}
SUIT1 = {'name': 'suite1', 'id': 551}
SUIT2 = {'name': 'suite2', 'id': 552}
SUIT3 = {'name': 'suite3', 'id': 553}
TEMP1 = {'name': 'template1', 'id': 991}
TEMP2 = {'name': 'template2', 'id': 992}
TEMP3 = {'name': 'template3', 'id': 993}
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


def test_add_result(client):
    RESULT_ID = 111
    TEST_ID = 1155

    result_config = {traw.const.TEST_ID: 998877,
                     traw.const.STATUS_ID: 8,
                     traw.const.COMMENT: 'mock comment',
                     traw.const.VERSION: 'VER.SI.ON.RC',
                     traw.const.ELAPSED: 12345,
                     traw.const.DEFECTS: 'DEF1,DEF2',
                     traw.const.ASSIGNEDTO_ID: 77}
    result = models.Result(client, dict(extra='extra', **result_config))

    client.api.result_add.return_value = dict(id=RESULT_ID, **result_config)

    with mock.patch.object(client, 'test') as test_mock:
        test_mock.return_value = models.Test(client, {'id': TEST_ID})
        response = client.add(result)

    assert isinstance(response, models.Result)
    assert response.id == RESULT_ID
    assert client.api.result_add.called
    assert 'mock comment' in str(client.api.result_add.call_args)
    assert 'extra' not in str(client.api.result_add.call_args)


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
    assert '[1, 2, 3, 4]' in str(client.api.run_add.call_args)
    assert 'extra' not in str(client.api.run_add.call_args)


def test_add_section(client):
    SECTION_ID = 14
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}

    section_config = {traw.const.NAME: 'mock name',
                      traw.const.DESCRIPTION: 'mock description',
                      traw.const.PROJECT_ID: PROJECT_ID}
    section = models.Section(client, dict(extra='extra', **section_config))

    client.api.section_add.return_value = dict(id=SECTION_ID, **section_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, PROJECT_DICT)
        response = client.add(section)

    assert isinstance(response, models.Section)
    assert response.id == SECTION_ID
    assert client.api.section_add.called
    assert 'mock name' in str(client.api.section_add.call_args)
    assert 'extra' not in str(client.api.section_add.call_args)


def test_add_section_w_suite(client):
    SECTION_ID = 13
    SUITE_ID = 14
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 2}

    section_config = {traw.const.NAME: 'mock name',
                      traw.const.DESCRIPTION: 'mock description',
                      traw.const.PROJECT_ID: PROJECT_ID,
                      traw.const.SUITE_ID: SUITE_ID}
    section = models.Section(client, dict(extra='extra', **section_config))

    client.api.section_add.return_value = dict(id=SECTION_ID, **section_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, PROJECT_DICT)
        response = client.add(section)

    assert isinstance(response, models.Section)
    assert response.id == SECTION_ID
    assert client.api.section_add.called
    assert 'mock name' in str(client.api.section_add.call_args)
    assert 'extra' not in str(client.api.section_add.call_args)


def test_add_section_exc(client):
    SECTION_ID = 13
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 2}

    section_config = {traw.const.NAME: 'mock name',
                      traw.const.DESCRIPTION: 'mock description',
                      traw.const.PROJECT_ID: PROJECT_ID}
    section = models.Section(client, dict(extra='extra', **section_config))

    client.api.section_add.return_value = dict(id=SECTION_ID, **section_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, PROJECT_DICT)

        with pytest.raises(ValueError) as exc:
            client.add(section)

    assert "not in Single Suite mode" in str(exc)
    assert not client.api.section_add.called
    proj_mock.assert_called_once_with(PROJECT_ID)


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


def test_delete_section(client):
    SECTION_ID = 111
    PROJECT_ID = 15

    section_config = {traw.const.NAME: 'mock name',
                      traw.const.DESCRIPTION: 'mock description',
                      traw.const.PROJECT_ID: PROJECT_ID}
    section = models.Section(client, dict(id=SECTION_ID, **section_config))

    client.api.section_delete.return_value = dict()

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.delete(section)

    assert response is None
    client.api.section_delete.assert_called_once_with(SECTION_ID)


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


def test_update_section(client):
    SECTION_ID = 111
    PROJECT_ID = 15

    section_config = {traw.const.NAME: 'mock name',
                      traw.const.DESCRIPTION: 'mock description',
                      traw.const.DUE_ON: 123456,
                      traw.const.START_ON: 12345,
                      traw.const.PROJECT_ID: PROJECT_ID}
    section = models.Section(client, dict(extra='extra', **section_config))

    client.api.section_update.return_value = dict(id=SECTION_ID, **section_config)

    with mock.patch.object(client, 'project') as proj_mock:
        proj_mock.return_value = models.Project(client, {'id': PROJECT_ID})
        response = client.update(section)

    assert isinstance(response, models.Section)
    assert response.id == SECTION_ID
    assert client.api.section_update.called
    assert 'mock name' in str(client.api.section_update.call_args)
    assert 'extra' not in str(client.api.section_update.call_args)


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
    assert case.created_by is None
    assert case.created_on is None
    assert case.estimate is None
    assert case.estimate_forecast is None
    assert case.id is None
    assert case.milestone is None
    assert case.priority is None
    assert case.suite is None
    assert case.template is None
    assert case.title is None
    assert case.case_type is None
    assert case.updated_by is None
    assert case.updated_on is None


def test_case_by_id(client):
    """ Verify calling ``client.case(123)`` with an ID returns that case """
    client.api.case_by_id.return_value = {'id': 1234}
    case = client.case(1234)

    assert isinstance(case, models.Case)
    assert case.id == 1234
    client.api.case_by_id.assert_called_once_with(1234)


def test_cases_exc(client):
    """ Verify the Client's ``cases`` method throws an exception if called """
    with pytest.raises(NotImplementedError) as exc:
        client.cases()

    assert 'You must pass in models.Project or int object' in str(exc)
    assert not client.api.cases_by_project_id.called


def test_cases_by_project_id(client):
    """ Verify calling ``client.cases(123)`` with an ID returns case
        generator
    """
    PROJECT_ID = 15
    client.api.project_by_id.return_value = {'id': PROJECT_ID, 'suite_mode': 1}
    client.api.cases_by_project_id.return_value = [CASE1, CASE2, CASE3]
    cases = client.cases(PROJECT_ID)

    case1 = next(cases)
    assert isinstance(case1, models.Case)
    assert case1.id == 991

    case2 = next(cases)
    assert isinstance(case2, models.Case)
    assert case2.id == 992

    case3 = next(cases)
    assert isinstance(case3, models.Case)
    assert case3.id == 993

    client.api.project_by_id.assert_called_once_with(PROJECT_ID)
    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project(client):
    """ Verify calling ``client.cases(Project)`` with an ID returns
        case generator
    """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    client.api.project_by_id.return_value = PROJECT_DICT
    client.api.cases_by_project_id.return_value = [CASE1, CASE2, CASE3]

    cases = client.cases(models.Project(client, PROJECT_DICT))

    case1 = next(cases)
    assert isinstance(case1, models.Case)
    assert case1.id == 991

    case2 = next(cases)
    assert isinstance(case2, models.Case)
    assert case2.id == 992

    case3 = next(cases)
    assert isinstance(case3, models.Case)
    assert case3.id == 993

    client.api.project_by_id.assert_called_once_with(PROJECT_ID)
    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_and_suite_and_section(client):
    """ Verify calling ``client.cases(Project, Suite, Section)`` returns
        case generator
    """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 2}
    SUITE_ID = 16
    SUITE_DICT = {'id': SUITE_ID}
    SECTION_ID = 17
    SECTION_DICT = {'id': SECTION_ID}

    client.api.project_by_id.return_value = PROJECT_DICT
    client.api.cases_by_project_id.return_value = [CASE1, ]

    project = models.Project(client, PROJECT_DICT)
    suite = models.Suite(client, SUITE_DICT)
    section = models.Section(client, SECTION_DICT)
    cases = client.cases(project, suite, section)

    case1 = next(cases)
    assert isinstance(case1, models.Case)
    assert case1.id == 991

    client.api.project_by_id.assert_called_once_with(PROJECT_ID)
    client.api.cases_by_project_id.assert_called_once_with(
        PROJECT_ID, suite_id=SUITE_ID, section_id=SECTION_ID)


def test_cases_by_project_and_suite_id_and_section_id(client):
    """ Verify calling ``client.cases(Project, 16, 17)`` returns
        case generator
    """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 2}
    SUITE_ID = 16
    SECTION_ID = 17

    client.api.project_by_id.return_value = PROJECT_DICT
    client.api.cases_by_project_id.return_value = [CASE1, ]

    project = models.Project(client, PROJECT_DICT)
    cases = client.cases(project, SUITE_ID, SECTION_ID)

    case1 = next(cases)
    assert isinstance(case1, models.Case)
    assert case1.id == 991

    client.api.project_by_id.assert_called_once_with(PROJECT_ID)
    client.api.cases_by_project_id.assert_called_once_with(
        PROJECT_ID, suite_id=SUITE_ID, section_id=SECTION_ID)


def test_cases_by_project_exc_1(client):
    """ Verify calling ``client.cases(Project)`` when the project is a
        suite_mode of 2 raises an exception
    """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 2}

    client.api.project_by_id.return_value = PROJECT_DICT
    client.api.cases_by_project_id.return_value = [SECT1, ]

    with pytest.raises(TypeError) as exc:
        list(client.cases(models.Project(client, PROJECT_DICT)))

    assert 'suite_mode of 2' in str(exc)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)
    assert not client.api.cases_by_project_id.called


def test_cases_by_project_exc_2(client):
    """ Verify calling ``client.cases(Project, 'asdf')`` when the project
        is a suite_mode of 2 raises an exception
    """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 2}

    client.api.project_by_id.return_value = PROJECT_DICT
    client.api.cases_by_project_id.return_value = [CASE1, ]

    with pytest.raises(TypeError) as exc:
        list(client.cases(models.Project(client, PROJECT_DICT), 'asdf'))

    assert 'models.Suite' in str(exc)
    assert 'int ID of a suite in testrail' in str(exc)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)
    assert not client.api.cases_by_project_id.called


def test_cases_by_project_exc_3(client):
    """ Verify calling ``client.cases(Project, None, 'asdf')`` when the project
        is a suite_mode of 2 raises an exception
    """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 2}
    SUITE_ID = 16

    client.api.project_by_id.return_value = PROJECT_DICT
    client.api.cases_by_project_id.return_value = [CASE1, ]

    with pytest.raises(TypeError) as exc:
        list(client.cases(models.Project(client, PROJECT_DICT), SUITE_ID, 'asdf'))

    assert 'models.Section' in str(exc)
    assert 'int ID of a section in testrail' in str(exc)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)
    assert not client.api.cases_by_project_id.called


def test_cases_by_project_w_case_type(client):
    """ Verify calling ``client.cases(Project)`` with case_type """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    ct = models.CaseType(client, {'id': 11})
    list(client.cases(project, case_type=ct))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, type_id='11')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_case_type_list(client):
    """ Verify calling ``client.cases(Project)`` with case_type """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    ct1 = models.CaseType(client, {'id': 11})
    ct2 = models.CaseType(client, {'id': 12})
    list(client.cases(project, case_type=[ct1, ct2]))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, type_id='11,12')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_case_type_id(client):
    """ Verify calling ``client.cases(Project)`` with case_type """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, case_type=11))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, type_id='11')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_case_type_id_list(client):
    """ Verify calling ``client.cases(Project)`` with case_type """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, case_type=[11, 12]))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, type_id='11,12')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_case_type_exc(client):
    """ Verify calling ``client.cases(Project)`` with case_type exception """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    with pytest.raises(TypeError) as exc:
        list(client.cases(project, case_type='asdf'))

    assert 'asdf' in str(exc)
    assert str(models.CaseType) in str(exc)
    assert str(int) in str(exc)


def test_cases_by_project_w_int_created_after(client):
    """ Verify calling ``client.cases(Project)`` with created_after """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, created_after=1112))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, created_after=1112)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_float_created_after(client):
    """ Verify calling ``client.cases(Project)`` with created_after """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, created_after=11.12))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, created_after=11)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_datetime_created_after(client):
    """ Verify calling ``client.cases(Project)`` with created_after """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    ca_dt = dt.fromtimestamp(33.22)
    list(client.cases(project, created_after=ca_dt))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, created_after=33)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_created_after_exc(client):
    """ Verify calling ``client.cases(Project)`` with created_after exception """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    client.api.project_by_id.return_value = PROJECT_DICT

    with pytest.raises(TypeError) as exc:
        list(client.cases(
            models.Project(client, {'id': 1234}), created_after='asdf'))

    assert 'created/updated after/before' in str(exc)
    assert 'asdf' in str(exc)
    assert not client.api.cases_by_project_id.called


def test_cases_by_project_w_int_created_before(client):
    """ Verify calling ``client.cases(Project)`` with created_before """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, created_before=1112))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, created_before=1112)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_float_created_before(client):
    """ Verify calling ``client.cases(Project)`` with created_before """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, created_before=11.12))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, created_before=11)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_datetime_created_before(client):
    """ Verify calling ``client.cases(Project)`` with created_before """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    ca_dt = dt.fromtimestamp(33.22)
    list(client.cases(project, created_before=ca_dt))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, created_before=33)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_created_before_exc(client):
    """ Verify calling ``client.cases(Project)`` with created_before exception """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    with pytest.raises(TypeError) as exc:
        list(client.cases(project, created_before='asdf'))

    assert 'created/updated after/before' in str(exc)
    assert 'asdf' in str(exc)
    assert not client.api.cases_by_project_id.called


def test_cases_by_project_w_created_by_user(client):
    """ Verify calling ``client.cases(Project)`` with created_by """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    user = models.User(client, {'id': 11})
    list(client.cases(project, created_by=user))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, created_by='11')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_created_by_user_list(client):
    """ Verify calling ``client.cases(Project)`` with created_by """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    user1 = models.User(client, {'id': 11})
    user2 = models.User(client, {'id': 12})
    list(client.cases(project, created_by=[user1, user2]))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, created_by='11,12')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_created_by_user_id(client):
    """ Verify calling ``client.cases(Project)`` with created_by """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, created_by=11))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, created_by='11')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_created_by_user_id_list(client):
    """ Verify calling ``client.cases(Project)`` with created_by """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, created_by=[11, 12]))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, created_by='11,12')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_created_by_exc(client):
    """ Verify calling ``client.cases(Project)`` with created_by exception """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    with pytest.raises(TypeError) as exc:
        list(client.cases(project, created_by='asdf'))

    assert 'asdf' in str(exc)
    assert str(models.User) in str(exc)
    assert str(int) in str(exc)


def test_cases_by_project_w_milestone(client):
    """ Verify calling ``client.cases(Project)`` with milestone """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    milestone = models.Milestone(client, {'id': 11})
    list(client.cases(project, milestone=milestone))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, milestone_id='11')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_milestone_list(client):
    """ Verify calling ``client.cases(Project)`` with milestone """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    milestone1 = models.Milestone(client, {'id': 11})
    milestone2 = models.Milestone(client, {'id': 12})
    list(client.cases(project, milestone=[milestone1, milestone2]))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, milestone_id='11,12')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_milestone_id(client):
    """ Verify calling ``client.cases(Project)`` with milestone """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, milestone=11))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, milestone_id='11')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_milestone_id_list(client):
    """ Verify calling ``client.cases(Project)`` with milestone """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, milestone=[11, 12]))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, milestone_id='11,12')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_milestone_exc(client):
    """ Verify calling ``client.cases(Project)`` with milestone exception """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    with pytest.raises(TypeError) as exc:
        list(client.cases(project, milestone='asdf'))

    assert 'asdf' in str(exc)
    assert str(models.Milestone) in str(exc)
    assert str(int) in str(exc)


def test_cases_by_project_w_sub_milestone(client):
    """ Verify calling ``client.cases(Project)`` with sub-milestone """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    submilestone = models.SubMilestone(client, {'id': 11})
    list(client.cases(project, milestone=submilestone))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, milestone_id='11')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_sub_milestone_list(client):
    """ Verify calling ``client.cases(Project)`` with sub-milestone """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    submilestone1 = models.SubMilestone(client, {'id': 11})
    submilestone2 = models.SubMilestone(client, {'id': 12})
    list(client.cases(project, milestone=[submilestone1, submilestone2]))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, milestone_id='11,12')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_priority(client):
    """ Verify calling ``client.cases(Project)`` with priority """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    priority = models.Priority(client, {'id': 11})
    list(client.cases(project, priority=priority))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, priority_id='11')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_priority_list(client):
    """ Verify calling ``client.cases(Project)`` with priority """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    priority1 = models.Priority(client, {'id': 11})
    priority2 = models.Priority(client, {'id': 12})
    list(client.cases(project, priority=[priority1, priority2]))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, priority_id='11,12')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_priority_id(client):
    """ Verify calling ``client.cases(Project)`` with priority """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, priority=11))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, priority_id='11')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_priority_id_list(client):
    """ Verify calling ``client.cases(Project)`` with priority """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, priority=[11, 12]))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, priority_id='11,12')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_priority_exc(client):
    """ Verify calling ``client.cases(Project)`` with priority exception """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    with pytest.raises(TypeError) as exc:
        list(client.cases(project, priority='asdf'))

    assert 'asdf' in str(exc)
    assert str(models.Priority) in str(exc)
    assert str(int) in str(exc)


def test_cases_by_project_w_template(client):
    """ Verify calling ``client.cases(Project)`` with template """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    template = models.Template(client, {'id': 11})
    list(client.cases(project, template=template))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, template_id='11')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_template_list(client):
    """ Verify calling ``client.cases(Project)`` with template """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    template1 = models.Template(client, {'id': 11})
    template2 = models.Template(client, {'id': 12})
    list(client.cases(project, template=[template1, template2]))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, template_id='11,12')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_template_id(client):
    """ Verify calling ``client.cases(Project)`` with template """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, template=11))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, template_id='11')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_template_id_list(client):
    """ Verify calling ``client.cases(Project)`` with template """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, template=[11, 12]))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, template_id='11,12')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_template_exc(client):
    """ Verify calling ``client.cases(Project)`` with template exception """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    with pytest.raises(TypeError) as exc:
        list(client.cases(project, template='asdf'))

    assert 'asdf' in str(exc)
    assert str(models.Template) in str(exc)
    assert str(int) in str(exc)


def test_cases_by_project_w_int_updated_after(client):
    """ Verify calling ``client.cases(Project)`` with updated_after """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, updated_after=1112))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, updated_after=1112)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_float_updated_after(client):
    """ Verify calling ``client.cases(Project)`` with updated_after """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, updated_after=11.12))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, updated_after=11)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_datetime_updated_after(client):
    """ Verify calling ``client.cases(Project)`` with updated_after """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    ca_dt = dt.fromtimestamp(33.22)
    list(client.cases(project, updated_after=ca_dt))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, updated_after=33)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_updated_after_exc(client):
    """ Verify calling ``client.cases(Project)`` with updated_after exception """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    client.api.project_by_id.return_value = PROJECT_DICT

    with pytest.raises(TypeError) as exc:
        list(client.cases(
            models.Project(client, {'id': 1234}), updated_after='asdf'))

    assert 'created/updated after/before' in str(exc)
    assert 'asdf' in str(exc)
    assert not client.api.cases_by_project_id.called


def test_cases_by_project_w_int_updated_before(client):
    """ Verify calling ``client.cases(Project)`` with updated_before """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, updated_before=1112))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, updated_before=1112)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_float_updated_before(client):
    """ Verify calling ``client.cases(Project)`` with updated_before """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, updated_before=11.12))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, updated_before=11)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_datetime_updated_before(client):
    """ Verify calling ``client.cases(Project)`` with updated_before """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    ca_dt = dt.fromtimestamp(33.22)
    list(client.cases(project, updated_before=ca_dt))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, updated_before=33)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_updated_before_exc(client):
    """ Verify calling ``client.cases(Project)`` with updated_before exception """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    with pytest.raises(TypeError) as exc:
        list(client.cases(project, updated_before='asdf'))

    assert 'created/updated after/before' in str(exc)
    assert 'asdf' in str(exc)
    assert not client.api.cases_by_project_id.called


def test_cases_by_project_w_updated_by_user(client):
    """ Verify calling ``client.cases(Project)`` with updated_by """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    user = models.User(client, {'id': 11})
    list(client.cases(project, updated_by=user))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, updated_by='11')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_updated_by_user_list(client):
    """ Verify calling ``client.cases(Project)`` with updated_by """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    user1 = models.User(client, {'id': 11})
    user2 = models.User(client, {'id': 12})
    list(client.cases(project, updated_by=[user1, user2]))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, updated_by='11,12')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_updated_by_user_id(client):
    """ Verify calling ``client.cases(Project)`` with updated_by """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, updated_by=11))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, updated_by='11')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_updated_by_user_id_list(client):
    """ Verify calling ``client.cases(Project)`` with updated_by """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    list(client.cases(project, updated_by=[11, 12]))

    client.api.cases_by_project_id.assert_called_once_with(PROJECT_ID, updated_by='11,12')
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)


def test_cases_by_project_w_updated_by_exc(client):
    """ Verify calling ``client.cases(Project)`` with updated_by exception """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    project = models.Project(client, PROJECT_DICT)
    client.api.project_by_id.return_value = PROJECT_DICT

    with pytest.raises(TypeError) as exc:
        list(client.cases(project, updated_by='asdf'))

    assert 'asdf' in str(exc)
    assert str(models.User) in str(exc)
    assert str(int) in str(exc)


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


def test_result(client):
    """ Verify result method returns a new models.Result instance if called without
        any parameters
    """
    result = client.result()

    assert isinstance(result, models.Result)
    assert result.assigned_to is None
    assert result.comment is None
    assert result.created_by is None
    assert result.created_on is None
    assert list(result.defects) == list()
    assert result.elapsed is None
    assert result.status is None
    assert result.test is None
    assert result.version is None


def test_results_exc(client):
    """ Verify the Client's ``tests`` method throws an exception if called """
    with pytest.raises(NotImplementedError) as exc:
        client.results()

    assert 'You must pass in models.Test or int object' in str(exc)
    assert not client.api.results_by_test_id.called


def test_results_by_run(client):
    """ Verify calling ``client.results(123)`` with an ID returns result
        generator
    """
    client.api.results_by_run_id.return_value = [RESU1, RESU2, RESU3]
    results = client.results(models.Run(client, {'id': 1234}))

    result1 = next(results)
    assert isinstance(result1, models.Result)
    assert result1.id == 771

    result2 = next(results)
    assert isinstance(result2, models.Result)
    assert result2.id == 772

    result3 = next(results)
    assert isinstance(result3, models.Result)
    assert result3.id == 773

    client.api.results_by_run_id.assert_called_once_with(1234)


def test_results_by_run_id(client):
    """ Verify calling ``client.results(123, obj_type=models.Run)`` with
        an ID returns result generator
    """
    client.api.results_by_run_id.return_value = [RESU1, RESU2]
    results = client.results(1234, obj_type=models.Run, limit=2)

    result1 = next(results)
    assert isinstance(result1, models.Result)
    assert result1.id == 771

    result2 = next(results)
    assert isinstance(result2, models.Result)
    assert result2.id == 772

    client.api.results_by_run_id.assert_called_once_with(1234, limit=2)


def test_results_by_run_id_exc_1(client):
    """ Verify calling ``client.results(123, obj_type='asdf')`` throws
        an exception
    """
    with pytest.raises(TypeError) as exc:
        next(client.results(1234, obj_type='asdf'))

    assert str(models.Run) in str(exc)
    assert str(models.Test) in str(exc)
    assert 'asdf' in str(exc)


def test_results_by_test_id(client):
    """ Verify calling ``client.results(123)`` with an ID returns result
        generator
    """
    client.api.results_by_test_id.return_value = [RESU1, RESU2]
    results = client.results(1234, limit=2)

    result1 = next(results)
    assert isinstance(result1, models.Result)
    assert result1.id == 771

    result2 = next(results)
    assert isinstance(result2, models.Result)
    assert result2.id == 772

    client.api.results_by_test_id.assert_called_once_with(1234, limit=2)


def test_results_by_test_id_with_status(client):
    """ Verify calling ``client.results(123)`` with a status returns result
        generator
    """
    client.api.results_by_test_id.return_value = [RESU1, ]
    status = models.Status(client, {'id': 234})

    results = client.results(1234, with_status=status)

    result1 = next(results)
    assert isinstance(result1, models.Result)
    assert result1.id == 771

    client.api.results_by_test_id.assert_called_once_with(1234, status_id='234')


def test_results_by_test_id_with_int_status(client):
    """ Verify calling ``client.results(123)`` with an int status returns result
        generator
    """
    client.api.results_by_test_id.return_value = [RESU1, ]

    results = client.results(1234, with_status=111)

    result1 = next(results)
    assert isinstance(result1, models.Result)
    assert result1.id == 771

    client.api.results_by_test_id.assert_called_once_with(1234, status_id='111')


def test_results_by_test_id_with_2_status(client):
    """ Verify calling ``client.results(123)`` with an ID returns result
        generator
    """
    client.api.results_by_test_id.return_value = [RESU1, ]
    status1 = models.Status(client, {'id': 234})
    status2 = models.Status(client, {'id': 345})

    results = client.results(1234, with_status=(status1, status2))

    result1 = next(results)
    assert isinstance(result1, models.Result)
    assert result1.id == 771

    client.api.results_by_test_id.assert_called_once_with(1234, status_id='234,345')


def test_results_by_test_id_with_2_status_ids(client):
    """ Verify calling ``client.results(123)`` with status IDs returns result
        generator
    """
    client.api.results_by_test_id.return_value = [RESU1, ]

    results = client.results(1234, with_status=(234, 345))

    result1 = next(results)
    assert isinstance(result1, models.Result)
    assert result1.id == 771

    client.api.results_by_test_id.assert_called_once_with(1234, status_id='234,345')


def test_results_by_test_id_exc_1(client):
    """ Verify calling ``client.results(123, status)`` throws an exception """
    with pytest.raises(TypeError) as exc:
        next(client.results(1234, with_status=111.11))

    assert str(None) in str(exc)
    assert str(int) in str(exc)
    assert str(models.Status) in str(exc)
    assert 'with_status' in str(exc)
    assert str(111.11) in str(exc)
    assert not client.api.results_by_test_id.called


def test_results_by_test_id_exc_2(client):
    """ Verify calling ``client.results(123, status)`` throws an exception """
    status1 = models.Status(client, {'id': 234})
    status2 = models.Status(client, {'id': 345})

    with pytest.raises(TypeError) as exc:
        next(client.results(1234, with_status=(status1, 'asdf', status2)))

    assert str(None) in str(exc)
    assert str(int) in str(exc)
    assert str(models.Status) in str(exc)
    assert 'with_status' in str(exc)
    assert 'asdf' in str(exc)
    assert not client.api.results_by_test_id.called


def test_results_by_test(client):
    """ Verify calling ``client.results(123)`` with an ID returns result
        generator
    """
    client.api.results_by_test_id.return_value = [RESU1, RESU2, RESU3]
    results = client.results(models.Test(client, {'id': 1234}))

    result1 = next(results)
    assert isinstance(result1, models.Result)
    assert result1.id == 771

    result2 = next(results)
    assert isinstance(result2, models.Result)
    assert result2.id == 772

    result3 = next(results)
    assert isinstance(result3, models.Result)
    assert result3.id == 773

    client.api.results_by_test_id.assert_called_once_with(1234)


def test_results_by_test_with_status(client):
    """ Verify calling ``client.results(123)`` with an ID returns result
        generator
    """
    client.api.results_by_test_id.return_value = [RESU1, ]
    status = models.Status(client, {'id': 234})

    results = client.results(models.Test(client, {'id': 1234}), with_status=status)

    result1 = next(results)
    assert isinstance(result1, models.Result)
    assert result1.id == 771

    client.api.results_by_test_id.assert_called_once_with(1234, status_id='234')


def test_results_by_test_with_2_status(client):
    """ Verify calling ``client.results(123)`` with an ID returns result
        generator
    """
    client.api.results_by_test_id.return_value = [RESU1, ]
    status1 = models.Status(client, {'id': 234})
    status2 = models.Status(client, {'id': 345})

    results = client.results(models.Test(client, {'id': 1234}), with_status=(status1, status2))

    result1 = next(results)
    assert isinstance(result1, models.Result)
    assert result1.id == 771

    client.api.results_by_test_id.assert_called_once_with(1234, status_id='234,345')


def test_run(client):
    """ Verify run method returns a new models.Run instance if called without
        any parameters
    """
    run = client.run()

    assert isinstance(run, models.Run)
    assert run.assigned_to is None
    assert run.blocked_count is None
    assert list(run.cases) == list()
    assert run.completed_on is None
    assert list(run.configs) == list()
    assert run.created_by is None
    assert run.created_on is None
    assert run.description is None
    assert run.failed_count is None
    assert run.include_all is True
    assert run.is_completed is False
    assert run.milestone is None
    assert run.name is None
    assert run.passed_count is None
    assert run.plan is None
    assert run.project is None
    assert run.retest_count is None
    assert run.suite is None
    assert run.untested_count is None
    assert run.url is None


def test_run_by_id(client):
    """ Verify calling ``client.run(123)`` with an ID returns that run """
    client.api.run_by_id.return_value = {'id': 1234}
    run = client.run(1234)

    assert isinstance(run, models.Run)
    assert run.id == 1234
    client.api.run_by_id.assert_called_once_with(1234)


def test_runs_exc(client):
    """ Verify the Client's ``runs`` method throws an exception if called """
    with pytest.raises(NotImplementedError) as exc:
        client.runs()

    assert 'You must pass in models.Project or int object' in str(exc)
    assert not client.api.runs_by_project_id.called


def test_runs_by_project_id(client):
    """ Verify calling ``client.runs(123)`` with an ID returns suite generator """
    client.api.runs_by_project_id.return_value = [RUN1, RUN2, RUN3]
    runs = client.runs(1234)

    run1 = next(runs)
    assert isinstance(run1, models.Run)
    assert run1.id == 881

    run2 = next(runs)
    assert isinstance(run2, models.Run)
    assert run2.id == 882

    run3 = next(runs)
    assert isinstance(run3, models.Run)
    assert run3.id == 883

    client.api.runs_by_project_id.assert_called_once_with(1234)


def test_runs_by_project(client):
    """ Verify calling ``client.runs(Project)`` with an ID returns run generator """
    client.api.runs_by_project_id.return_value = [RUN1, RUN2, RUN3]
    runs = client.runs(models.Project(client, {'id': 1234}))

    run1 = next(runs)
    assert isinstance(run1, models.Run)
    assert run1.id == 881

    run2 = next(runs)
    assert isinstance(run2, models.Run)
    assert run2.id == 882

    run3 = next(runs)
    assert isinstance(run3, models.Run)
    assert run3.id == 883

    client.api.runs_by_project_id.assert_called_once_with(1234)


def test_runs_by_project_w_limit(client):
    """ Verify calling ``client.runs(Project)`` with a limit """
    list(client.runs(models.Project(client, {'id': 1234}), limit=2))

    client.api.runs_by_project_id.assert_called_once_with(1234, limit=2)


def test_runs_by_project_w_int_created_after(client):
    """ Verify calling ``client.runs(Project)`` with created_after """
    list(client.runs(models.Project(client, {'id': 1234}), created_after=1112))

    client.api.runs_by_project_id.assert_called_once_with(1234, created_after=1112)


def test_runs_by_project_w_float_created_after(client):
    """ Verify calling ``client.runs(Project)`` with created_after """
    list(client.runs(models.Project(client, {'id': 1234}), created_after=11.12))

    client.api.runs_by_project_id.assert_called_once_with(1234, created_after=11)


def test_runs_by_project_w_datetime_created_after(client):
    """ Verify calling ``client.runs(Project)`` with created_after """
    ca_dt = dt.fromtimestamp(33.22)
    list(client.runs(models.Project(client, {'id': 1234}), created_after=ca_dt))

    client.api.runs_by_project_id.assert_called_once_with(1234, created_after=33)


def test_runs_by_project_w_created_after_exc(client):
    """ Verify calling ``client.runs(Project)`` with created_after exception """
    with pytest.raises(TypeError) as exc:
        list(client.runs(
            models.Project(client, {'id': 1234}), created_after='asdf'))

    assert 'created/updated after/before' in str(exc)
    assert 'asdf' in str(exc)
    assert not client.api.runs_by_project_id.called


def test_runs_by_project_w_int_created_before(client):
    """ Verify calling ``client.runs(Project)`` with created_before """
    list(client.runs(models.Project(client, {'id': 1234}), created_before=1112))

    client.api.runs_by_project_id.assert_called_once_with(1234, created_before=1112)


def test_runs_by_project_w_float_created_before(client):
    """ Verify calling ``client.runs(Project)`` with created_before """
    list(client.runs(models.Project(client, {'id': 1234}), created_before=11.12))

    client.api.runs_by_project_id.assert_called_once_with(1234, created_before=11)


def test_runs_by_project_w_datetime_created_before(client):
    """ Verify calling ``client.runs(Project)`` with created_before """
    ca_dt = dt.fromtimestamp(33.22)
    list(client.runs(models.Project(client, {'id': 1234}), created_before=ca_dt))

    client.api.runs_by_project_id.assert_called_once_with(1234, created_before=33)


def test_runs_by_project_w_created_before_exc(client):
    """ Verify calling ``client.runs(Project)`` with created_before exception """
    with pytest.raises(TypeError) as exc:
        list(client.runs(
            models.Project(client, {'id': 1234}), created_before='asdf'))

    assert 'created/updated after/before' in str(exc)
    assert 'asdf' in str(exc)
    assert not client.api.runs_by_project_id.called


def test_runs_by_project_w_created_by_user(client):
    """ Verify calling ``client.runs(Project)`` with created_by """
    user = models.User(client, {'id': 11})
    list(client.runs(models.Project(client, {'id': 1234}), created_by=user))

    client.api.runs_by_project_id.assert_called_once_with(1234, created_by='11')


def test_runs_by_project_w_created_by_user_list(client):
    """ Verify calling ``client.runs(Project)`` with created_by """
    users = [models.User(client, {'id': 11}), models.User(client, {'id': 12})]
    list(client.runs(models.Project(client, {'id': 1234}), created_by=users))

    client.api.runs_by_project_id.assert_called_once_with(1234, created_by='11,12')


def test_runs_by_project_w_created_by_user_id(client):
    """ Verify calling ``client.runs(Project)`` with created_by """
    list(client.runs(models.Project(client, {'id': 1234}), created_by=11))

    client.api.runs_by_project_id.assert_called_once_with(1234, created_by='11')


def test_runs_by_project_w_created_by_user_id_list(client):
    """ Verify calling ``client.runs(Project)`` with created_by """
    list(client.runs(models.Project(client, {'id': 1234}), created_by=[11, 12]))

    client.api.runs_by_project_id.assert_called_once_with(1234, created_by='11,12')


def test_runs_by_project_w_created_by_exc(client):
    """ Verify calling ``client.runs(Project)`` with created_by exception """
    with pytest.raises(TypeError) as exc:
        list(client.runs(models.Project(client, {'id': 1234}), created_by='asdf'))

    assert 'asdf' in str(exc)
    assert str(models.User) in str(exc)
    assert str(int) in str(exc)


def test_runs_by_project_id_w_created_by_user(client):
    """ Verify calling ``client.runs(1234)`` with created_by """
    user = models.User(client, {'id': 11})
    list(client.runs(1234, created_by=user))

    client.api.runs_by_project_id.assert_called_once_with(1234, created_by='11')


def test_runs_by_project_id_w_created_by_user_id(client):
    """ Verify calling ``client.runs(1234)`` with created_by """
    list(client.runs(1234, created_by=11))

    client.api.runs_by_project_id.assert_called_once_with(1234, created_by='11')


def test_runs_by_project_id_w_created_by_exc(client):
    """ Verify calling ``client.runs(1234)`` with created_by exception """
    with pytest.raises(TypeError) as exc:
        list(client.runs(1234, created_by='asdf'))

    assert 'asdf' in str(exc)
    assert str(models.User) in str(exc)
    assert str(int) in str(exc)


def test_runs_by_project_w_is_completed_true(client):
    """ Verify calling ``client.runs(Project)`` with is_completed """
    list(client.runs(models.Project(client, {'id': 1234}), is_completed=True))

    client.api.runs_by_project_id.assert_called_once_with(1234, is_completed=1)


def test_runs_by_project_w_is_copmleted_false(client):
    """ Verify calling ``client.runs(Project)`` with is_completed """
    list(client.runs(models.Project(client, {'id': 1234}), is_completed=False))

    client.api.runs_by_project_id.assert_called_once_with(1234, is_completed=0)


def test_runs_by_project_w_is_completed_exc(client):
    """ Verify calling ``client.runs(Project)`` with is_completed exception """
    with pytest.raises(TypeError) as exc:
        list(client.runs(models.Project(client, {'id': 1234}), is_completed='asdf'))

    assert 'asdf' in str(exc)
    assert 'None, True, or False' in str(exc)


def test_runs_by_project_id_w_is_completed_true(client):
    """ Verify calling ``client.runs(1234)`` with is_completed """
    list(client.runs(1234, is_completed=True))

    client.api.runs_by_project_id.assert_called_once_with(1234, is_completed=1)


def test_runs_by_project_id_w_is_completed_false(client):
    """ Verify calling ``client.runs(1234)`` with is_completed """
    list(client.runs(1234, is_completed=False))

    client.api.runs_by_project_id.assert_called_once_with(1234, is_completed=0)


def test_runs_by_project_id_w_is_complete_exc(client):
    """ Verify calling ``client.runs(1234)`` with is_completed exception """
    with pytest.raises(TypeError) as exc:
        list(client.runs(1234, is_completed='asdf'))

    assert 'asdf' in str(exc)
    assert 'None, True, or False' in str(exc)


def test_runs_by_project_w_milestone(client):
    """ Verify calling ``client.runs(Project)`` with milestone """
    ms = models.Milestone(client, {'id': 22})
    list(client.runs(models.Project(client, {'id': 1234}), milestone=ms))

    client.api.runs_by_project_id.assert_called_once_with(1234, milestone_id='22')


def test_runs_by_project_w_milestone_id(client):
    """ Verify calling ``client.runs(Project)`` with milestone """
    list(client.runs(models.Project(client, {'id': 1234}), milestone=22))

    client.api.runs_by_project_id.assert_called_once_with(1234, milestone_id='22')


def test_runs_by_project_w_milestone_exc(client):
    """ Verify calling ``client.runs(Project)`` with milestone exception """
    with pytest.raises(TypeError) as exc:
        list(client.runs(models.Project(client, {'id': 1234}), milestone='asdf'))

    assert 'asdf' in str(exc)
    assert str(models.Milestone) in str(exc)
    assert str(models.SubMilestone) in str(exc)
    assert str(int) in str(exc)


def test_runs_by_project_id_w_milestone(client):
    """ Verify calling ``client.runs(1234)`` with milestone """
    ms = models.Milestone(client, {'id': 22})
    list(client.runs(1234, milestone=ms))

    client.api.runs_by_project_id.assert_called_once_with(1234, milestone_id='22')


def test_runs_by_project_id_w_milestone_id(client):
    """ Verify calling ``client.runs(1234)`` with milestone """
    list(client.runs(1234, milestone=22))

    client.api.runs_by_project_id.assert_called_once_with(1234, milestone_id='22')


def test_runs_by_project_id_w_milestone_exc(client):
    """ Verify calling ``client.runs(1234)`` with milestone exception """
    with pytest.raises(TypeError) as exc:
        list(client.runs(1234, milestone='asdf'))

    assert 'asdf' in str(exc)
    assert str(models.Milestone) in str(exc)
    assert str(models.SubMilestone) in str(exc)
    assert str(int) in str(exc)


def test_runs_by_project_w_suite(client):
    """ Verify calling ``client.runs(Project)`` with suite """
    suite = models.Suite(client, {'id': 22})
    list(client.runs(models.Project(client, {'id': 1234}), suite=suite))

    client.api.runs_by_project_id.assert_called_once_with(1234, suite_id='22')


def test_runs_by_project_w_suite_id(client):
    """ Verify calling ``client.runs(Project)`` with suite """
    list(client.runs(models.Project(client, {'id': 1234}), suite=22))

    client.api.runs_by_project_id.assert_called_once_with(1234, suite_id='22')


def test_runs_by_project_w_suite_exc(client):
    """ Verify calling ``client.runs(Project)`` with suite exception """
    with pytest.raises(TypeError) as exc:
        list(client.runs(models.Project(client, {'id': 1234}), suite='asdf'))

    assert 'asdf' in str(exc)
    assert str(models.Suite) in str(exc)
    assert str(int) in str(exc)


def test_runs_by_project_id_w_suite(client):
    """ Verify calling ``client.runs(1234)`` with suite """
    suite = models.Suite(client, {'id': 22})
    list(client.runs(1234, suite=suite))

    client.api.runs_by_project_id.assert_called_once_with(1234, suite_id='22')


def test_runs_by_project_id_w_suite_id(client):
    """ Verify calling ``client.runs(1234)`` with suite """
    list(client.runs(1234, suite=22))

    client.api.runs_by_project_id.assert_called_once_with(1234, suite_id='22')


def test_runs_by_project_id_w_suite_exc(client):
    """ Verify calling ``client.runs(1234)`` with suite exception """
    with pytest.raises(TypeError) as exc:
        list(client.runs(1234, suite='asdf'))

    assert 'asdf' in str(exc)
    assert str(models.Suite) in str(exc)
    assert str(int) in str(exc)


def test_section(client):
    """ Verify the Client's ``section`` method returns models.Section object """
    section = client.section()

    assert isinstance(section, models.Section)
    assert section.depth is None
    assert section.description is None
    assert section.display_order is None
    assert section.name is None
    assert section.parent is None
    assert section.project is None
    assert section.suite is None


def test_section_by_id(client):
    """ Verify calling ``client.section(123)`` with an ID returns that section """
    client.api.section_by_id.return_value = {'id': 1234}
    section = client.section(1234)

    assert isinstance(section, models.Section)
    assert section.id == 1234
    client.api.section_by_id.assert_called_once_with(1234)


def test_sections_exc(client):
    """ Verify the Client's ``sections`` method throws an exception if called """
    with pytest.raises(NotImplementedError) as exc:
        client.sections()

    assert 'You must pass in models.Project or int object' in str(exc)
    assert not client.api.sections_by_project_id.called


def test_sections_by_project_id(client):
    """ Verify calling ``client.sections(123)`` with an ID returns section
        generator
    """
    PROJECT_ID = 15
    client.api.project_by_id.return_value = {'id': PROJECT_ID, 'suite_mode': 1}
    client.api.sections_by_project_id.return_value = [SECT1, SECT2, SECT3]
    sections = client.sections(PROJECT_ID)

    section1 = next(sections)
    assert isinstance(section1, models.Section)
    assert section1.id == 991

    section2 = next(sections)
    assert isinstance(section2, models.Section)
    assert section2.id == 992

    section3 = next(sections)
    assert isinstance(section3, models.Section)
    assert section3.id == 993

    client.api.project_by_id.assert_called_once_with(PROJECT_ID)
    client.api.sections_by_project_id.assert_called_once_with(PROJECT_ID, None)


def test_sections_by_project(client):
    """ Verify calling ``client.sections(Project)`` with an ID returns
        section generator
    """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 1}
    client.api.project_by_id.return_value = PROJECT_DICT
    client.api.sections_by_project_id.return_value = [SECT1, SECT2, SECT3]

    sections = client.sections(models.Project(client, PROJECT_DICT))

    section1 = next(sections)
    assert isinstance(section1, models.Section)
    assert section1.id == 991

    section2 = next(sections)
    assert isinstance(section2, models.Section)
    assert section2.id == 992

    section3 = next(sections)
    assert isinstance(section3, models.Section)
    assert section3.id == 993

    client.api.project_by_id.assert_called_once_with(PROJECT_ID)
    client.api.sections_by_project_id.assert_called_once_with(PROJECT_ID, None)


def test_sections_by_project_and_suite(client):
    """ Verify calling ``client.sections(Project, Suite)`` returns
        section generator
    """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 2}
    SUITE_ID = 16
    SUITE_DICT = {'id': SUITE_ID}

    client.api.project_by_id.return_value = PROJECT_DICT
    client.api.sections_by_project_id.return_value = [SECT1, ]

    project = models.Project(client, PROJECT_DICT)
    suite = models.Suite(client, SUITE_DICT)
    sections = client.sections(project, suite)

    section1 = next(sections)
    assert isinstance(section1, models.Section)
    assert section1.id == 991

    client.api.project_by_id.assert_called_once_with(PROJECT_ID)
    client.api.sections_by_project_id.assert_called_once_with(PROJECT_ID, SUITE_ID)


def test_sections_by_project_and_suite_id(client):
    """ Verify calling ``client.sections(Project, 15)`` returns
        section generator
    """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 2}
    SUITE_ID = 16

    client.api.project_by_id.return_value = PROJECT_DICT
    client.api.sections_by_project_id.return_value = [SECT1, ]

    project = models.Project(client, PROJECT_DICT)
    sections = client.sections(project, SUITE_ID)

    section1 = next(sections)
    assert isinstance(section1, models.Section)
    assert section1.id == 991

    client.api.project_by_id.assert_called_once_with(PROJECT_ID)
    client.api.sections_by_project_id.assert_called_once_with(PROJECT_ID, SUITE_ID)


def test_sections_by_project_exc_1(client):
    """ Verify calling ``client.sections(Project)`` when the project is a
        suite_mode of 2 raises an exception
    """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 2}

    client.api.project_by_id.return_value = PROJECT_DICT
    client.api.sections_by_project_id.return_value = [SECT1, ]

    with pytest.raises(TypeError) as exc:
        list(client.sections(models.Project(client, PROJECT_DICT)))

    assert 'suite_mode of 2' in str(exc)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)
    assert not client.api.sections_by_project_id.called


def test_sections_by_project_exc_2(client):
    """ Verify calling ``client.sections(Project, 'asdf')`` when the project
        is a suite_mode of 2 raises an exception
    """
    PROJECT_ID = 15
    PROJECT_DICT = {'id': PROJECT_ID, 'suite_mode': 2}

    client.api.project_by_id.return_value = PROJECT_DICT
    client.api.sections_by_project_id.return_value = [SECT1, ]

    with pytest.raises(TypeError) as exc:
        list(client.sections(models.Project(client, PROJECT_DICT), 'asdf'))

    assert 'models.Suite' in str(exc)
    assert 'int ID of a suite in testrail' in str(exc)
    client.api.project_by_id.assert_called_once_with(PROJECT_ID)
    assert not client.api.sections_by_project_id.called


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
    """ Verify the Client's ``suite`` method returns models.Suite object """
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


def test_template_exc(client):
    """ Verify the Client's ``template`` method throws an exception if called """
    with pytest.raises(NotImplementedError) as exc:
        client.template()

    assert 'You must pass in int object' in str(exc)
    assert not client.api.templates.called


def test_template_by_int(client):
    """ Verify the Client's ``templates`` method call with int"""
    client.api.templates.return_value = [TEMP1, TEMP2, TEMP3]

    with mock.patch.object(client, 'projects') as proj_mock:
        proj_mock.return_value = [models.Project(client, {'id': 123}), ]
        template = client.template(992)

    assert isinstance(template, models.Template)
    assert template.id == 992
    assert client.api.templates.called


def test_template_by_int_exc(client):
    """ Verify the Client's ``template`` method throws an exception if
        unmatched id
    """
    client.api.templates.return_value = [TEMP1, TEMP2, TEMP3]

    with mock.patch.object(client, 'projects') as proj_mock:
        proj_mock.return_value = [models.Project(client, {'id': 123}), ]
        with pytest.raises(TRAWClientError) as exc:
            client.template(994)

    assert 'id of 994' in str(exc)
    assert client.api.templates.called


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
    assert client.api.results_by_test_id.cache.clear.called
    assert client.api.run_by_id.cache.clear.called
    assert client.api.runs_by_project_id.cache.clear.called
    assert client.api.section_by_id.cache.clear.called
    assert client.api.sections_by_project_id.cache.clear.called
    assert client.api.statuses.cache.clear.called
    assert client.api.suite_by_id.cache.clear.called
    assert client.api.suites_by_project_id.cache.clear.called
    assert client.api.templates.cache.clear.called
    assert client.api.test_by_id.cache.clear.called
    assert client.api.tests_by_run_id.cache.clear.called
    assert client.api.user_by_email.cache.clear.called
    assert client.api.user_by_id.cache.clear.called
    assert client.api.users.cache.clear.called
