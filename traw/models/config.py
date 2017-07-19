from ..const import (CONFIG_GROUP_ADD_FIELDS, CONFIG_GROUP_UPDATE_FIELDS,
                     CONFIG_ADD_FIELDS, CONFIG_UPDATE_FIELDS, SETTER_ERR)
from .model_base import ModelBase
from .posters import Addable, Deleteable, Updatable
from .project import Project


class ConfigBase(ModelBase):
    """ Base Class for Config-related classes """
    @property
    def name(self):
        """ The name of the configuration group """
        return self._content.get('name', None)

    @name.setter
    def name(self, val):
        if not isinstance(val, str):
            raise TypeError(SETTER_ERR.format(str, type(val)))
        self._content['name'] = val

    @property
    def project(self):
        """ The Project the configuration group belongs to """
        project_id = self._content.get('project_id', None)
        return self.client.project(project_id) if project_id is not None else None

    @project.setter
    def project(self, project):
        if not isinstance(project, Project):
            raise TypeError(SETTER_ERR.format(Project, type(project)))
        self._content['project_id'] = project.id


class ConfigGroup(Addable, Deleteable, Updatable, ConfigBase):
    """ Object model for TestRail Config Groups

    To get an existing config group from the TestRail API:

    .. code-block:: python

        # Locate an existing config group by config group ID
        con_grp = traw_client.config_group(1234)

    To get all config gorups for a project from the TestRail API:

    .. code-block:: python

        # Locate the target project by project ID
        project = traw_client.project(4321)
        con_grps = traw_client.config_groups(project)

    """
    _ADDABLE_FIELDS = CONFIG_GROUP_ADD_FIELDS
    _UPDATABLE_FIELDS = CONFIG_GROUP_UPDATE_FIELDS

    @property
    def configs(self):
        """ Yields the individual configurations for the config group """
        project = self.project
        for config in self._content.get('configs', list()):
            yield Config(self.client, config, project=project)


class Config(Addable, Deleteable, Updatable, ConfigBase):
    """ Object model for TestRail Configs

    To get an existing config from the TestRail API:

    .. code-block:: python

        # Locate an existing config group by config group ID
        con_grp = traw_client.config_group(1234)
        configs = list(con_grp.configs)

    """
    _ADDABLE_FIELDS = CONFIG_ADD_FIELDS
    _UPDATABLE_FIELDS = CONFIG_UPDATE_FIELDS

    def __init__(self, client, content=None, project=None):
        super(Config, self).__init__(client, content)
        # TestRail configuration objects dont maintain references to the project
        # by default. However, in order to return a ConfigGroup instance, this
        # class needs a project reference in order to query the API
        if project:
            self.project = project

    @property
    def config_group(self):
        """ The config's parent ConfigGroup """
        config_group_id = self._content.get('group_id', None)
        if config_group_id is not None:
            if self.project is None:
                # TODO: Log a warning here, that we could not return full details
                #       without the project being set
                config_group = ConfigGroup(self.client, {'id': config_group_id})
            else:
                config_group = self.client.config_group(self.project, config_group_id)
        else:
            config_group = None

        return config_group

    @config_group.setter
    def config_group(self, val):
        if not isinstance(val, ConfigGroup):
            raise TypeError(SETTER_ERR.format(ConfigGroup, type(val)))
        self._content['group_id'] = val.id
