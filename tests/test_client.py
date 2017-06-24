import traw


def test___init__():
    client = traw.Client(username="mock username", password="mock password", url="mock_url")
    assert hasattr(client, '_api')
    assert isinstance(client._api, traw.api.API)
