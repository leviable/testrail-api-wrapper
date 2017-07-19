import time
from copy import deepcopy
from datetime import datetime as dt

from .. import const
from .model_base import ModelBase
from .posters import Addable, Deleteable, Updatable
from .project import Project


class MilestoneBase(Addable, Deleteable, Updatable, ModelBase):
    _ADDABLE_FIELDS = const.MILESTONE_ADD_FIELDS
    _UPDATABLE_FIELDS = const.MILESTONE_UPDATE_FIELDS

    @property
    def completed_on(self):
        """ The date/time when the milestone was marked as completed
            (as datetime.datetime object)
        """
        co = self._content.get('completed_on', None)
        return dt.fromtimestamp(co) if co is not None else None

    @property
    def description(self):
        """ The description of the milestone. Can be set to any string """
        return self._content.get('description', None)

    @description.setter
    def description(self, val):
        if not isinstance(val, str):
            raise TypeError(const.SETTER_ERR.format(str, type(val)))
        self._content['description'] = val

    @property
    def due_on(self):
        """ The due date of the milestone. Can be set to a datetime.datetime object
            Defaults to None if no due date has been set
        """
        due_on_ = self._content.get('due_on', None)
        return dt.fromtimestamp(due_on_) if due_on_ is not None else None

    @due_on.setter
    def due_on(self, val):
        # TODO: log warning if setting due date to past
        if not isinstance(val, dt):
            raise TypeError(const.SETTER_ERR.format(dt, type(val)))
        self._content['due_on'] = int(time.mktime(val.timetuple()))

    @property
    def is_completed(self):
        """ True if the milestone is marked as completed and false otherwise """
        return self._content.get('is_completed', False)

    @is_completed.setter
    def is_completed(self, val):
        if not isinstance(val, bool):
            raise TypeError(const.SETTER_ERR.format(bool, type(val)))
        self._content['is_completed'] = val

    @property
    def is_started(self):
        """ True if the milestone is marked as started and false otherwise """
        return self._content.get('is_started', False)

    @is_started.setter
    def is_started(self, val):
        if not isinstance(val, bool):
            raise TypeError(const.SETTER_ERR.format(bool, type(val)))
        self._content['is_started'] = val

    @property
    def name(self):
        """ The full name of the milestone """
        return self._content.get('name', None)

    @name.setter
    def name(self, val):
        if not isinstance(val, str):
            raise TypeError(const.SETTER_ERR.format(str, type(val)))
        self._content['name'] = val

    @property
    def project(self):
        """ The Project the milestone belongs to """
        project_id = self._content.get('project_id', None)
        return self.client.project(project_id) if project_id is not None else None

    @project.setter
    def project(self, project):
        if not isinstance(project, Project):
            raise TypeError(const.SETTER_ERR.format(Project, type(project)))
        self._content['project_id'] = project.id

    @property
    def start_on(self):
        """ The scheduled start date/time of the milestone
            (as datetime.datetime object)
        """
        start_on_ = self._content.get('start_on', None)
        return dt.fromtimestamp(start_on_) if start_on_ is not None else None

    @start_on.setter
    def start_on(self, val):
        if not isinstance(val, dt):
            raise TypeError(const.SETTER_ERR.format(dt, type(val)))
        self._content['start_on'] = int(time.mktime(val.timetuple()))

    @property
    def started_on(self):
        """ The date/time when the milestone was started
            (as datetime.datetime object)
        """
        started_on_ = self._content.get('started_on', None)
        return dt.fromtimestamp(started_on_) if started_on_ is not None else None

    @started_on.setter
    def started_on(self, val):
        if not isinstance(val, dt):
            raise TypeError(const.SETTER_ERR.format(dt, type(val)))
        self._content['started_on'] = int(time.mktime(val.timetuple()))

    @property
    def url(self):
        """ The address/URL of the milestone in the user interface """
        return self._content.get('url', None)


class SubMilestone(MilestoneBase):
    @property
    def parent(self):
        """ The ID of the parent milestone the sub-milestone belongs to

            When assigning a new parent milestone to a sub-milestone, they most both have
            the same project set
        """
        parent_id = self._content.get('parent_id', None)
        return self.client.milestone(parent_id) if parent_id is not None else None

    @parent.setter
    def parent(self, parent_ms):
        if not isinstance(parent_ms, Milestone):
            raise TypeError(const.SETTER_ERR.format(Milestone, type(parent_ms)))
        elif self.project is None:
            msg = "You must set the sub-milestone's project to an existing project first"
            raise ValueError(msg)
        elif self.project.id != parent_ms.project.id:
            msg = ("The sub-milestone and parent milestone project IDs must match. Currently, "
                   "the sub-milestone project ID is {0} and the parent milestone project "
                   "ID is {1}")
            raise ValueError(msg.format(self.project.id, parent_ms.project.id))
        else:
            self._content['parent_id'] = parent_ms.id


class Milestone(MilestoneBase):
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
    def add_parent(self, milestone):
        """ Adding a parent milestone to a Milestone object transforms it into a
            SubMilestone

            :param milestone: Milestone or int of the paraent milestone

            :returns: new SubMilestone
        """
        if not isinstance(milestone, (int, Milestone)):
            exp_types = "{0} or {1}".format(int, Milestone)
            raise TypeError(const.SETTER_ERR.format(exp_types, type(milestone)))

        parent_id = milestone if isinstance(milestone, int) else milestone.id

        sub_milestone = deepcopy(self._content)
        sub_milestone['parent_id'] = parent_id

        return SubMilestone(self.client, sub_milestone)

    @property
    def sub_milestones(self):
        """ Returns sub Milestone generator

            The sub-milestones that belong to the milestone (if any)
        """
        # This one is a bit tricky, as sub milestones are only included in the API response
        # if the milestone came from the ``get_milestone`` endpoint. If it came from, for
        # example, ``get_milestones``, the keyword will be completely absent
        sub_milestones_ = self._content.get('milestones', None)
        if sub_milestones_ is None:
            # None indicates this milestone came from somewhere other than the `get_milestone`
            # endpoint. Need to make an additional API call to get the sub milestones
            self._content['milestones'] = self.client.api.milestone_by_id(self.id)['milestones']

        for sub_milestone in self._content['milestones']:
            yield SubMilestone(self.client, sub_milestone)
