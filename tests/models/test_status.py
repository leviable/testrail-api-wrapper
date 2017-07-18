from copy import deepcopy

import pytest

from traw.models import Status

COLOR_BRIGHT = 16631751
COLOR_DARK = 14250867
COLOR_MEDIUM = 15829135
ID = 1234
LABEL = "Failed"
NAME = 'mock status name'


@pytest.fixture()
def status(client):
    content = {"color_bright": COLOR_BRIGHT,
               "color_dark": COLOR_DARK,
               "color_medium": COLOR_MEDIUM,
               "id": ID,
               "is_final": False,
               "is_system": True,
               "is_untested": False,
               "label": LABEL,
               "name": NAME}
    return Status(client, deepcopy(content))


def test_color_bright(status):
    assert status.color_bright == COLOR_BRIGHT


def test_color_dark(status):
    assert status.color_dark == COLOR_DARK


def test_color_medium(status):
    assert status.color_medium == COLOR_MEDIUM


def test_id(status):
    assert status.id == ID


def test_is_final(status):
    assert status.is_final is False


def test_is_system(status):
    assert status.is_system is True


def test_is_untested(status):
    assert status.is_untested is False


def test_label(status):
    assert status.label == LABEL


def test_name(status):
    assert status.name == NAME
