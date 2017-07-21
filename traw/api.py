import os
from os import path
from collections import defaultdict
try:
    from ConfigParser import ConfigParser  # pragma: no cover
except ImportError:  # pragma: no cover
    from configparser import ConfigParser  # pragma: no cover

from .const import API_PATH, CONFIG_FILE_NAME, DEFAULT_CACHE_TIMEOUT, ENVs, GET, POST
from .exceptions import TRAWLoginError
from . import models
from .sessions import Session
from .utils import cacheable, cacheable_generator, clear_cache

_USER_KEY = 'username'
_PASS_KEY = 'password'
_URL_KEY = 'url'


class API(object):
    """ TRAW's interface class to TestRail's REST API

    The API class is not meant to be accessed directly, rather, use the traw.Client
    """
    cache_timeouts = defaultdict(lambda: defaultdict(lambda: DEFAULT_CACHE_TIMEOUT))

    def __init__(self, username=None, user_api_key=None, password=None, url=None):
        """
        """
        config = _load_config()
        _username = username or _env_var(_USER_KEY) or config[_USER_KEY]
        _password = user_api_key or password or _env_var(_PASS_KEY) or config[_PASS_KEY]
        _url = url or _env_var(_URL_KEY) or config[_URL_KEY]

        if _username is None or _password is None or _url is None:
            msg = ('You must set a username, password/api_key, and url to '
                   'use TRAW')
            raise TRAWLoginError(msg)

        self._session = Session(auth=(_username, _password), url=_url)

    @cacheable(models.Case)
    def case_by_id(self, case_id):
        """ Calls `get_case` API endpoint with the given case_id

        :param case_id: int id of case

        :returns: case dict
        """
        path = API_PATH['get_case'].format(case_id=case_id)
        return self._session.request(method=GET, path=path)

    @cacheable_generator(models.CaseType)
    def case_types(self):
        """ Calls `get_case_types` API endpoint

        :yields: case_type dictionaries from api
        """
        path = API_PATH['get_case_types']
        for case_type in self._session.request(method=GET, path=path):
            yield case_type

    @cacheable_generator(models.ConfigGroup)
    def config_groups(self, project_id):
        """ Calls `get_configs` API endpoint

        :yields: config_group dictionaries from api
        """
        path = API_PATH['get_configs'].format(project_id=project_id)

        for config_group in self._session.request(method=GET, path=path):
            yield config_group

    @clear_cache(config_groups)
    def config_add(self, config_group_id, params):
        path = API_PATH['add_config'].format(config_group_id=config_group_id)
        return self._session.request(method=POST, path=path, json=params)

    @clear_cache(config_groups)
    def config_delete(self, config_id):
        path = API_PATH['delete_config'].format(config_id=config_id)
        return self._session.request(method=POST, path=path)

    @clear_cache(config_groups)
    def config_update(self, config_id, params):
        path = API_PATH['update_config'].format(config_id=config_id)
        return self._session.request(method=POST, path=path, json=params)

    @clear_cache(config_groups)
    def config_group_add(self, project_id, params):
        path = API_PATH['add_config_group'].format(project_id=project_id)
        return self._session.request(method=POST, path=path, json=params)

    @clear_cache(config_groups)
    def config_group_delete(self, config_group_id):
        path = API_PATH['delete_config_group'].format(config_group_id=config_group_id)
        return self._session.request(method=POST, path=path)

    @clear_cache(config_groups)
    def config_group_update(self, config_group_id, params):
        path = API_PATH['update_config_group'].format(config_group_id=config_group_id)
        return self._session.request(method=POST, path=path, json=params)

    @cacheable(models.Milestone)
    def milestone_by_id(self, milestone_id):
        """ Calls `get_milestone` API endpoint with the given milestone_id

        :param milestone_id: int id of milestone

        :returns: milestone dict
        """
        path = API_PATH['get_milestone'].format(milestone_id=milestone_id)
        return self._session.request(method=GET, path=path)

    @cacheable_generator(models.Milestone)
    def milestones(self, project_id, is_completed=None, is_started=None):
        """ Calls `get_milestones` API endpoint

        :yields: milestone dictionaries from api
        """
        is_comp = int(is_completed) if is_completed is not None else None
        is_star = int(is_started) if is_started is not None else None

        path = API_PATH['get_milestones'].format(project_id=project_id)

        params = dict()
        if is_completed is not None:
            params['is_completed'] = is_comp

        if is_started is not None:
            params['is_started'] = is_star

        params = params or None

        for milestone in self._session.request(method=GET, path=path, params=params):
            yield milestone

    @clear_cache(milestones)
    @clear_cache(milestone_by_id)
    def milestone_add(self, project_id, params):
        path = API_PATH['add_milestone'].format(project_id=project_id)
        return self._session.request(method=POST, path=path, json=params)

    @clear_cache(milestones)
    @clear_cache(milestone_by_id)
    def milestone_delete(self, milestone_id):
        path = API_PATH['delete_milestone'].format(milestone_id=milestone_id)
        return self._session.request(method=POST, path=path)

    @clear_cache(milestones)
    @clear_cache(milestone_by_id)
    def milestone_update(self, milestone_id, params):
        path = API_PATH['update_milestone'].format(milestone_id=milestone_id)
        return self._session.request(method=POST, path=path, json=params)

    @cacheable(models.Plan)
    def plan_by_id(self, plan_id):
        """ Calls `get_plan` API endpoint with the given plan_id

        :param plan_id: int id of plan

        :returns: plan dict
        """
        path = API_PATH['get_plan'].format(plan_id=plan_id)
        return self._session.request(method=GET, path=path)

    @cacheable_generator(models.Priority)
    def priorities(self):
        """ Calls `get_priorities` API endpoint

        :yields: priority dictionaries from api
        """
        path = API_PATH['get_priorities']
        for priority in self._session.request(method=GET, path=path):
            yield priority

    @cacheable(models.Project)
    def project_by_id(self, project_id):
        """ Calls `get_project` API endpoint with the given project_id

        :param project_id: int id of project

        :returns: project dict
        """
        path = API_PATH['get_project'].format(project_id=project_id)
        return self._session.request(method=GET, path=path)

    @cacheable_generator(models.Project)
    def projects(self, is_completed=None):
        """ Calls `projects` API endpoint with given filter

        :param project_filter: Filter results by completion status: 0, 1, or None

        :yields: project dictionaries from api
        """
        path = API_PATH['get_projects']
        if is_completed is not None:
            params = dict(is_completed=is_completed)
        else:
            params = None

        for project in self._session.request(method=GET, path=path, params=params):
            yield project

    @clear_cache(projects)
    @clear_cache(project_by_id)
    def project_add(self, params):
        path = API_PATH['add_project']
        return self._session.request(method=POST, path=path, json=params)

    @clear_cache(projects)
    @clear_cache(project_by_id)
    def project_delete(self, project_id):
        path = API_PATH['delete_project'].format(project_id=project_id)
        return self._session.request(method=POST, path=path)

    @clear_cache(projects)
    @clear_cache(project_by_id)
    def project_update(self, project_id, params):
        path = API_PATH['update_project'].format(project_id=project_id)
        return self._session.request(method=POST, path=path, json=params)

    @cacheable(models.Run)
    def run_by_id(self, run_id):
        """ Calls `get_run` API endpoint with the given run_id

        :param run_id: int id of run

        :returns: run dict
        """
        path = API_PATH['get_run'].format(run_id=run_id)
        return self._session.request(method=GET, path=path)

    @clear_cache(run_by_id)
    def run_add(self, project_id, params):
        path = API_PATH['add_run'].format(project_id=project_id)
        return self._session.request(method=POST, path=path, json=params)

    @clear_cache(run_by_id)
    def run_close(self, run_id):
        path = API_PATH['close_run'].format(run_id=run_id)
        return self._session.request(method=POST, path=path)

    @clear_cache(run_by_id)
    def run_delete(self, run_id):
        path = API_PATH['delete_run'].format(run_id=run_id)
        return self._session.request(method=POST, path=path)

    @clear_cache(run_by_id)
    def run_update(self, run_id, params):
        path = API_PATH['update_run'].format(run_id=run_id)
        return self._session.request(method=POST, path=path, json=params)

    @cacheable_generator(models.Status)
    def statuses(self):
        """ Calls `get_statuses` API endpoint

        :yields: status dictionaries from api
        """
        path = API_PATH['get_statuses']
        for status in self._session.request(method=GET, path=path):
            yield status

    @cacheable(models.Suite)
    def suite_by_id(self, suite_id):
        """ Calls `get_suite` API endpoint with the given suite_id

        :param suite_id: int id of suite

        :returns: suite dict
        """
        path = API_PATH['get_suite'].format(suite_id=suite_id)
        return self._session.request(method=GET, path=path)

    @cacheable_generator(models.Suite)
    def suites_by_project_id(self, project_id):
        """ Calls `get_suites` API endpoint

        :yields: suite dictionaries from api
        """
        path = API_PATH['get_suites'].format(project_id=project_id)
        for suite in self._session.request(method=GET, path=path):
            yield suite

    @clear_cache(suite_by_id)
    @clear_cache(suites_by_project_id)
    def suite_add(self, project_id, params):
        path = API_PATH['add_suite'].format(project_id=project_id)
        return self._session.request(method=POST, path=path, json=params)

    @clear_cache(suite_by_id)
    @clear_cache(suites_by_project_id)
    def suite_delete(self, suite_id):
        path = API_PATH['delete_suite'].format(suite_id=suite_id)
        return self._session.request(method=POST, path=path)

    @clear_cache(suite_by_id)
    @clear_cache(suites_by_project_id)
    def suite_update(self, suite_id, params):
        path = API_PATH['update_suite'].format(suite_id=suite_id)
        return self._session.request(method=POST, path=path, json=params)

    @cacheable_generator(models.Template)
    def templates(self, project_id):
        """ Calls `get_templates` API endpoint

        :yields: template dictionaries from api
        """
        path = API_PATH['get_templates'].format(project_id=project_id)
        for template in self._session.request(method=GET, path=path):
            yield template

    @cacheable(models.Test)
    def test_by_id(self, test_id):
        """ Calls `get_test` API endpoint with the given test_id

        :param test_id: int id of test

        :returns: test dict
        """
        path = API_PATH['get_test'].format(test_id=test_id)
        return self._session.request(method=GET, path=path)

    @cacheable_generator(models.Test)
    def tests_by_run_id(self, run_id, status_id=None):
        """ Calls `get_tests` API endpoint

        :yields: test dictionaries from api
        """
        path = API_PATH['get_tests'].format(run_id=run_id)
        params = {'status_id': status_id} if status_id else None
        for test in self._session.request(method=GET, path=path, params=params):
            yield test

    @cacheable(models.User)
    def user_by_email(self, email):
        """ Calls `get_user` API endpoint with the given user email

        :param email: str email of user

        :returns: user dict
        """
        path = API_PATH['get_user_by_email']
        params = {'email': email}
        return self._session.request(method=GET, path=path, params=params)

    @cacheable(models.User)
    def user_by_id(self, user_id):
        """ Calls `get_user` API endpoint with the given user_id

        :param user_id: int id of user

        :returns: user dict
        """
        path = API_PATH['get_user'].format(user_id=user_id)
        return self._session.request(method=GET, path=path)

    @cacheable_generator(models.User)
    def users(self):
        """ Calls `users` API endpoint

        :yields: user dictionaries from api
        """
        path = API_PATH['get_users']
        for user in self._session.request(method=GET, path=path):
            yield user


def _env_var(var_name):
    """ Load the target environment variable, if it exists

    :param var_name: Name of the environment variable to load

    :returns: string if the env var exists, None if it does not
    """
    var = None

    if var_name == _USER_KEY:
        var = os.environ.get(ENVs.USER_KEY, None)
    elif var_name == _PASS_KEY:
        var = os.environ.get(ENVs.API_KEY, None) or os.environ.get(ENVs.PASS_KEY, None)
    elif var_name == _URL_KEY:
        var = os.environ.get(ENVs.URL_KEY, None)
    else:
        msg = "'var_name' must be {0}, {1}, or {2}"
        raise ValueError(msg.format(_USER_KEY, _PASS_KEY, _URL_KEY))

    return var


def _load_config():
    """ Load the configuration file, if it exists

    :returns: dict
    """
    config_dict = {_USER_KEY: None, _PASS_KEY: None, _URL_KEY: None}

    conf_file_path = path.expanduser(path.join('~', CONFIG_FILE_NAME))
    if path.exists(conf_file_path):
        config_parser = ConfigParser()
        config_parser.read(conf_file_path)
        t_conf = config_parser['TRAW']

        config_dict[_USER_KEY] = t_conf.get('username', None)
        config_dict[_PASS_KEY] = t_conf.get('user_api_key', None) or t_conf.get('password', None)
        config_dict[_URL_KEY] = t_conf.get('url', None)

    return config_dict
