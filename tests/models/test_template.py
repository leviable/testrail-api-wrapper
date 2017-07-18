from copy import deepcopy

import pytest

from traw.models import Template

ID = 1234
NAME = 'mock template name'


@pytest.fixture()
def template(client):
    content = {"id": ID,
               "is_default": True,
               "name": NAME}
    return Template(client, deepcopy(content))


def test_id(template):
    assert template.id == ID


def test_is_default(template):
    assert template.is_default is True


def test_name(template):
    assert template.name == NAME
