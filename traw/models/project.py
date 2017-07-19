from datetime import datetime as dt

from .model_base import ModelBase
from ..const import PROJECT_ADD_FIELDS, PROJECT_UPDATE_FIELDS, SETTER_ERR
from .posters import Addable, Deleteable, Updatable


class Project(Addable, Deleteable, Updatable, ModelBase):
    """ Object model for TestRail Projects

    To create new project

    .. code-block:: python

        new_project = traw_client.project()
        new_project.name = "My new TestRail project"
        new_project.announcement = "My new project announcment"
        new_project.show_announcement = True
        new_project.suite_mode = 1

    """
    _ADDABLE_FIELDS = PROJECT_ADD_FIELDS
    _UPDATABLE_FIELDS = PROJECT_UPDATE_FIELDS

    @property
    def announcement(self):
        """ The description/announcement of the project
            Can be set to any string
        """
        return self._content.get('announcement', None)

    @announcement.setter
    def announcement(self, val):
        if not isinstance(val, str):
            raise TypeError(SETTER_ERR.format(str, type(val)))
        self._content['announcement'] = val

    @property
    def completed_on(self):
        """ The date/time when the project was marked as completed
            (as datetime.datetime object)
        """
        co = self._content.get('completed_on', None)
        if co:
            co = dt.fromtimestamp(co)
        return co

    @property
    def is_completed(self):
        """ True if the project is marked as completed and false otherwise """
        return self._content.get('is_completed', False)

    @is_completed.setter
    def is_completed(self, val):
        if not isinstance(val, bool):
            raise TypeError(SETTER_ERR.format(bool, type(val)))
        self._content['is_completed'] = val

    @property
    def name(self):
        """ The name of the project. Can be set to any string """
        return self._content.get('name', None)

    @name.setter
    def name(self, val):
        if not isinstance(val, str):
            raise TypeError(SETTER_ERR.format(str, type(val)))
        self._content['name'] = val

    @property
    def show_announcement(self):
        """ To show or not show an announement. Can be set to True or False """
        return self._content.get('show_announcement', False)

    @show_announcement.setter
    def show_announcement(self, val):
        if not isinstance(val, bool):
            raise TypeError(SETTER_ERR.format(bool, type(val)))
        self._content['show_announcement'] = val

    @property
    def suite_mode(self):
        """ The suite mode of the project (1 for single suite mode,
            2 for single suite + baselines, 3 for multiple suites)
            (added with TestRail 4.0)
        """
        return self._content.get('suite_mode', None)

    @suite_mode.setter
    def suite_mode(self, val):
        if not isinstance(val, int):
            raise TypeError(SETTER_ERR.format(int, type(val)))
        elif val not in [1, 2, 3]:
            raise ValueError('suite_mode can only be set to 1, 2, or 3')
        self._content['suite_mode'] = val

    @property
    def url(self):
        """ The address/URL of the project in the user interface """
        return self._content.get('url', None)
