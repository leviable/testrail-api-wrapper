import os
from os import path
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

from .sessions import Session
from .exceptions import TRAWLoginError
from .const import ENVs, CONFIG_FILE_NAME, GET, API_PATH

_USER_KEY = 'username'
_PASS_KEY = 'password'
_URL_KEY = 'url'


class API(object):
    """ TRAW's interface class to TestRail's REST API

    The API class is not meant to be accessed directly, rather, use the traw.Client
    """
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

    def priorities(self):
        """ Calls `get_priorities` API endpoint

        :yields: priority dictionaries from api
        """
        path = API_PATH['get_priorities']
        for priority in self._session.request(method=GET, path=path):
            yield priority

    def project_by_id(self, project_id):
        """ Calls `get_project` API endpoint with the given project_id

        :param project_id: int id of project

        :returns: project dict
        """
        path = API_PATH['get_project'].format(project_id=project_id)
        return self._session.request(method=GET, path=path)

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

    def user_by_email(self, email):
        """ Calls `get_user` API endpoint with the given user email

        :param email: str email of user

        :returns: user dict
        """
        path = API_PATH['get_user_by_email']
        params = {'email': email}
        return self._session.request(method=GET, path=path, params=params)

    def user_by_id(self, user_id):
        """ Calls `get_user` API endpoint with the given user_id

        :param user_id: int id of user

        :returns: user dict
        """
        path = API_PATH['get_user'].format(user_id=user_id)
        return self._session.request(method=GET, path=path)

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
