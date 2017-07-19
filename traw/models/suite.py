from datetime import datetime as dt

from .. import const
from .model_base import ModelBase
from .posters import Addable, Deleteable, Updatable
from .project import Project


class Suite(Addable, Deleteable, Updatable, ModelBase):
    _ADDABLE_FIELDS = const.SUITE_ADD_FIELDS
    _UPDATABLE_FIELDS = const.SUITE_UPDATE_FIELDS

    @property
    def completed_on(self):
        """ The date/time when the suite was marked as completed
            (as datetime.datetime object)
        """
        co = self._content.get('completed_on', None)
        return dt.fromtimestamp(co) if co is not None else None

    @property
    def description(self):
        """ The description of the suite. Can be set to any string """
        return self._content.get('description', None)

    @description.setter
    def description(self, val):
        if not isinstance(val, str):
            raise TypeError(const.SETTER_ERR.format(str, type(val)))
        self._content['description'] = val

    @property
    def is_baseline(self):
        """ True if the test suite is a baseline test suite and false otherwise """
        return self._content.get('is_baseline', False)

    @property
    def is_completed(self):
        """ True if the test suite is marked as completed and false otherwise """
        return self._content.get('is_completed', False)

    @property
    def is_master(self):
        """ True if the test suite is a master test suite and false otherwise """
        return self._content.get('is_master', False)

    @property
    def name(self):
        """ The full name of the test suite """
        return self._content.get('name', None)

    @name.setter
    def name(self, val):
        if not isinstance(val, str):
            raise TypeError(const.SETTER_ERR.format(str, type(val)))
        self._content['name'] = val

    @property
    def project(self):
        """ The Project the test suite belongs to """
        project_id = self._content.get('project_id', None)
        return self.client.project(project_id) if project_id is not None else None

    @project.setter
    def project(self, project):
        if not isinstance(project, Project):
            raise TypeError(const.SETTER_ERR.format(Project, type(project)))
        self._content['project_id'] = project.id

    @property
    def url(self):
        """ The address/URL of the test suite in the user interface """
        return self._content.get('url', None)
