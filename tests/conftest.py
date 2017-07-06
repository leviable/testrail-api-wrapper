import time

import mock
import pytest

import traw

USER = 'mock username'
PASS = 'mock password'
URL = 'mock url'


# Prevent calls to sleep
class SleepMock(object):
    def __init__(self):
        self.mock_obj = mock.MagicMock()

    def __call__(self, *args):
        self.mock_obj(*args)


time.sleep = SleepMock()


@pytest.fixture()
def client():
    with mock.patch('traw.client.API') as api_mock:
        api_mock.return_value = api_mock

        yield traw.Client(username=USER, password=PASS, url=URL)
