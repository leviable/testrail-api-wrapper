from copy import deepcopy

import pytest

from traw.models import Config, ConfigGroup, Project

CONFIG_GROUP_ID = 555
CONFIG_GROUP_NAME = 'mock config group name'
CONFIG_GROUP_NAME_NEW = 'new mock config group name'
CONFIG_ID = 666
CONFIG_NAME = 'mock config name'
CONFIG_NAME_NEW = "new config name"
PROJECT_ID = 15
CONFIG_CONTENT = {"group_id": CONFIG_GROUP_ID,
                  "id": CONFIG_ID,
                  "name": CONFIG_NAME}
CONFIG_GROUP_CONTENT = {"configs": [CONFIG_CONTENT],
                        "id": CONFIG_GROUP_ID,
                        "name": CONFIG_GROUP_NAME,
                        "project_id": PROJECT_ID}


@pytest.fixture()
def empty_config(client):
    return Config(client)


@pytest.fixture()
def empty_config_group(client):
    return ConfigGroup(client)


@pytest.fixture()
def config(client):
    return Config(client, deepcopy(CONFIG_CONTENT))


@pytest.fixture()
def config_w_project(client):
    project = Project(client, {'id': PROJECT_ID})
    return Config(client, deepcopy(CONFIG_CONTENT), project)


@pytest.fixture()
def config_group(client):
    return ConfigGroup(client, deepcopy(CONFIG_GROUP_CONTENT))


def test_config_project(empty_config, config, config_w_project):
    config.client.api.project_by_id.return_value = {'id': PROJECT_ID}

    assert empty_config.project is None

    assert config.project is None

    assert isinstance(config_w_project.project, Project)
    assert config_w_project.project.id == PROJECT_ID
    config.client.api.project_by_id.assert_called_with(PROJECT_ID)


def test_config_project_set(empty_config):
    project = Project(None, {'id': PROJECT_ID})

    assert empty_config.project is None

    empty_config.project = project

    assert empty_config._content['project_id'] == PROJECT_ID


def test_config_project_set_exc(empty_config):
    with pytest.raises(TypeError) as exc:
        empty_config.project = 1234

    assert str(Project) in str(exc)


def test_config_name_get(empty_config, config, config_w_project):
    assert empty_config.name is None
    assert config.name == CONFIG_NAME
    assert config_w_project.name == CONFIG_NAME


def test_config_name_set(empty_config, config, config_w_project):
    assert empty_config.name is None
    empty_config.name = CONFIG_NAME_NEW
    assert empty_config.name == CONFIG_NAME_NEW

    assert config.name == CONFIG_NAME
    config.name = CONFIG_NAME_NEW
    assert config.name == CONFIG_NAME_NEW

    assert config_w_project.name == CONFIG_NAME
    config_w_project.name = CONFIG_NAME_NEW
    assert config_w_project.name == CONFIG_NAME_NEW


def test_config_name_set_exc(empty_config):
    with pytest.raises(TypeError) as exc:
        empty_config.name = 1234

    assert str(str) in str(exc)
    assert str(int) in str(exc)


def test_config_config_group_get(empty_config, config, config_w_project):
    config.client.api.project_by_id.return_value = {'id': PROJECT_ID}
    config.client.api.config_groups.return_value = [CONFIG_GROUP_CONTENT]

    assert empty_config.config_group is None
    assert empty_config.client.api.method_calls == list()
    assert not empty_config.client.api.project_by_id.called
    assert not empty_config.client.api.config_groups.called

    assert isinstance(config.config_group, ConfigGroup)
    assert config.config_group.id == CONFIG_GROUP_ID
    assert config.config_group.name is None
    assert not config.client.api.project_by_id.called
    assert not config.client.api.config_groups.called

    assert isinstance(config_w_project.config_group, ConfigGroup)
    assert config_w_project.config_group.id == CONFIG_GROUP_ID
    assert config_w_project.config_group.name == CONFIG_GROUP_NAME
    config_w_project.client.api.project_by_id.assert_called_with(PROJECT_ID)
    config_w_project.client.api.config_groups.assert_called_with(PROJECT_ID)


def test_config_config_group_set(empty_config):
    assert empty_config.config_group is None
    empty_config.config_group = ConfigGroup(None, {'id': CONFIG_GROUP_ID})
    assert empty_config.config_group.id == CONFIG_GROUP_ID


def test_config_config_group(empty_config):
    with pytest.raises(TypeError) as exc:
        empty_config.config_group = 1234

    assert str(ConfigGroup) in str(exc)
    assert str(int) in str(exc)


def test_config_group_configs(empty_config_group, config_group):
    empty_config_group.client.api.project_by_id.return_value = {'id': PROJECT_ID}
    config_group.client.api.project_by_id.return_value = {'id': PROJECT_ID}

    assert list(empty_config_group.configs) == list()
    assert not empty_config_group.client.api.project_by_id.called

    assert len(list(config_group.configs)) == 1
    assert isinstance(next(config_group.configs), Config)
    assert next(config_group.configs).id == CONFIG_ID
    assert next(config_group.configs).name == CONFIG_NAME
    assert config_group.client.api.project_by_id.called
