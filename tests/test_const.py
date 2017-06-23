from traw.const import API_PATH, BASE_API_PATH


def test_api_path():
    assert isinstance(API_PATH, dict)


def test_base_api_path():
    assert isinstance(BASE_API_PATH, str)
