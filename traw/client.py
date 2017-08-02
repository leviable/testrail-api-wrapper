from collections import Iterable
from datetime import datetime as dt
import time

from . import const
from . import models
from .api import API
from .exceptions import TRAWClientError, UnknownCustomStatusError
from .models.model_base import ModelBase
from .utils import dispatchmethod


class Client(object):
    """ The Client class is the primary access point to the Testrail REST API

    The intended way to use this class is:

    .. code-block:: python

        import traw
        testrail = traw.Client(username='username',
                               user_api_key='api_key',
                               url='url')

    Authentication credentials will be pulled in the following order:
     - TRAW Client instantiation
       - traw.Client(username='<username>', user_api_key='<api_key>', url='<url>')
       - (optional) You may substitute `password` for `user_api_key`
     - Environmental variables
       - TRAW_USERNAME=<username>
       - TRAW_USER_API_KEY=<api_key>
       - TRAW_URL=<url>
       - (optional) You may substitude `TRAW_PASSWORD` for `TRAW_USER_API_KEY`
     - A configuration file in the user's home directory (~/.traw_config)
       - [TRAW]
         username = <username>
         user_api_key = <user_api_key>
         url = <url>
       - (optional) You may substitute `password = <password>` for `user_api_key`

    If both a user api key and a user password are provided, the api key will be used
    """
    def __init__(self, **credentials):
        """ Initialize the TRAW instance """
        # TODO: Update doc string with supported credential keywords
        self.api = API(**credentials)

    # POST generics
    @dispatchmethod
    def add(self, obj):
        # Not directly implemented. TypeError is raised if called with unregistered object
        msg = "TRAW and/or TestRail's API does not support adding objects of type {0}"
        raise TypeError(msg.format(type(obj)))

    @dispatchmethod
    def close(self, obj):
        # Not directly implemented. TypeError is raised if called with unregistered object
        msg = "TRAW and/or TestRail's API does not support closing objects of type {0}"
        raise TypeError(msg.format(type(obj)))

    @dispatchmethod
    def delete(self, obj):
        # Not directly implemented. TypeError is raised if called with unregistered object
        msg = "TRAW and/or TestRail's API does not support deleting objects of type {0}"
        raise TypeError(msg.format(type(obj)))

    @dispatchmethod
    def update(self, obj):
        # Not directly implemented. TypeError is raised if called with unregistered object
        msg = "TRAW and/or TestRail's API does not support updating objects of type {0}"
        raise TypeError(msg.format(type(obj)))

    # Case related methods
    @dispatchmethod
    def case(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return a models.Case instance
            `client.case()` returns a new Case instance (no API call)
            `client.case(1234)` returns a Case instance with an ID of 1234

        :param: no method parameters, will return a new, uncofigured models.Case instance
        :param case_id: int, Case ID for a case that exists in TestRail

        :returns: models.Case instance
        """
        return models.Case(self)

    @case.register(int)
    def _case_by_id(self, case_id):
        """ Do not call directly
            Returns case with ``case_id``
        """
        return models.Case(self, self.api.case_by_id(case_id))

    @dispatchmethod
    def cases(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return models.Case generator for the given models.Project object
            or project ID

        `client.cases(project)` yields cases associated with the Project instance
        `client.cases(1234)` yields cases associated with project id 1234

        Optional filter examples:
        `client.cases(1234, case_type=client.case_type(112))`  # by CaseType object
        `client.cases(1234, case_type=112)`  # by CaseType ID
        `client.cases(1234, case_type=[101, 102, 103])`  # by list of CaseType IDs
        `client.cases(1234, created_after=datetime.now()-timedelta(days=1))`  # 1 day old
        `client.cases(1234, created_before=1469726522)`  # using a timestamp
        `client.cases(1234, created_by=client.user("automation@user.com"))`  # by User object
        `client.cases(1234, created_by=client.user(15))`  # by User ID
        `client.cases(1234, created_by=[12, 15, 34])`  # by list of User IDs
        `client.cases(1234, is_completed=True)`
        `client.cases(1234, limit=3500)`
        `client.cases(1234, milestone=client.milestone(112))`  # by Milestone object
        `client.cases(1234, milestone=112)`  # by Milestone ID
        `client.cases(1234, milestone=[101, 102, 103])`  # by list of Milestone IDs
        `client.cases(1234, priority=client.priority(4))`  # by Priority object
        `client.cases(1234, priority=112)`  # by Priority ID
        `client.cases(1234, priority=[101, 102, 103])`  # by list of Priority IDs
        `client.cases(1234, section=client.section(223))`  # by Section object
        `client.cases(1234, section=223)`  # by Section ID
        `client.cases(1234, suite=client.suite(223))`  # by Suite object
        `client.cases(1234, suite=223)`  # by Suite ID
        `client.cases(1234, template=client.template(4))`  # by Template object
        `client.cases(1234, template=112)`  # by Template ID
        `client.cases(1234, template=[101, 102, 103])`  # by list of Template IDs
        `client.cases(1234, updated_after=datetime.now()-timedelta(days=1))`  # 1 day old
        `client.cases(1234, updated_before=1469726522)`  # using a timestamp
        `client.cases(1234, updated_by=client.user("automation@user.com"))`  # by User object
        `client.cases(1234, updated_by=client.user(15))`  # by User ID
        `client.cases(1234, updated_by=[12, 15, 34])`  # by list of User IDs

        :param project: models.Project object for a project in TestRail
        :param project_id: int, Project ID for a project that exists in TestRail
        :param section: models.Section instance or int (Section ID)
        :param suite: models.Suite instance or int (Suite ID)

        :param case_type: models.CaseType instance(s) or int(s) (CaseType ID(s))
        :param created_after: datetime.datetime object or timestamp
        :param created_before: datetime.datetime object or timestamp
        :param created_by: models.User instance(s) or int(s) (User ID(s))
        :param milestone: models.(Sub)Milestone instance(s) or int(s) (Milestone ID(s))
        :param priority: models.Priority instance(s) or int(s) (Priority ID(s))
        :param template: models.Template instance(s) or int(s) (Template ID(s))
        :param updated_after: datetime.datetime object or timestamp
        :param updated_before: datetime.datetime object or timestamp
        :param updated_by: models.User instance(s) or int(s) (User ID(s))

        :raiess: NotImplementedError if called with no parameters (`client.runs()`) or
                 a parameter of an unsupported type (`client.runs(True)`)

        :yields: models.Run objects
        """
        raise NotImplementedError(const.NOTIMP.format("models.Project or int"))

    @cases.register(int)
    def _cases_by_project_id(self, project_id, suite=None, section=None, **kwargs):

        project = self.project(project_id)
        if project.suite_mode != 1 and suite is None:
            msg = ("The project with ID {0} is set to a suite_mode of {1}, which "
                   "requires a valid suite or suite_id to retrieve cases")
            raise TypeError(msg.format(project, project.suite_mode))

        params = dict()
        if suite:
            if not isinstance(suite, (int, models.Suite)):
                msg = ("``suite`` must be a models.Suite object, or int ID of a "
                       "suite in testrail. Found {0}")
                raise TypeError(msg.format(suite))

            params['suite_id'] = suite.id if isinstance(suite, models.Suite) else suite

        if section:
            if not isinstance(section, (int, models.Section)):
                msg = ("``section`` must be a models.Section object, or int ID "
                       "of a section in testrail. Found {0}")
                raise TypeError(msg.format(section))

            params['section_id'] = section.id if isinstance(section, models.Section) else section

        normalize_dt_filter(kwargs, params, 'created_after')
        normalize_dt_filter(kwargs, params, 'created_before')
        normalize_param(kwargs, params, 'case_type', 'type_id', models.CaseType)
        normalize_param(kwargs, params, 'created_by', 'created_by', models.User)
        normalize_param(kwargs, params, 'milestone', 'milestone_id',
                        models.Milestone, models.SubMilestone)
        normalize_param(kwargs, params, 'priority', 'priority_id', models.Priority)
        normalize_param(kwargs, params, 'template', 'template_id', models.Template)
        normalize_param(kwargs, params, 'updated_by', 'updated_by', models.User)
        normalize_dt_filter(kwargs, params, 'updated_after')
        normalize_dt_filter(kwargs, params, 'updated_before')

        for case in self.api.cases_by_project_id(project_id, **params):
            yield models.Case(self, case)

    @cases.register(models.Project)
    def _cases_by_project(self, project, suite=None, section=None, **kwargs):
        for case in self.cases(project.id, suite, section, **kwargs):
            yield case

    # Case type related methods
    @dispatchmethod
    def case_type(self):
        """
            :param case_type_id: int

            :returns: models.CaseType
        """
        raise NotImplementedError(const.NOTIMP.format("int"))

    @case_type.register(int)
    def _case_type_by_id(self, case_type_id):
        """ Do not call directly
            Returns a models.CaseType object with id of ``case_type_id``
            :param case_type_id: int

            :returns: models.CaseType
        """
        for sys_case_type in self.case_types():
            if sys_case_type.id == case_type_id:
                case_type = sys_case_type
                break
        else:
            msg = "Could not locate a models.CaseType with id of {0}"
            raise TRAWClientError(msg.format(case_type_id))

        return case_type

    def case_types(self):
        """ Returns a case types generator

        :yields: models.CaseType Objects

        """
        for case_type in list(self.api.case_types()):
            yield models.CaseType(self, case_type)

    # Config related methods
    @dispatchmethod
    def config(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return new models.Config object

            `client.config()` returns a new Config instance (no API call)

        :returns: models.Config object
        """
        return models.Config(self)

    @add.register(models.Config)
    def _config_add(self, config):
        response = self.api.config_add(config.config_group.id, config.add_params)
        return models.Config(self, response)

    @config.register(models.Project)
    def _config_by_project(self, project, config_id):
        return self.config(project.id, config_id)

    @config.register(int)
    def _config_by_project_id(self, project_id, config_id):
        for config_group in self.config_groups(project_id):
            for sys_config in config_group.configs:
                if sys_config.id == config_id:
                    config = sys_config
                    break
            else:  # Necessary to break out of both for loops
                continue
            break
        else:
            msg = ("Could not locate a models.Config with id of {0} "
                   "for project with ID {1}")
            raise TRAWClientError(msg.format(config_id, project_id))

        return config

    @delete.register(models.Config)
    def _config_delete(self, config):
        self.api.config_delete(config.id)

    @update.register(models.Config)
    def _config_update(self, config):
        response = self.api.config_update(config.id, config.update_params)
        return models.Config(self, response)

    @dispatchmethod
    def config_group(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return models.ConfigGroup for the given models.Project or project ID
            and config_group ID

            `client.config_group()` returns a new ConfigGroup instance (no API call)
            `client.config_group(project, 5678)` yields config group associated
                with the Project instance and config group id 5678
            `client.config_group(1234, 5678)` yields config groups associated with
                project id 1234 and config group 5678

        :param project: models.Project object for a project that exists in TestRail
        :param project_id: int, Project ID for a project that exists in TestRail
        :param config_group_id: the ID of the target config group

        :raiess: NotImplementedError if called with no parameters or a parameter of an
                     unsupported type(`client.config_group()`)

        :returns: models.ConfigGroup object
        """
        return models.ConfigGroup(self)

    @add.register(models.ConfigGroup)
    def _config_group_add(self, config_group):
        response = self.api.config_group_add(config_group.project.id, config_group.add_params)
        return models.ConfigGroup(self, response)

    @config_group.register(int)
    def _config_group_by_project_id(self, project_id, config_group_id):
        for sys_config_group in self.config_groups(project_id):
            if sys_config_group.id == config_group_id:
                config_group = sys_config_group
                break
        else:
            msg = ("Could not locate a models.ConfigGroup with id of {0} "
                   "for project with ID {1}")
            raise TRAWClientError(msg.format(config_group_id, project_id))

        return config_group

    @config_group.register(models.Project)
    def _config_group_by_project(self, project, config_group_id):
        return self.config_group(project.id, config_group_id)

    @delete.register(models.ConfigGroup)
    def _config_group_delete(self, config_group):
        self.api.config_group_delete(config_group.id)

    @update.register(models.ConfigGroup)
    def _config_group_update(self, config_group):
        response = self.api.config_group_update(config_group.id, config_group.update_params)
        return models.ConfigGroup(self, response)

    @dispatchmethod
    def config_groups(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return models.ConfigGroup generator for the given models.Project
            object or project ID

            `client.config_groups(project)` yields config groups associated with
                the Project instance
            `client.config_groups(1234)` yields config groups associated with
                project id 1234

        :param project: models.Project object for a project that exists in TestRail
        :param project_id: int, Project ID for a project that exists in TestRail

        :raiess: NotImplementedError if called with no parameters or a parameter of an
                     unsupported type(`client.config_groups()`)

        :yields: models.ConfigGroup objects
        """
        raise NotImplementedError(const.NOTIMP.format("models.Project or int"))

    @config_groups.register(int)
    def _config_groups_by_project_id(self, project_id):
        for config_group in self.api.config_groups(project_id):
            yield models.ConfigGroup(self, config_group)

    @config_groups.register(models.Project)
    def _config_groups_by_project(self, project):
        for config_group in self.config_groups(project.id):
            yield config_group

    # Milestone related methods
    @dispatchmethod
    def milestone(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return a models.Milestone instance
            `client.milestone()` returns a new Milestone instance (no API call)
            `client.milestone(1234)` returns a Milestone instance with an ID of 1234

        :param: no method parameters, will return a new, uncofigured Milestone instance
        :param milestone_id: int, Milestone ID for a milestone that exists in TestRail

        :returns: models.Milestone instance
        """
        return models.Milestone(self)

    @milestone.register(int)
    def _milestone_by_id(self, milestone_id):
        """ Do not call directly
            Returns milestone with ``milestone_id``
        """
        return models.Milestone(self, self.api.milestone_by_id(milestone_id))

    @add.register(models.Milestone)
    @add.register(models.SubMilestone)
    def _milestone_add(self, milestone):
        response = self.api.milestone_add(milestone.project.id, milestone.add_params)
        if response.get('parent_id', None) is None:
            added_milestone = models.Milestone(self, response)
        else:
            added_milestone = models.SubMilestone(self, response)

        return added_milestone

    @delete.register(models.Milestone)
    @delete.register(models.SubMilestone)
    def _milestone_delete(self, milestone):
        self.api.milestone_delete(milestone.id)

    @update.register(models.Milestone)
    @update.register(models.SubMilestone)
    def _milestone_update(self, milestone):
        response = self.api.milestone_update(milestone.id, milestone.update_params)
        if response.get('parent_id', None) is None:
            updated_milestone = models.Milestone(self, response)
        else:
            updated_milestone = models.SubMilestone(self, response)

        return updated_milestone

    @dispatchmethod
    def milestones(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return models.Milestone generator for the given models.Project object or project ID

            `client.milestones(project)` yields milestones associated with the Project instance
            `client.milestones(1234)` yields milestones associated with project id 1234

        :param project: models.Project object for a project that exists in TestRail
        :param project_id: int, Project ID for a project that exists in TestRail

        :raiess: NotImplementedError if called with no parameters or a parameter of an
                     unsupported type(`client.milestones()`)

        :yields: models.Milestone objects
        """
        raise NotImplementedError(const.NOTIMP.format("models.Project or int"))

    @milestones.register(int)
    def _milestones_by_project_id(self, project_id, is_completed=None, is_started=None):
        msg = "{0} must be either None or bool, found {1}"
        if not isinstance(is_completed, (type(None), bool)):
            raise TypeError(msg.format('is_completed', is_completed, type(is_completed)))
        elif not isinstance(is_started, (type(None), bool)):
            raise TypeError(msg.format('is_started', is_started, type(is_started)))

        for milestone in self.api.milestones(project_id, is_completed, is_started):
            yield models.Milestone(self, milestone)

    @milestones.register(models.Project)
    def _milestones_by_project(self, project, is_completed=None, is_started=None):
        for milestone in self.milestones(project.id, is_completed, is_started):
            yield milestone

    # Plan related methods
    @dispatchmethod
    def plan(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return a models.Plan instance
            `client.plan()` returns a new Plan instance (no API call)
            `client.plan(1234)` returns a Plan instance with an ID of 1234

        :param: no method parameters, will return a new, uncofigured models.Plan instance
        :param plan_id: int, Plan ID for a plan that exists in TestRail

        :returns: models.Plan instance
        """
        return models.Plan(self)

    @plan.register(int)
    def _plan_by_id(self, plan_id):
        """ Do not call directly
            Returns plan with ``plan_id``
        """
        return models.Plan(self, self.api.plan_by_id(plan_id))

    # Priority related methods
    @dispatchmethod
    def priority(self):
        """
            :param priority_id: int

            :returns: models.Priority
        """
        raise NotImplementedError(const.NOTIMP.format("int"))

    @priority.register(int)
    def _priority_by_id(self, priority_id):
        """ Do not call directly
            Returns a models.Priority object with id of ``priority_id``
            :param priority_id: int

            :returns: models.Priority
        """
        for sys_priority in self.priorities():
            if sys_priority.id == priority_id:
                priority = sys_priority
                break
        else:
            msg = "Could not locate a models.Priority with id of {0}"
            raise TRAWClientError(msg.format(priority_id))

        return priority

    def priorities(self):
        """ Returns a priority generator

        :yields: models.Priority Objects
        """
        for priority in list(self.api.priorities()):
            yield models.Priority(self, priority)

    # Project related methods
    @dispatchmethod
    def project(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return a Project instance
            `client.project()` returns a new Project instance (no API call)
            `client.project(1234)` returns a Project instance with an id of 1234

            :returns: models.Project
        """
        return models.Project(self)

    @add.register(models.Project)
    def _project_add(self, project):
        response = self.api.project_add(project.add_params)
        return models.Project(self, response)

    @project.register(int)
    def _project_by_id(self, project_id):
        """ Do not call directly
            :param project_id: int

            :returns: models.Project
        """
        return models.Project(self, self.api.project_by_id(project_id))

    @delete.register(models.Project)
    def _project_delete(self, project):
        self.api.project_delete(project.id)

    @update.register(models.Project)
    def _project_update(self, project):
        response = self.api.project_update(project.id, project.update_params)
        return models.Project(self, response)

    def projects(self, active_only=False, completed_only=False):
        """ Returns models.Projects generator

        Leave both active_only and completed_only as False to return all projects

        :param active_only: Only include currently active projects in list
        :param completed_only: Only include completed projects in list

        :raises: TypeError if both active_only and completed_only are both set to True

        :yields: models.Project Objects
        """
        if active_only is True and completed_only is True:
            raise TypeError('Either `active_only` or `completed_only` can be '
                            'set to True, but not both')

        elif active_only is True or completed_only is True:
            is_completed = 1 if completed_only else 0
        else:
            is_completed = None

        for project in list(self.api.projects(is_completed)):
            yield models.Project(self, project)

    # Result related methods
    @dispatchmethod
    def result(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return a models.Result instance
            `client.result()` returns a new Result instance (no API call)

        :param: no method parameters, will return a new, uncofigured models.Result instance

        :returns: models.Result instance
        """
        return models.Result(self)

    @add.register(models.Result)
    def _result_add(self, result):
        response = self.api.result_add(result.test.id, result.add_params)
        return models.Result(self, response)

    @dispatchmethod
    def results(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return models.Result generator for the given models.Test object or test ID

        `client.results(test)` yields results for Test instance
        `client.results(1234)` yields results for test with id 1234
        `client.results(run)` yields results for Run instance
        `client.results(1234, obj_type=models.Run)` yields results for Run with id 1234

        :param test: models.Test object for a test that exists in TestRail
        :param run: models.Run object for a run that exists in TestRail
        :param obj_id: int, Run ID or Test ID for a Run/Test that exists in TestRail

        :raiess: NotImplementedError if called with no parameters (`client.results()`) or
                 a parameter of an unsupported type (`client.results(True)`)

        :yields: models.Result objects
        """
        raise NotImplementedError(const.NOTIMP.format("models.Test or int"))

    @results.register(int)
    def _results_by_obj_id(self, obj_id, obj_type=models.Test, with_status=None, limit=None):
        API_METHODS = {models.Run: self.api.results_by_run_id,
                       models.Test: self.api.results_by_test_id}
        if obj_type not in API_METHODS:
            msg = "Unknown obj_type. Must be {0}. Found {1}"
            msg = msg.format(" or ".join([str(models.Run), str(models.Test)]), obj_type)
            raise TypeError(msg)

        api_method = API_METHODS[obj_type]

        params = dict()
        if limit:
            params['limit'] = int(limit)

        ws_args = {'with_status': with_status}
        normalize_param(ws_args, params, 'with_status', 'status_id', models.Status)

        for result in api_method(obj_id, **params):
            yield models.Result(self, result)

    @results.register(models.Run)
    def _results_by_run(self, run, with_status=None, limit=None):
        params = dict(obj_type=models.Run, with_status=with_status, limit=limit)
        for result in self.results(run.id, **params):
            yield result

    @results.register(models.Test)
    def _results_by_test(self, test, with_status=None, limit=None):
        for result in self.results(test.id, with_status=with_status, limit=limit):
            yield result

    # Run related methods
    @dispatchmethod
    def run(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return a models.Run instance
            `client.run()` returns a new Run instance (no API call)
            `client.run(1234)` returns a Run instance with an ID of 1234

        :param: no method parameters, will return a new, uncofigured models.Run instance
        :param run_id: int, Run ID for a run that exists in TestRail

        :returns: models.Run instance
        """
        return models.Run(self)

    @add.register(models.Run)
    def _run_add(self, run):
        response = self.api.run_add(run.project.id, run.add_params)
        return models.Run(self, response)

    @run.register(int)
    def _run_by_id(self, run_id):
        """ Do not call directly
            Returns run with ``run_id``
        """
        return models.Run(self, self.api.run_by_id(run_id))

    @close.register(models.Run)
    def _run_close(self, run):
        return models.Run(self, self.api.run_close(run.id))

    @delete.register(models.Run)
    def _run_delete(self, run):
        self.api.run_delete(run.id)

    @update.register(models.Run)
    def _run_update(self, run):
        response = self.api.run_update(run.id, run.update_params)
        return models.Run(self, response)

    @dispatchmethod
    def runs(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return models.Run generator for the given models.Project object or project ID

        `client.runs(project)` yields runs associated with the Project instance
        `client.runs(1234)` yields runs associated with project id 1234

        Optional filter examples:
        `client.runs(1234, created_after=datetime.now()-timedelta(days=1))`  # 1 day old
        `client.runs(1234, created_before=1469726522)`  # using a timestamp
        `client.runs(1234, created_by=client.user("automation@user.com"))`  # by User object
        `client.runs(1234, created_by=client.user(15))`  # by User ID
        `client.runs(1234, created_by=[12, 15, 34])`  # by list of User IDs
        `client.runs(1234, is_completed=True)`
        `client.runs(1234, limit=3500)`
        `client.runs(1234, milestone=client.milestone(112))`  # by Milestone object
        `client.runs(1234, milestone=112)`  # by Milestone ID
        `client.runs(1234, milestone=[101, 102, 103])`  # by list of Milestone IDs
        `client.runs(1234, suite=client.suite(223))`  # by Suite object
        `client.runs(1234, suite=223)`  # by Suite ID
        `client.runs(1234, suite=[222, 223, 224])`  # by list of Suite IDs
        `client.runs(1234, suite=[suite1, suite2, suite3])`  # by list of Suite objects

        :param project: models.Project object for a project that exists in TestRail
        :param project_id: int, Project ID for a project that exists in TestRail
        :param created_after: datetime.datetime object or timestamp
        :param created_before: datetime.datetime object or timestamp
        :param created_by: models.User instance(s) or int(s) (User ID(s))
        :param is_completed: None (any state) or Bool
        :param limit: int, only return <limit> responses
        :param milestone: models.(Sub)Milestone instance(s) or int(s) (Milestone ID(s))
        :param suite: models.Suite instance(s) or int(s) (Suite ID(s))

        :raiess: NotImplementedError if called with no parameters (`client.runs()`) or
                 a parameter of an unsupported type (`client.runs(True)`)

        :yields: models.Run objects
        """
        raise NotImplementedError(const.NOTIMP.format("models.Project or int"))

    @runs.register(int)
    def _runs_by_project_id(self, project_id, **kwargs):
        params = dict()
        normalize_dt_filter(kwargs, params, 'created_after')
        normalize_dt_filter(kwargs, params, 'created_before')

        is_completed = kwargs.get('is_completed', None)
        if is_completed is not None:
            if is_completed is not True and is_completed is not False:
                msg = "`is_completed` can only be None, True, or False. Found '{0}'"
                raise TypeError(msg.format(is_completed))
            params['is_completed'] = int(is_completed)

        limit = kwargs.get('limit', None)
        if limit:
            params['limit'] = int(limit)

        normalize_param(kwargs, params, 'created_by', 'created_by', models.User)
        normalize_param(kwargs, params, 'milestone', 'milestone_id',
                        models.Milestone, models.SubMilestone)
        normalize_param(kwargs, params, 'suite', 'suite_id', models.Suite)

        for run in self.api.runs_by_project_id(project_id, **params):
            yield models.Run(self, run)

    @runs.register(models.Project)
    def _runs_by_project(self, project, created_after=None, created_before=None,
                         created_by=None, is_completed=None, milestone=None,
                         suite=None, limit=None):

        for run in self.runs(project.id, created_after=created_after,
                             created_before=created_before, created_by=created_by,
                             is_completed=is_completed,
                             milestone=milestone, suite=suite, limit=limit):
            yield run

    # Section related methods
    @dispatchmethod
    def section(self):
        """
            :param section_id: int

            :returns: models.Section
        """
        return models.Section(self)

    @add.register(models.Section)
    def _section_add(self, section):
        if section.project.suite_mode != 1 and section.suite is None:
            msg = ("You must associate the Section with a TestRail Suite "
                   "if the Project is not in Single Suite mode")
            raise ValueError(msg)
        response = self.api.section_add(section.project.id, section.add_params)
        return models.Section(self, response)

    @section.register(int)
    def _section_by_id(self, section_id):
        """ Do not call directly
            Returns a models.Section object with id of ``section_id``
            :param section_id: int

            :returns: models.Section
        """
        return models.Section(self, self.api.section_by_id(section_id))

    @delete.register(models.Section)
    def _section_delete(self, section):
        self.api.section_delete(section.id)

    @update.register(models.Section)
    def _section_update(self, section):
        response = self.api.section_update(section.id, section.update_params)
        return models.Section(self, response)

    @dispatchmethod
    def sections(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return models.Section generator for the given models.Project object or project ID

            `client.sections(project)` yields sections associated with the Project instance
            `client.sections(1234)` yields sections associated with project id 1234

        :param project: models.Project object for a project that exists in TestRail
        :param project_id: int, Project ID for a project that exists in TestRail

        :raiess: NotImplementedError if called with no parameters (`client.sections()`) or
                 a parameter of an unsupported type (`client.sections(True)`)

        :yields: models.Section objects
        """
        raise NotImplementedError(const.NOTIMP.format("models.Project or int"))

    @sections.register(int)
    def _sections_by_project_id(self, project_id, suite=None):
        project = self.project(project_id)
        if project.suite_mode != 1 and suite is None:
            msg = ("The project with ID {0} is set to a suite_mode of {1}, which "
                   "requires a valid suite or suite_id to retrieve sections")
            raise TypeError(msg.format(project, project.suite_mode))

        if suite and not isinstance(suite, (int, models.Suite)):
            msg = ("``suite`` must be a models.Suite object, or int ID of a "
                   "suite in testrail. Found {0}")
            raise TypeError(msg.format(suite))

        suite_id = suite.id if isinstance(suite, models.Suite) else suite

        for section in self.api.sections_by_project_id(project_id, suite_id):
            yield models.Section(self, section)

    @sections.register(models.Project)
    def _sections_by_project(self, project, suite=None):
        for section in self.sections(project.id, suite):
            yield section

    # Status related methods
    @dispatchmethod
    def custom_status(self, *args, **kwargs):
        """
            :param custom_status_id: int, from 1 to 7

            :returns: models.Status
        """
        raise NotImplementedError(const.NOTIMP.format("int"))

    @custom_status.register(int)
    def _custom_status_by_id(self, custom_status_id):
        """ Do not call directly
            Returns a models.Status object with id of ``custom_status_id`` + 5
            :param status_id: int, from 1 to 7

            :returns: models.Status

            :raises: TRAWClientError if no matching status is found
        """
        for sys_status in self.statuses():
            if sys_status.id == 5 + custom_status_id:
                status = sys_status
                break
        else:
            msg = "There is no active custom status associated with custom status ID {0}"
            raise UnknownCustomStatusError(msg.format(custom_status_id))

        return status

    @custom_status.register(str)
    def _custom_status_by_name(self, custom_status_str):
        """ Do not call directly
            Returns a models.Status object with name of ``custom_status_str``
            ``custom_status_str`` must have format of `custom_statusX`, where X is
                between 1 and 7

            :param custom_status_str: str

            :returns: models.Status

            :raises: TRAWClientError if custom_status_str is isnt formated correctly
            :raises: TRAWClientError if no matching status is found
        """
        if (not custom_status_str.startswith('custom_status') or
                custom_status_str[-1] not in '1234567'):
            msg = ("custom_status_str must be of format 'custom_statusX', where X "
                   "is between 1 and 7. Found {0}")
            raise UnknownCustomStatusError(msg.format(custom_status_str))

        # str: custom_status6 -> int: 6
        custom_status_id = int(custom_status_str.split('custom_status')[1])
        return self.custom_status(custom_status_id)

    @dispatchmethod
    def status(self):
        """
            :param status_id: int

            :returns: models.Status
        """
        raise NotImplementedError(const.NOTIMP.format("int"))

    @status.register(int)
    def _status_by_id(self, status_id):
        """ Do not call directly
            Returns a models.Status object with id of ``status_id``
            :param status_id: int

            :returns: models.Status
        """
        for sys_status in self.statuses():
            if sys_status.id == status_id:
                status = sys_status
                break
        else:
            msg = "Could not locate a models.Status with id of {0}"
            raise TRAWClientError(msg.format(status_id))

        return status

    @status.register(str)
    def _status_by_label(self, label, strict=False):
        """ Do not call directly
            Returns a models.Status object with label of ``label``
            :param label: str
            :param strict: bool, matches case if true, ignores case if false

            :returns: models.Status
        """
        for sys_status in self.statuses():
            if strict:
                if label == sys_status.label:
                    status = sys_status
                    break
                else:
                    continue  # pragma: no cover
            elif label.lower() == sys_status.label.lower():
                status = sys_status
                break
        else:
            msg = "Could not locate a models.Status with label of {0}"
            raise TRAWClientError(msg.format(label))

        return status

    def statuses(self):
        """ Returns models.Status generator

        :yields: models.Status Objects
        """
        for status in list(self.api.statuses()):
            yield models.Status(self, status)

    # Suite related methods
    @dispatchmethod
    def suite(self):
        """
            :param suite_id: int

            :returns: models.Suite
        """
        return models.Suite(self)

    @add.register(models.Suite)
    def _suite_add(self, suite):
        response = self.api.suite_add(suite.project.id, suite.add_params)
        return models.Suite(self, response)

    @suite.register(int)
    def _suite_by_id(self, suite_id):
        """ Do not call directly
            Returns a models.Suite object with id of ``suite_id``
            :param suite_id: int

            :returns: models.Suite
        """
        return models.Suite(self, self.api.suite_by_id(suite_id))

    @delete.register(models.Suite)
    def _suite_delete(self, suite):
        self.api.suite_delete(suite.id)

    @update.register(models.Suite)
    def _suite_update(self, suite):
        response = self.api.suite_update(suite.id, suite.update_params)
        return models.Suite(self, response)

    @dispatchmethod
    def suites(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return models.Suite generator for the given models.Project object or project ID

            `client.suites(project)` yields suites associated with the Project instance
            `client.suites(1234)` yields suites associated with project id 1234

        :param project: models.Project object for a project that exists in TestRail
        :param project_id: int, Project ID for a project that exists in TestRail

        :raiess: NotImplementedError if called with no parameters (`client.suites()`) or
                 a parameter of an unsupported type (`client.suites(True)`)

        :yields: models.Suite objects
        """
        raise NotImplementedError(const.NOTIMP.format("models.Project or int"))

    @suites.register(int)
    def _suites_by_project_id(self, project_id):
        for suite in self.api.suites_by_project_id(project_id):
            yield models.Suite(self, suite)

    @suites.register(models.Project)
    def _suites_by_project(self, project):
        for suite in self.suites(project.id):
            yield suite

    # Template related methods
    @dispatchmethod
    def template(self):
        """
            :param template_id: int

            :returns: models.Template
        """
        raise NotImplementedError(const.NOTIMP.format("int"))

    @template.register(int)
    def _template_by_id(self, template_id):
        """ Do not call directly
            Returns a models.Template object with id of ``template_id``
            :param template_id: int

            :returns: models.Template
        """
        for project in self.projects():
            for sys_template in self.templates(project):
                if sys_template.id == template_id:
                    template = sys_template
                    break
            else:  # Necessary to break out of both for loops
                continue
            break
        else:
            msg = "Could not locate a models.Template with id of {0}"
            raise TRAWClientError(msg.format(template_id))

        return template

    @dispatchmethod
    def templates(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return models.Template generator for the given models.Project object or project ID

            `client.templates(project)` yields templates associated with the Project instance
            `client.templates(1234)` yields templates associated with project id 1234

        :param project: models.Project object for a project that exists in TestRail
        :param project_id: int, Project ID for a project that exists in TestRail

        :raiess: NotImplementedError if called with no parameters (`client.templates()`)

        :yields: models.Template objects
        """
        raise NotImplementedError(const.NOTIMP.format("models.Project or int"))

    @templates.register(int)
    def _templates_by_project_id(self, project_id):
        for template in list(self.api.templates(project_id)):
            yield models.Template(self, template)

    @templates.register(models.Project)
    def _templates_by_project(self, project):
        for template in self.templates(project.id):
            yield template

    # Test related methods
    @dispatchmethod
    def test(self):
        """
            :param test_id: int

            :returns: models.Test
        """
        raise NotImplementedError(const.NOTIMP.format("int"))

    @test.register(int)
    def _test_by_id(self, test_id):
        """ Do not call directly
            Returns a models.Test object with id of ``test_id``
            :param test_id: int

            :returns: models.Test
        """
        return models.Test(self, self.api.test_by_id(test_id))

    @dispatchmethod
    def tests(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return models.Test generator for the given models.Run object or run ID

            `client.tests(run)` yields tests associated with the Run instance
            `client.tests(1234)` yields tests associated with run id 1234

        :param run: models.Run object for a run that exists in TestRail
        :param run_id: int, Run ID for a run that exists in TestRail

        :raiess: NotImplementedError if called with no parameters (`client.tests()`) or
                 a parameter of an unsupported type (`client.tests(True)`)

        :yields: models.Test objects
        """
        raise NotImplementedError(const.NOTIMP.format("models.Run or int"))

    @tests.register(int)
    def _tests_by_run_id(self, run_id, with_status=None):
        msg = ("`with_status` must be either None, models.Status or an iterable of "
               "models.Status objects. Found {0}")
        if with_status is None:
            pass
        elif not isinstance(with_status, (models.Status, Iterable)):
            raise TypeError(msg.format(type(with_status)))
        elif (isinstance(with_status, Iterable) and
                not all([isinstance(s, models.Status) for s in with_status])):
            # TODO: This will exhaust generators, tee them first?
            raise TypeError(msg.format([type(s) for s in with_status]))

        if with_status is not None:
            with_status = with_status if isinstance(with_status, Iterable) else (with_status, )
            with_status = ','.join([str(s.id) for s in with_status])

        for test in list(self.api.tests_by_run_id(run_id, with_status)):
            yield models.Test(self, test)

    @tests.register(models.Run)
    def _tests_by_run(self, run, with_status=None):
        for test in self.tests(run.id, with_status):
            yield test

    # User related methods
    @dispatchmethod
    def user(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return a models.User instance
            `client.user()` returns a new User instance (no API call)
            `client.user(1234)` returns a User instance with an ID of 1234
            `client.user('user@email.com')` returns a User instance the user
                who has the email user@email.com

        :param: no method parameters, will return a new, uncofigured User instance
        :param email: str, email of a user that exists in TestRail
        :param user_id: int, User ID for a user that exists in TestRail

        :returns: models.User instance
        """
        return models.User(self)

    @user.register(str)
    def _user_by_email(self, email):
        """ Do not call directly
            Returns user associated with ``email``
        """
        if '@' not in email:
            raise ValueError('"email" must be a string that includes an "@" symbol')

        return models.User(self, self.api.user_by_email(email))

    @user.register(int)
    def _user_by_id(self, user_id):
        """ Do not call directly
            Returns user with ``user_id``
        """
        return models.User(self, self.api.user_by_id(user_id))

    def users(self):
        """ Returns a models.User generator that yields all Users

        :yields: models.User Objects
        """
        for user in list(self.api.users()):
            yield models.User(self, user)

    # Cache control related methods
    def change_cache_timeout(self, new_timeout, model_cls=None):
        """ Change the cache invalidation timeout for `model_cls` to
            ``new_timeout``. If ``model_cls`` is not specified, the cache
            invalidation timeout for ALL TRAW models will be changed to
            ``new_timeout``.

        .. code-block:: python

            # Change all caches timeouts to 30 seconds
            client.change_cache_timeout(30)

            # Change Project related cache timeouts to 30 seonds, leaving others untouched
            client.change_cache_timeout(30, models.Project)

        """
        if model_cls:
            if not issubclass(model_cls, ModelBase):
                msg = ("Expected model_cls to be a subclass of "
                       "traw.models.model_base.ModelBase, found class of type {0}")
                raise TypeError(msg.format(model_cls))

            self.api.cache_timeouts[self.api][model_cls] = int(new_timeout)
        else:
            for cls_name in models.__all__:
                cls = getattr(models, cls_name)
                self.api.cache_timeouts[self.api][cls] = int(new_timeout)

    @dispatchmethod
    def clear_cache(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Clear object caches

        Clear client side caching for a specific object type, or for all caches:

        .. code-block:: python

            client.clear_cache()  # Clears all caches
            client.clear_cache(models.Project)  # Clears all Project related caches

        """
        self._clear_cache_case(None)
        self._clear_cache_case_types(None)
        self._clear_cache_config_groups(None)
        self._clear_cache_milestone(None)
        self._clear_cache_plan(None)
        self._clear_cache_priority(None)
        self._clear_cache_project(None)
        self._clear_cache_result(None)
        self._clear_cache_run(None)
        self._clear_cache_section(None)
        self._clear_cache_status(None)
        self._clear_cache_suite(None)
        self._clear_cache_template(None)
        self._clear_cache_test(None)
        self._clear_cache_user(None)

    @clear_cache.register(models.Case)
    def _clear_cache_case(self, _):
        """ Clear cache for models.Case related API methods """
        self.api.case_by_id.cache.clear()
        self.api.cases_by_project_id.cache.clear()

    @clear_cache.register(models.CaseType)
    def _clear_cache_case_types(self, _):
        """ Clear cache for models.CaseType related API methods """
        self.api.case_types.cache.clear()

    @clear_cache.register(models.ConfigGroup)
    def _clear_cache_config_groups(self, _):
        """ Clear cache for models.ConfigGroup related API methods """
        self.api.config_groups.cache.clear()

    @clear_cache.register(models.Milestone)
    def _clear_cache_milestone(self, _):
        """ Clear cache for models.Milestone related API methods """
        self.api.milestone_by_id.cache.clear()
        self.api.milestones.cache.clear()

    @clear_cache.register(models.Plan)
    def _clear_cache_plan(self, _):
        """ Clear cache for models.Plan related API methods """
        self.api.plan_by_id.cache.clear()

    @clear_cache.register(models.Priority)
    def _clear_cache_priority(self, _):
        """ Clear cache for models.Priority related API methods """
        self.api.priorities.cache.clear()

    @clear_cache.register(models.Project)
    def _clear_cache_project(self, _):
        """ Clear cache for models.Project related API methods """
        self.api.project_by_id.cache.clear()
        self.api.projects.cache.clear()

    @clear_cache.register(models.Result)
    def _clear_cache_result(self, _):
        """ Clear cache for models.Result related API methods """
        self.api.results_by_run_id.cache.clear()
        self.api.results_by_test_id.cache.clear()

    @clear_cache.register(models.Run)
    def _clear_cache_run(self, _):
        """ Clear cache for models.Run related API methods """
        self.api.run_by_id.cache.clear()
        self.api.runs_by_project_id.cache.clear()

    @clear_cache.register(models.Section)
    def _clear_cache_section(self, _):
        """ Clear cache for models.Section related API methods """
        self.api.section_by_id.cache.clear()
        self.api.sections_by_project_id.cache.clear()

    @clear_cache.register(models.Status)
    def _clear_cache_status(self, _):
        """ Clear cache for models.Status related API methods """
        self.api.statuses.cache.clear()

    @clear_cache.register(models.Suite)
    def _clear_cache_suite(self, _):
        """ Clear cache for models.Suite related API methods """
        self.api.suite_by_id.cache.clear()
        self.api.suites_by_project_id.cache.clear()

    @clear_cache.register(models.Template)
    def _clear_cache_template(self, _):
        """ Clear cache for models.Template related API methods """
        self.api.templates.cache.clear()

    @clear_cache.register(models.Test)
    def _clear_cache_test(self, _):
        """ Clear cache for models.Test related API methods """
        self.api.test_by_id.cache.clear()
        self.api.tests_by_run_id.cache.clear()

    @clear_cache.register(models.User)
    def _clear_cache_user(self, _):
        """ Clear cache for models.User related API methods """
        self.api.user_by_email.cache.clear()
        self.api.user_by_id.cache.clear()
        self.api.users.cache.clear()


def normalize_dt_filter(kwargs, params, key):
    kw_val = kwargs.get(key, None)
    if kw_val is None:
        pass
    elif kw_val and not isinstance(kw_val, (int, float, dt)):
        msg = ("`created/updated after/before` must be a datetime.datetime "
               "object or UNIX timestamp (1469726522 or 1469726522.10. Found {0}")
        raise TypeError(msg.format(kw_val))
    elif isinstance(kw_val, (int, float)):
        filter_timestamp = int(kw_val)
    else:
        filter_timestamp = int(time.mktime(kw_val.timetuple()))

    if kw_val:
        params[key] = filter_timestamp


# def normalize_param(param_name, param_vals, param_types, iter_types):
def normalize_param(kwargs, params, kw_key, param_key, *model_types):

    param_types = (int, type(None), Iterable) + model_types
    iter_types = (int, ) + model_types

    param_types_str = ' or '.join(map(str, param_types))
    iter_types_str = " or ".join(map(str, iter_types))
    kwarg_vals = kwargs.get(kw_key, None)
    msg = ("`{kw_key}` must be {param_types} types. "
           "Each object returned from the `{kw_key}` interable can "
           " only be of type {iter_types}. Found '{kwarg_vals}'")

    msg = msg.format(param_types=param_types_str, iter_types=iter_types_str,
                     kw_key=kw_key, kwarg_vals=kwarg_vals)

    if not isinstance(kwarg_vals, param_types):
        raise TypeError(msg)
    elif isinstance(kwarg_vals, ModelBase):
        kwarg_vals = kwarg_vals.id
    elif isinstance(kwarg_vals, Iterable):
        expanded_vals = list()
        for val in kwarg_vals:
            if not isinstance(val, iter_types):
                raise TypeError(msg)
            elif isinstance(val, int):
                expanded_vals.append(val)
            else:
                expanded_vals.append(val.id)

        kwarg_vals = expanded_vals

    if kwarg_vals is not None:
        kwarg_vals = kwarg_vals if isinstance(kwarg_vals, Iterable) else (kwarg_vals, )
        kwarg_vals = ','.join([str(v) for v in kwarg_vals])

    if kwarg_vals:
        params[param_key] = kwarg_vals
