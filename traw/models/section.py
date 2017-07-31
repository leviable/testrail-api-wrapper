from .. import const
from .model_base import ModelBase
from .posters import Addable, Deleteable, Updatable
from .project import Project
from .suite import Suite


class Section(Addable, Deleteable, Updatable, ModelBase):
    """ Object model for TestRail Sections

    To add a new section

    .. code-block:: python

        # Get the project and suite you'll be working with
        project = traw_client.project(15)  # Project with ID of 15
        suite = traw_client.suite(12)      # Suite with ID of 12

        # Get an empty section object
        new_section = traw_client.section()
        new_section.name = "New project section"
        new_section.description = "New section description"
        new_section.project = project
        new_section.suite = suite

        # Add it
        section = traw_client.add(new_section)

    """
    _ADDABLE_FIELDS = const.SECTION_ADD_FIELDS
    _UPDATABLE_FIELDS = const.SECTION_UPDATE_FIELDS

    @property
    def depth(self):
        """ The level in the section hierarchy of the test suite """
        return self._content.get('depth', None)

    @property
    def description(self):
        """ The description of the section"""
        return self._content.get('description')

    @description.setter
    def description(self, val):
        if not isinstance(val, str):
            raise TypeError(const.SETTER_ERR.format(str, type(val)))
        self._content['description'] = val

    @property
    def display_order(self):
        """ The order in the test suite """
        return self._content.get('display_order', None)

    @property
    def name(self):
        """ The name of the section"""
        return self._content.get('name')

    @name.setter
    def name(self, val):
        if not isinstance(val, str):
            raise TypeError(const.SETTER_ERR.format(str, type(val)))
        self._content['name'] = val

    @property
    def parent(self):
        """ The parent section in the test suite """
        parent_id = self._content.get('parent_id', None)
        return self.client.section(parent_id) if parent_id is not None else None

    @parent.setter
    def parent(self, val):
        if not isinstance(val, Section):
            raise TypeError(const.SETTER_ERR.format(Section, type(val)))
        self._content['parent_id'] = val.id

    @property
    def project(self):
        """ The project this test section belong to """
        project_id = self._content.get('project_id', None)
        return self.client.project(project_id) if project_id is not None else None

    @project.setter
    def project(self, val):
        if not isinstance(val, Project):
            raise TypeError(const.SETTER_ERR.format(Project, type(val)))
        self._content['project_id'] = val.id

    @property
    def suite(self):
        """ The suite this test section belong to """
        suite_id = self._content.get('suite_id', None)
        return self.client.suite(suite_id) if suite_id is not None else None

    @suite.setter
    def suite(self, val):
        if not isinstance(val, Suite):
            raise TypeError(const.SETTER_ERR.format(Suite, type(val)))
        self._content['suite_id'] = val.id
