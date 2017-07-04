from datetime import datetime as dt

from ..const import SETTER_ERR
from .model_base import ModelBase


class Milestone(ModelBase):
    """ Object model for TestRail Milestones

    To get all Milestones

    .. code-block:: python

        project = traw_client.project(1234)  # Get Project with ID 1234
        milestones = list(traw_client.milestones(project))  # Get all milestones for project

    To get a specific milestone

    .. code-block:: python

        milestone_123 = traw_client.milestone(123)  # Gets milestone with ID 123 from API

    To create new project

    .. code-block:: python

        from datetime import timedelta, datetime as dt

        project = traw_client.project(15)  # Get project with project_id = 15

        new_milestone = traw_client.milestone()
        new_milestone.name = "My new TestRail milestone"
        new_milestone.description = "My new milestone description"
        new_milestone.due_on = dt.now() + timedelta(days=14)  # Due in 14 days
        new_milestone.is_completed = False
        new_milestone.project = project

    """
    @property
    def completed_on(self):
        """ The date/time when the milestone was marked as completed
            (as datetime.datetime object)
        """
        co = self._content.get('completed_on', None)
        if co:
            co = dt.fromtimestamp(co)
        return co

    @property
    def description(self):
        """ The description of the milestone. Can be set to any string """
        return self._content.get('description', None)

    @description.setter
    def description(self, val):
        if not isinstance(val, str):
            raise TypeError(SETTER_ERR.format(str, type(val)))
        self._content['description'] = val

    @property
    def due_on(self):
        """ The due date of the milestone. Can be set to a datetime.datetime object
            Defaults to None if no due date has been set
        """
        return dt.fromtimestamp(self._content.get('due_on', None))

    @due_on.setter
    def due_on(self, val):
        # TODO: log warning if setting due date to past
        if not isinstance(val, dt):
            raise TypeError(SETTER_ERR.format(dt, type(val)))
        self._content['due_on'] = val.timestamp()

    @property
    def is_complete(self):
        """ True if the milestone is marked as completed and false otherwise """
        return self._content.get('is_complete', False)

    @is_complete.setter
    def is_complete(self, val):
        if not isinstance(val, bool):
            raise TypeError(SETTER_ERR.format(bool, type(val)))
        self._content['is_complete'] = val

    @property
    def is_started(self):
        """ True if the milestone is marked as started and false otherwise """
        return self._content.get('is_started', False)

    @property
    def name(self):
        """ The full name of the milestone """
        return self._content.get('name', None)
