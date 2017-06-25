import pytest

import traw

USER = 'mock username'
PASS = 'mock password'
URL = 'mock url'


@pytest.fixture()
def client():
    return traw.Client(username=USER, password=PASS, url=URL)


def test___init__():
    client = traw.Client(username=USER, password=PASS, url=URL)
    assert hasattr(client, '_api')
    assert isinstance(client._api, traw.api.API)


def test_client_add_exception(client):
    with pytest.raises(TypeError):
        client.add()


def test_client_close_exception(client):
    with pytest.raises(TypeError):
        client.close()


def test_client_delete_exception(client):
    with pytest.raises(TypeError):
        client.delete()


def test_client_update_exception(client):
    with pytest.raises(TypeError):
        client.update()
