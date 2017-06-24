import os
from os import path
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

from .const import ENVs, CONFIG_FILE_NAME
from .exceptions import TRAWLoginError

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
        self.username = username or _env_var(_USER_KEY) or config[_USER_KEY]
        self.password = user_api_key or password or _env_var(_PASS_KEY) or config[_PASS_KEY]
        self.url = url or _env_var(_URL_KEY) or config[_URL_KEY]

        if self.username is None or self.password is None or self.url is None:
            msg = ('You must set a username, password/api_key, and url to '
                   'use TRAW')
            raise TRAWLoginError(msg)


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
