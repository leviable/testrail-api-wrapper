from types import GeneratorType
from datetime import datetime as dt

from .case import Case
from .. import const
from .milestone import Milestone
from .model_base import ModelBase
from .posters import Addable, Closeable, Deleteable, Updatable
from .project import Project
from .suite import Suite
from .user import User


class Run(Addable, Closeable, Deleteable, Updatable, ModelBase):
    """ Object model for TestRail Runs

    To create new run

    .. code-block:: python

        new_run = traw_client.run()
        new_run.name = "My new TestRail Run"
        new_run.description = "My new run description"

    """
    _ADDABLE_FIELDS = const.RUN_ADD_FIELDS
    _UPDATABLE_FIELDS = const.RUN_UPDATE_FIELDS

    @property
    def add_params(self):
        """ Returns params necessary to add the subclass object to TestRail """
        fields = {field: self._content.get(field, None) for field in self._ADDABLE_FIELDS}

        if fields['case_ids'] is None or fields['case_ids'] == list():
            fields.pop('case_ids')
        else:
            fields['case_ids'] = ','.join(map(str, fields['case_ids']))

        return fields

    @property
    def assigned_to(self):
        """ The user the entire test run is assigned to """
        user_id = self._content.get('assignedto_id', None)
        return self.client.user(user_id) if user_id is not None else None

    @assigned_to.setter
    def assigned_to(self, val):
        if not isinstance(val, User):
            raise TypeError(const.SETTER_ERR.format(User, type(val)))
        self._content['assignedto_id'] = val.id

    @property
    def blocked_count(self):
        """ The amount of tests in the test run marked as blocked """
        return self._content.get('blocked_count', None)

    @property
    def cases(self):
        """ A list of cases for the custom case selection """
        case_ids = self._content.get('case_ids', list())
        for case in [self.client.case(c) for c in case_ids]:
            yield case

    @cases.setter
    def cases(self, vals):
        if not isinstance(vals, (list, set, tuple, GeneratorType)):
            msg = ("``cases`` only accepts an iterable (list, set, tuple, "
                   "generator). Found {0}")
            raise TypeError(msg.format(type(vals)))

        case_ids = list()
        for val in vals:
            if not isinstance(val, (Case, int)):
                msg = ("cases iterator can only be models.Case objects or "
                       "int case IDs. Found at least one {0}")
                raise TypeError(msg.format(type(val)))
            case_ids.append(val.id if isinstance(val, Case) else val)
        self._content['case_ids'] = case_ids

    @property
    def completed_on(self):
        """ The date/time when the test run was closed
            (as datetime.datetime object)
        """
        co = self._content.get('completed_on', None)
        return dt.fromtimestamp(co) if co is not None else None

    @property
    def configs(self):
        """ The configs of the test run
            (only present if run is a part of a test plan with configurations)
        """
        if self.project is None:
            raise StopIteration

        for config_id in self._content.get('config_ids', list()):
            yield self.client.config(self.project, config_id)

    @property
    def created_by(self):
        """ The user who created the test run """
        user_id = self._content.get('created_by', None)
        return self.client.user(user_id) if user_id is not None else None

    @property
    def created_on(self):
        """ The date/time when the test run was created
            (as datetime.datetime object)
        """
        co = self._content.get('created_on', None)
        return dt.fromtimestamp(co) if co is not None else None

    # TODO: Add support for custom_statusX_count

    @property
    def description(self):
        """ The description of the run. Can be set to any string """
        return self._content.get('description', None)

    @description.setter
    def description(self, val):
        if not isinstance(val, str):
            raise TypeError(const.SETTER_ERR.format(str, type(val)))
        self._content['description'] = val

    @property
    def failed_count(self):
        """ The amount of tests in the test run marked as failed """
        return self._content.get('failed_count', None)

    @property
    def include_all(self):
        """ True if the test run includes all test cases and false otherwise """
        return self._content.get('include_all', True)

    @include_all.setter
    def include_all(self, val):
        if not isinstance(val, bool):
            raise TypeError(const.SETTER_ERR.format(bool, type(val)))
        self._content['include_all'] = val

    @property
    def is_completed(self):
        """ True if the test run was closed and false otherwise """
        return self._content.get('is_completed', False)

    @property
    def milestone(self):  # TODO: find out why API returns only None
        """ The  milestone this test run belongs to """
        milestone_id = self._content.get('milestone_id', None)
        return self.client.milestone(milestone_id) if milestone_id is not None else None

    @milestone.setter
    def milestone(self, val):
        if not isinstance(val, Milestone):
            raise TypeError(const.SETTER_ERR.format(Milestone, type(val)))
        self._content['milestone_id'] = val.id

    @property
    def name(self):
        """ The name of the test run """
        return self._content.get('name', None)

    @name.setter
    def name(self, val):
        if not isinstance(val, str):
            raise TypeError(const.SETTER_ERR.format(str, type(val)))
        self._content['name'] = val

    @property
    def passed_count(self):
        """ The amount of tests in the test run marked as passed """
        return self._content.get('passed_count', None)

    @property
    def plan(self):
        """ The test plan this test run belongs to """
        plan_id = self._content.get('plan_id', None)
        return self.client.plan(plan_id) if plan_id is not None else None

    @property
    def project(self):
        """ The Project the run belongs to """
        project_id = self._content.get('project_id', None)
        return self.client.project(project_id) if project_id is not None else None

    @project.setter
    def project(self, project):
        if not isinstance(project, Project):
            raise TypeError(const.SETTER_ERR.format(Project, type(project)))
        self._content['project_id'] = project.id

    @property
    def retest_count(self):
        """ The amount of tests in the test run marked as retest """
        return self._content.get('retest_count', None)

    @property
    def suite(self):
        """ The test suite for the test run
            (optional if the project is operating in single suite mode,
            required otherwise)
        """
        suite_id = self._content.get('suite_id', None)
        return self.client.suite(suite_id) if suite_id is not None else None

    @suite.setter
    def suite(self, val):
        if not isinstance(val, Suite):
            raise TypeError(const.SETTER_ERR.format(Suite, type(val)))
        self._content['suite_id'] = val.id

    @property
    def untested_count(self):
        """ The amount of tests in the test run marked as untested """
        return self._content.get('untested_count', None)

    @property
    def update_params(self):
        """ Returns params necessary to update the subclass object in TestRail """
        fields = {field: self._content.get(field, None) for field in self._UPDATABLE_FIELDS}
        if fields['case_ids'] is None or fields['case_ids'] == list():
            fields.pop('case_ids')
        else:
            fields['case_ids'] = ','.join(map(str, fields['case_ids']))

        return fields

    @property
    def url(self):
        """ The address/URL of the run in the user interface """
        return self._content.get('url', None)
