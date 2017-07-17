from copy import deepcopy
import pytest

from traw.models import CaseType

ID = 1234
NAME = 'mock case type name'


@pytest.fixture()
def case_type(client):
    content = {"id": ID,
               "is_default": True,
               "name": NAME}
    return CaseType(client, deepcopy(content))


def test_id(case_type):
    assert case_type.id == ID


def test_is_default(case_type):
    assert case_type.is_default is True


def test_name(case_type):
    assert case_type.name == NAME
