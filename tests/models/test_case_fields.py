import pytest

from traw.models import CaseField
from traw.models.case_field import Config, Context, Options

DESCRIPTION = "mock case field description"
DISPLAY_ORDER = 1
ID = 1234
LABEL = "mock label text"
NAME = 'mock name'
SYSTEM_NAME = 'mock system name'
TYPE_ID = 5

CONFIG_ID = "789624d5-d92b-4f95-9779-3edfd4963679"
PROJECT_IDS = [12, 34, 56]


@pytest.fixture()
def OPTIONS():
    return {"default_value": "1",
            "is_required": True}


@pytest.fixture()
def CONTEXT():
    return {"is_global": False,
            "project_ids": PROJECT_IDS}


@pytest.fixture()
def CONFIG(CONTEXT, OPTIONS):
    return {"context": CONTEXT,
            "id": CONFIG_ID,
            "options": OPTIONS}


@pytest.fixture()
def case_field(client, CONFIG):
    content = {"configs": [CONFIG],
               "description": DESCRIPTION,
               "display_order": DISPLAY_ORDER,
               "id": ID,
               "label": LABEL,
               "name": NAME,
               "system_name": SYSTEM_NAME,
               "type_id": TYPE_ID}
    return CaseField(client, content)


def test_case_field_config(case_field):
    assert isinstance(case_field.configs[0], Config)
    assert isinstance(case_field.configs[0].context, Context)
    assert case_field.configs[0].id == CONFIG_ID
    assert isinstance(case_field.configs[0].options, Options)


def test_case_field_config_context(case_field):
    assert case_field.configs[0].context.is_global is False
    assert case_field.configs[0].context.project_ids == PROJECT_IDS


def test_case_field_config_options(case_field):
    assert case_field.configs[0].options.default_value == '1'
    assert case_field.configs[0].options.is_required is True


def test_description(case_field):
    assert case_field.description == DESCRIPTION


def test_display_order(case_field):
    assert case_field.display_order == DISPLAY_ORDER


def test_id(case_field):
    assert case_field.id == ID


def test_label(case_field):
    assert case_field.label == LABEL


def test_name(case_field):
    assert case_field.name == NAME


def test_system_name(case_field):
    assert case_field.system_name == SYSTEM_NAME


def test_type_id(case_field):
    assert case_field.type_id == TYPE_ID
