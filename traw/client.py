from . import const
from . import models
from .api import API
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

    # Case type related methods
    def case_types(self):
        """ Returns a case types generator

        :yields: models.CaseType Objects

        """
        for case_type in self.api.case_types():
            yield models.CaseType(self, case_type)

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

    @dispatchmethod
    def milestones(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Return models.Template generator for the given models.Project object or project ID

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
        msg = "{0} must be either None or bool, found {1}(2)"
        if not isinstance(is_completed, (type(None), bool)):
            raise TypeError(msg.format('is_completed', is_completed, type(is_completed)))
        elif not isinstance(is_started, (type(None), bool)):
            raise TypeError(msg.format('is_started', is_started, type(is_started)))

        for milestone in self.api.milestones(project_id, is_completed, is_started):
            yield models.Milestone(self, milestone)

    @milestones.register(models.Project)
    def _milestones_by_project(self, project, is_completed=None, is_started=None):
        msg = "{0} must be either None or bool, found {1}(2)"
        if not isinstance(is_completed, (type(None), bool)):
            raise TypeError(msg.format('is_completed', is_completed, type(is_completed)))
        elif not isinstance(is_started, (type(None), bool)):
            raise TypeError(msg.format('is_started', is_started, type(is_started)))

        for milestone in self.api.milestones(project.id, is_completed, is_started):
            yield models.Milestone(self, milestone)

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

    # Priorities related methods
    def priorities(self):
        """ Returns a priority generator

        :yields: models.Priority Objects
        """
        for priority in self.api.priorities():
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

    @delete.register(models.Project)
    def _project_delete(self, project):
        self.api.project_delete(project.id)

    @update.register(models.Project)
    def _project_update(self, project):
        response = self.api.project_update(project.id, project.update_params)
        return models.Project(self, response)

    @project.register(int)
    def _project_by_id(self, project_id):
        """ Do not call directly
            :param project_id: int

            :returns: models.Project
        """
        return models.Project(self, self.api.project_by_id(project_id))

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

        for project in self.api.projects(is_completed):
            yield models.Project(self, project)

    # Status related methods
    def statuses(self):
        """ Returns models.Status generator

        :yields: models.Status Objects
        """
        for status in self.api.statuses():
            yield models.Status(self, status)

    # Template related methods
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
        for template in self.api.templates(project_id):
            yield models.Template(self, template)

    @templates.register(models.Project)
    def _templates_by_project(self, project):
        for template in self.api.templates(project.id):
            yield models.Template(self, template)

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
            raise ValueError('"email" must be a string that includes an "@" sym')

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
        for user in self.api.users():
            yield models.User(self, user)
