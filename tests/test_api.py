import mock
import pytest

import traw
from traw.exceptions import TRAWLoginError
from traw.const import ENVs, GET, POST, API_PATH as AP

MOCK_USERNAME = 'mock username'
MOCK_USER_API_KEY = 'mock user api key'
MOCK_PASSWORD = 'mock password'
MOCK_URL = 'mock url'
CASE1 = {'case': 'case1'}
CASE2 = {'case': 'case2'}
CASE3 = {'case': 'case3'}
CG1 = {'config_group': 'config_group1'}
CG2 = {'config_group': 'config_group2'}
CG3 = {'config_group': 'config_group3'}
CONF1 = {'config': 'config1'}
CONF2 = {'config': 'config2'}
CONF3 = {'config': 'config3'}
CT1 = {'casetype': 'casetype1'}
CT2 = {'casetype': 'casetype2'}
CT3 = {'casetype': 'casetype3'}
MILE1 = {'milestone': 'milestone1'}
MILE2 = {'milestone': 'milestone2'}
MILE3 = {'milestone': 'milestone3'}
PLAN1 = {'plan': 'plan1'}
PLAN2 = {'plan': 'plan2'}
PLAN3 = {'plan': 'plan3'}
PRIO1 = {'priority': 'priority1'}
PRIO2 = {'priority': 'priority2'}
PRIO3 = {'priority': 'priority3'}
PROJ1 = {'project': 'project1'}
PROJ2 = {'project': 'project2'}
PROJ3 = {'project': 'project3'}
RUN1 = {'run': 'run1'}
RUN2 = {'run': 'run2'}
RUN3 = {'run': 'run3'}
STAT1 = {'stat': 'stat1'}
STAT2 = {'stat': 'stat2'}
STAT3 = {'stat': 'stat3'}
SUIT1 = {'suite': 'suite1'}
SUIT2 = {'suite': 'suite2'}
SUIT3 = {'suite': 'suite3'}
TEMP1 = {'temp': 'temp1'}
TEMP2 = {'temp': 'temp2'}
TEMP3 = {'temp': 'temp3'}
TEST1 = {'test': 'test1'}
TEST2 = {'test': 'test2'}
TEST3 = {'test': 'test3'}
USER1 = {'user': 'user1'}
USER2 = {'user': 'user2'}
USER3 = {'user': 'user3'}


@pytest.fixture()
def no_env_vars():
    empty_dict = dict()
    with mock.patch.dict('traw.api.os.environ', empty_dict):
        yield empty_dict


@pytest.fixture()
def env_vars():
    env_vars_dict = {ENVs.USER_KEY: MOCK_USERNAME,
                     ENVs.API_KEY: MOCK_USER_API_KEY,
                     ENVs.PASS_KEY: MOCK_PASSWORD,
                     ENVs.URL_KEY: MOCK_URL}
    with mock.patch.dict('traw.api.os.environ', env_vars_dict):
        yield env_vars_dict


@pytest.fixture()
def env_vars_no_key():
    env_vars_dict = {ENVs.USER_KEY: MOCK_USERNAME,
                     ENVs.PASS_KEY: MOCK_PASSWORD,
                     ENVs.URL_KEY: MOCK_URL}
    with mock.patch.dict('traw.api.os.environ', env_vars_dict):
        yield env_vars_dict


@pytest.fixture()
def no_path_mock():
    with mock.patch('traw.api.os.path') as path_mock:
        path_mock.exists.return_value = False
        yield path_mock


@pytest.fixture()
def config_parser_mock():
    traw_config = {'username': MOCK_USERNAME,
                   'user_api_key': MOCK_USER_API_KEY,
                   'password': MOCK_PASSWORD,
                   'url': MOCK_URL}
    cp_mock = mock.MagicMock()
    cp_mock.return_value = cp_mock
    cp_mock.read.return_value = cp_mock
    cp_mock.__getitem__.return_value = traw_config
    with mock.patch('traw.api.ConfigParser', new_callable=cp_mock):
        with mock.patch('traw.api.os.path.exists'):
            yield traw_config


@pytest.fixture()
def api():
    with mock.patch('traw.api.Session') as Session:
        Session.return_value = Session
        yield traw.api.API(username=MOCK_USERNAME,
                           user_api_key=MOCK_USER_API_KEY,
                           password=MOCK_PASSWORD,
                           url=MOCK_URL)


def test___init___with_caller_supplied_credentials(no_env_vars, no_path_mock):
    """ Verify the credentials can be set through the API init call
        Verify that the user_api_key keyword overrides the password keyword
    """
    api = traw.api.API(username=MOCK_USERNAME,
                       user_api_key=MOCK_USER_API_KEY,
                       password=MOCK_PASSWORD,
                       url=MOCK_URL)

    assert api._session._auth[0] == MOCK_USERNAME
    assert api._session._auth[1] == MOCK_USER_API_KEY
    assert api._session._auth[1] != MOCK_PASSWORD
    assert api._session._url == MOCK_URL


def test___init___with_caller_supplied_password(no_env_vars, no_path_mock):
    """ Verify a password can be used instead of the apk key """
    api = traw.api.API(username=MOCK_USERNAME,
                       password=MOCK_PASSWORD,
                       url=MOCK_URL)

    assert api._session._auth[0] == MOCK_USERNAME
    assert api._session._auth[1] != MOCK_USER_API_KEY
    assert api._session._auth[1] == MOCK_PASSWORD
    assert api._session._url == MOCK_URL


def test___init___with_env_credentials(env_vars, no_path_mock):
    """ Verify the credentials can be set through environment variables
        Verify that the user_api_key keyword overrides the password keyword
    """
    api = traw.api.API()

    assert api._session._auth[0] == MOCK_USERNAME
    assert api._session._auth[1] == MOCK_USER_API_KEY
    assert api._session._auth[1] != MOCK_PASSWORD
    assert api._session._url == MOCK_URL


def test___init___with_env_password(env_vars_no_key, no_path_mock):
    """ Verify the credentials can be set through environment variables
        Verify that the user_api_key keyword overrides the password keyword
    """
    api = traw.api.API()

    assert api._session._auth[0] == MOCK_USERNAME
    assert api._session._auth[1] != MOCK_USER_API_KEY
    assert api._session._auth[1] == MOCK_PASSWORD
    assert api._session._url == MOCK_URL


def test__env_var_exception():
    """ Verify an exception is raised if the wrong value is passed in """
    with pytest.raises(ValueError):
        traw.api._env_var('does not exist')


def test__init__with_config_file(no_env_vars, config_parser_mock):
    """ Verify the credentials can be set a configuration file
        Verify that the user_api_key keyword overrides the password keyword
    """
    api = traw.api.API()

    assert api._session._auth[0] == MOCK_USERNAME
    assert api._session._auth[1] == MOCK_USER_API_KEY
    assert api._session._auth[1] != MOCK_PASSWORD
    assert api._session._url == MOCK_URL


def test__init__with_config_file_w_password(no_env_vars, config_parser_mock):
    """ Verify the credentials can be set a configuration file
        Verify that the password keyword can be used
    """
    config_parser_mock['user_api_key'] = None
    api = traw.api.API()

    assert api._session._auth[0] == MOCK_USERNAME
    assert api._session._auth[1] != MOCK_USER_API_KEY
    assert api._session._auth[1] == MOCK_PASSWORD
    assert api._session._url == MOCK_URL


def test__init__no_credentials_exception(no_env_vars, no_path_mock):
    """ Verify that an exception is raised if no credentials are set """
    with pytest.raises(TRAWLoginError):
        traw.api.API()


def test_case_by_id(api):
    """ Verify the ``case_by_id`` method call """
    CASE_ID = 1234
    api._session.request.return_value = CASE1
    case = api.case_by_id(CASE_ID)

    exp_call = mock.call(method=GET, path=AP['get_case'].format(case_id=CASE_ID))

    assert case == CASE1
    assert isinstance(case, dict)
    assert api._session.request.call_args == exp_call


def test_case_types(api):
    """ Verify the ``case_types`` method call """
    api._session.request.return_value = [CT1, CT2, CT3]
    ct_list = list(api.case_types())

    exp_call = mock.call(method=GET, path=AP['get_case_types'])

    assert all(map(lambda c: isinstance(c, dict), ct_list))
    assert len(ct_list) == 3
    assert api._session.request.call_args == exp_call


def test_config_add(api):
    """ Verify the ``config_add`` method call """
    CONFIG_GROUP_ID = 15
    PARAMS = {'param_key': 'param_value'}
    api._session.request.return_value = CONF1
    config = api.config_add(CONFIG_GROUP_ID, params=PARAMS)

    exp_call = mock.call(method=POST,
                         path=AP['add_config'].format(config_group_id=CONFIG_GROUP_ID),
                         json=PARAMS)

    assert config == CONF1
    assert isinstance(config, dict)
    assert api._session.request.call_args == exp_call


def test_config_delete(api):
    """ Verify the ``config_delete`` method call """
    CONFIG_ID = 15
    api._session.request.return_value = {}
    config = api.config_delete(CONFIG_ID)

    exp_call = mock.call(method=POST,
                         path=AP['delete_config'].format(config_id=CONFIG_ID))

    assert isinstance(config, dict)
    assert config == dict()
    assert api._session.request.call_args == exp_call


def test_config_update(api):
    """ Verify the ``config_update`` method call """
    CONFIG_ID = 15
    PARAMS = {'param_key': 'param_value'}
    api._session.request.return_value = CONF1
    config = api.config_update(CONFIG_ID, PARAMS)

    exp_call = mock.call(method=POST,
                         path=AP['update_config'].format(config_id=CONFIG_ID),
                         json=PARAMS)

    assert config == CONF1
    assert isinstance(config, dict)
    assert api._session.request.call_args == exp_call


def test_config_group_add(api):
    """ Verify the ``config_group_add`` method call """
    PROJECT_ID = 15
    PARAMS = {'param_key': 'param_value'}
    api._session.request.return_value = CG1
    con_grp = api.config_group_add(PROJECT_ID, params=PARAMS)

    exp_call = mock.call(method=POST,
                         path=AP['add_config_group'].format(project_id=PROJECT_ID),
                         json=PARAMS)

    assert con_grp == CG1
    assert isinstance(con_grp, dict)
    assert api._session.request.call_args == exp_call


def test_config_group_delete(api):
    """ Verify the ``config_group_delete`` method call """
    CONFIG_GROUP_ID = 15
    api._session.request.return_value = {}
    con_grp = api.config_group_delete(CONFIG_GROUP_ID)

    exp_call = mock.call(method=POST,
                         path=AP['delete_config_group'].format(config_group_id=CONFIG_GROUP_ID))

    assert isinstance(con_grp, dict)
    assert con_grp == dict()
    assert api._session.request.call_args == exp_call


def test_config_group_update(api):
    """ Verify the ``config_group_update`` method call """
    CONFIG_GROUP_ID = 15
    PARAMS = {'param_key': 'param_value'}
    api._session.request.return_value = CG1
    con_grp = api.config_group_update(CONFIG_GROUP_ID, PARAMS)

    exp_call = mock.call(method=POST,
                         path=AP['update_config_group'].format(config_group_id=CONFIG_GROUP_ID),
                         json=PARAMS)

    assert con_grp == CG1
    assert isinstance(con_grp, dict)
    assert api._session.request.call_args == exp_call


def test_config_groups(api):
    """ Verify the ``config_groups`` method call """
    PROJECT_ID = 15
    api._session.request.return_value = [CG1, CG2, CG3]
    cg_list = list(api.config_groups(PROJECT_ID))

    exp_call = mock.call(method=GET, path=AP['get_configs'].format(project_id=PROJECT_ID))

    assert all(map(lambda c: isinstance(c, dict), cg_list))
    assert len(cg_list) == 3
    assert api._session.request.call_args == exp_call


def test_milestone_add(api):
    """ Verify the ``milestone_add`` method call """
    PROJECT_ID = 15
    PARAMS = {'param_key': 'param_value'}
    api._session.request.return_value = MILE1
    milestone = api.milestone_add(PROJECT_ID, PARAMS)

    exp_call = mock.call(method=POST,
                         path=AP['add_milestone'].format(project_id=PROJECT_ID),
                         json=PARAMS)

    assert milestone == MILE1
    assert isinstance(milestone, dict)
    assert api._session.request.call_args == exp_call


def test_milestone_delete(api):
    """ Verify the ``milestone_delete`` method call """
    MILESTONE_ID = 1234
    api._session.request.return_value = {}
    milestone = api.milestone_delete(MILESTONE_ID)

    exp_call = mock.call(method=POST,
                         path=AP['delete_milestone'].format(milestone_id=MILESTONE_ID))

    assert isinstance(milestone, dict)
    assert milestone == dict()
    assert api._session.request.call_args == exp_call


def test_milestone_update(api):
    """ Verify the ``milestone_update`` method call """
    MILESTONE_ID = 1234
    PARAMS = {'param_key': 'param_value'}
    api._session.request.return_value = MILE1
    milestone = api.milestone_update(MILESTONE_ID, PARAMS)

    exp_call = mock.call(method=POST,
                         path=AP['update_milestone'].format(milestone_id=MILESTONE_ID),
                         json=PARAMS)

    assert milestone == MILE1
    assert isinstance(milestone, dict)
    assert api._session.request.call_args == exp_call


def test_milestone_by_id(api):
    """ Verify the ``milestone_by_id`` method call """
    MILESTONE_ID = 1234
    api._session.request.return_value = MILE1
    milestone = api.milestone_by_id(MILESTONE_ID)

    exp_call = mock.call(method=GET,
                         path=AP['get_milestone'].format(milestone_id=MILESTONE_ID))

    assert milestone == MILE1
    assert isinstance(milestone, dict)
    assert api._session.request.call_args == exp_call


def test_milestones_w_defaults(api):
    """ Verify the ``milestones`` method call """
    PROJECT_ID = 15
    api._session.request.return_value = [MILE1, MILE2, MILE3]
    mile_list = list(api.milestones(PROJECT_ID))

    exp_call = mock.call(method=GET,
                         path=AP['get_milestones'].format(project_id=PROJECT_ID),
                         params=None)

    assert all(map(lambda m: isinstance(m, dict), mile_list))
    assert len(mile_list) == 3
    assert api._session.request.call_args == exp_call


def test_milestones_w_params(api):
    """ Verify the ``milestones`` method call with parameters """
    PROJECT_ID = 15
    api._session.request.return_value = [MILE1, MILE2, MILE3]
    mile_list = list(api.milestones(PROJECT_ID, True, False))

    exp_call = mock.call(method=GET,
                         path=AP['get_milestones'].format(project_id=PROJECT_ID),
                         params={'is_completed': 1, 'is_started': 0})

    assert all(map(lambda m: isinstance(m, dict), mile_list))
    assert len(mile_list) == 3
    assert api._session.request.call_args == exp_call


def test_plan_by_id(api):
    """ Verify the ``plan_by_id`` method call """
    PLAN_ID = 1234
    api._session.request.return_value = PLAN1
    plan = api.plan_by_id(PLAN_ID)

    exp_call = mock.call(method=GET, path=AP['get_plan'].format(plan_id=PLAN_ID))

    assert plan == PLAN1
    assert isinstance(plan, dict)
    assert api._session.request.call_args == exp_call


def test_priorities(api):
    """ Verify the ``priorities`` method call """
    api._session.request.return_value = [PRIO1, PRIO2, PRIO3]
    prio_list = list(api.priorities())

    exp_call = mock.call(method=GET, path=AP['get_priorities'])

    assert all(map(lambda p: isinstance(p, dict), prio_list))
    assert len(prio_list) == 3
    assert api._session.request.call_args == exp_call


def test_project_add(api):
    """ Verify the ``project_add`` method call """
    PARAMS = {'param_key': 'param_value'}
    api._session.request.return_value = PROJ1
    project = api.project_add(PARAMS)

    exp_call = mock.call(method=POST,
                         path=AP['add_project'],
                         json=PARAMS)

    assert project == PROJ1
    assert isinstance(project, dict)
    assert api._session.request.call_args == exp_call


def test_project_by_id(api):
    """ Verify the project_by_id method can be called """
    PROJ_ID = 1234
    PROJ_DICT = {'proj': 'proj_info'}

    api._session.request.return_value = PROJ_DICT

    proj = api.project_by_id(PROJ_ID)

    assert proj is PROJ_DICT
    assert str(PROJ_ID) in str(api._session.request.call_args)


def test_project_delete(api):
    """ Verify the ``project_delete`` method call """
    PROJECT_ID = 15
    api._session.request.return_value = {}
    project = api.project_delete(PROJECT_ID)

    exp_call = mock.call(method=POST,
                         path=AP['delete_project'].format(project_id=PROJECT_ID))

    assert isinstance(project, dict)
    assert project == dict()
    assert api._session.request.call_args == exp_call


def test_project_update(api):
    """ Verify the ``project_update`` method call """
    PROJECT_ID = 15
    PARAMS = {'param_key': 'param_value'}
    api._session.request.return_value = PROJ1
    project = api.project_update(PROJECT_ID, PARAMS)

    exp_call = mock.call(method=POST,
                         path=AP['update_project'].format(project_id=PROJECT_ID),
                         json=PARAMS)

    assert project == PROJ1
    assert isinstance(project, dict)
    assert api._session.request.call_args == exp_call


def test_projects_no_arg(api):
    """ Verify the ``projects`` method call with no args """
    api._session.request.return_value = [PROJ1, PROJ2, PROJ3]
    proj_list = list(api.projects())

    exp_call = mock.call(method=GET, params=None, path=AP['get_projects'])

    assert all(map(lambda p: isinstance(p, dict), proj_list))
    assert len(proj_list) == 3
    assert api._session.request.call_args == exp_call


def test_projects_with_arg(api):
    """ Verify the ``projects`` method call with an arg """
    api._session.request.return_value = [PROJ1, PROJ2, PROJ3]
    ARG1 = 'arg1'
    proj_list = list(api.projects(ARG1))

    exp_call = mock.call(
        method=GET, params={'is_completed': ARG1}, path=AP['get_projects'])

    assert all(map(lambda p: isinstance(p, dict), proj_list))
    assert len(proj_list) == 3
    assert api._session.request.call_args == exp_call


def test_run_add(api):
    """ Verify the ``run_add`` method call """
    PROJECT_ID = 15
    PARAMS = {'param_key': 'param_value'}
    api._session.request.return_value = RUN1
    run = api.run_add(PROJECT_ID, PARAMS)

    exp_call = mock.call(method=POST,
                         path=AP['add_run'].format(project_id=PROJECT_ID),
                         json=PARAMS)

    assert run == RUN1
    assert isinstance(run, dict)
    assert api._session.request.call_args == exp_call


def test_run_by_id(api):
    """ Verify the ``run_by_id`` method call """
    RUN_ID = 1234
    api._session.request.return_value = RUN1
    run = api.run_by_id(RUN_ID)

    exp_call = mock.call(method=GET, path=AP['get_run'].format(run_id=RUN_ID))

    assert run == RUN1
    assert isinstance(run, dict)
    assert api._session.request.call_args == exp_call


def test_run_close(api):
    """ Verify the ``run_close`` method call """
    RUN_ID = 1234
    api._session.request.return_value = RUN1
    run = api.run_close(RUN_ID)

    exp_call = mock.call(method=POST,
                         path=AP['close_run'].format(run_id=RUN_ID))

    assert run == RUN1
    assert isinstance(run, dict)
    assert api._session.request.call_args == exp_call


def test_run_delete(api):
    """ Verify the ``milestone_delete`` method call """
    RUN_ID = 1234
    api._session.request.return_value = {}
    run = api.run_delete(RUN_ID)

    exp_call = mock.call(method=POST, path=AP['delete_run'].format(run_id=RUN_ID))

    assert isinstance(run, dict)
    assert run == dict()
    assert api._session.request.call_args == exp_call


def test_run_update(api):
    """ Verify the ``run_update`` method call """
    RUN_ID = 1234
    PARAMS = {'param_key': 'param_value'}
    api._session.request.return_value = RUN1
    run = api.run_update(RUN_ID, PARAMS)

    exp_call = mock.call(method=POST,
                         path=AP['update_run'].format(run_id=RUN_ID),
                         json=PARAMS)

    assert run == RUN1
    assert isinstance(run, dict)
    assert api._session.request.call_args == exp_call


def test_statuses(api):
    """ Verify the ``statuses`` method call """
    api._session.request.return_value = [STAT1, STAT2, STAT3]
    stat_list = list(api.statuses())

    exp_call = mock.call(method=GET, path=AP['get_statuses'])

    assert all(map(lambda s: isinstance(s, dict), stat_list))
    assert len(stat_list) == 3
    assert api._session.request.call_args == exp_call


def test_suite_add(api):
    """ Verify the ``suite_add`` method call """
    PROJECT_ID = 15
    PARAMS = {'param_key': 'param_value'}
    api._session.request.return_value = SUIT1
    suite = api.suite_add(PROJECT_ID, PARAMS)

    exp_call = mock.call(method=POST,
                         path=AP['add_suite'].format(project_id=PROJECT_ID),
                         json=PARAMS)

    assert suite == SUIT1
    assert isinstance(suite, dict)
    assert api._session.request.call_args == exp_call


def test_suite_by_id(api):
    """ Verify the ``suite_by_id`` method call """
    SUITE_ID = 1234
    api._session.request.return_value = SUIT1
    suite = api.suite_by_id(SUITE_ID)

    exp_call = mock.call(method=GET, path=AP['get_suite'].format(suite_id=SUITE_ID))

    assert suite == SUIT1
    assert isinstance(suite, dict)
    assert api._session.request.call_args == exp_call


def test_suites_by_project_id(api):
    """ Verify the ``suites_by_project_id`` method call """
    PROJECT_ID = 1234
    api._session.request.return_value = [SUIT1, SUIT2]

    suite = next(api.suites_by_project_id(PROJECT_ID))

    exp_call = mock.call(method=GET, path=AP['get_suites'].format(project_id=PROJECT_ID))

    assert suite == SUIT1
    assert isinstance(suite, dict)
    assert api._session.request.call_args == exp_call


def test_suite_delete(api):
    """ Verify the ``suite_delete`` method call """
    SUITE_ID = 1234
    api._session.request.return_value = {}
    suite = api.suite_delete(SUITE_ID)

    exp_call = mock.call(method=POST,
                         path=AP['delete_suite'].format(suite_id=SUITE_ID))

    assert isinstance(suite, dict)
    assert suite == dict()
    assert api._session.request.call_args == exp_call


def test_suite_update(api):
    """ Verify the ``suite_update`` method call """
    SUITE_ID = 1234
    PARAMS = {'param_key': 'param_value'}
    api._session.request.return_value = SUIT1
    suite = api.suite_update(SUITE_ID, PARAMS)

    exp_call = mock.call(method=POST,
                         path=AP['update_suite'].format(suite_id=SUITE_ID),
                         json=PARAMS)

    assert suite == SUIT1
    assert isinstance(suite, dict)
    assert api._session.request.call_args == exp_call


def test_templates(api):
    """ Verify the ``templates`` method call """
    PROJECT_ID = 15
    api._session.request.return_value = [TEMP1, TEMP2, TEMP3]
    temp_list = list(api.templates(PROJECT_ID))

    exp_call = mock.call(method=GET, path=AP['get_templates'].format(project_id=PROJECT_ID))

    assert all(map(lambda t: isinstance(t, dict), temp_list))
    assert len(temp_list) == 3
    assert api._session.request.call_args == exp_call


def test_test_by_id(api):
    """ Verify the ``test_by_id`` method call """
    TEST_ID = 1234
    api._session.request.return_value = TEST1
    test = api.test_by_id(TEST_ID)

    exp_call = mock.call(method=GET, path=AP['get_test'].format(test_id=TEST_ID))

    assert test == TEST1
    assert isinstance(test, dict)
    assert api._session.request.call_args == exp_call


def test_tests_by_run_id_no_status_id(api):
    """ Verify the ``tests_by_run_id`` method call with no status_id"""
    RUN_ID = 1234
    api._session.request.return_value = [TEST1, TEST2]

    test = next(api.tests_by_run_id(RUN_ID))

    exp_call = mock.call(
        method=GET, path=AP['get_tests'].format(run_id=RUN_ID), params=None)

    assert test == TEST1
    assert isinstance(test, dict)
    assert api._session.request.call_args == exp_call


def test_tests_by_run_id_w_status_id(api):
    """ Verify the ``tests_by_run_id`` method call with status_id"""
    RUN_ID = 1234
    api._session.request.return_value = [TEST1, TEST2]

    test = next(api.tests_by_run_id(RUN_ID, "111,222"))

    exp_call = mock.call(method=GET,
                         path=AP['get_tests'].format(run_id=RUN_ID),
                         params={'status_id': '111,222'})

    assert test == TEST1
    assert isinstance(test, dict)
    assert api._session.request.call_args == exp_call


def test_user_by_email(api):
    """ Verify the user_by_email method can be called """
    USER_EMAIL = 'mock.user@mock.com'
    USER_DICT = {'email': USER_EMAIL}

    api._session.request.return_value = USER_DICT

    user = api.user_by_email(USER_EMAIL)

    assert user is USER_DICT
    assert USER_EMAIL in str(api._session.request.call_args)


def test_user_by_id(api):
    """ Verify the user_by_id method can be called """
    USER_ID = 1234
    USER_DICT = {'id': USER_ID}

    api._session.request.return_value = USER_DICT

    user = api.user_by_id(USER_ID)

    assert user is USER_DICT
    assert str(USER_ID) in str(api._session.request.call_args)


def test_users(api):
    """ Verify the ``users`` method call """
    api._session.request.return_value = [USER1, USER2, USER3]
    user_list = list(api.users())

    exp_call = mock.call(method=GET, path=AP['get_users'])

    assert all(map(lambda u: isinstance(u, dict), user_list))
    assert len(user_list) == 3
    assert api._session.request.call_args == exp_call
