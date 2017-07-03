from .model_base import ModelBase


class CaseField(ModelBase):
    """ Object model for custom TestRail Case Fields

    To get all case fields

    .. code-block:: python

        case_fields = list(traw_client.case_fields())

    Case Field type_id's can be any of the following:
        1	String
        2	Integer
        3	Text
        4	URL
        5	Checkbox
        6	Dropdown
        7	User
        8	Date
        9	Milestone
        10	Steps
        12	Multi-select

    Note that only 'Custom' case fields are returned here. Case fields listed
    as 'System' (Estimate, Milestone, References) are not returned

    """
    @property
    def configs(self):
        """ Returns a list of configurations for the case field """
        return list(map(Config, self._content.get('configs')))

    @property
    def description(self):
        """ Description of the case field """
        return self._content.get('description')

    @property
    def display_order(self):
        """ The display order of the case field """
        return self._content.get('display_order')

    @property
    def label(self):
        """ The displayed label for the case field (e.g. 'Preconditions') """
        return self._content.get('label')

    @property
    def name(self):
        """ The name of the case field (e.g. 'preconds') """
        return self._content.get('name')

    @property
    def system_name(self):
        """ The testrail system name of the case field (e.g. 'custom_preconds') """
        return self._content.get('system_name')

    @property
    def type_id(self):
        """ The case field type_id (i.e. type_id of 4 indicates a URL) """
        return self._content.get('type_id')


class Config(object):
    """ Config object model for Case Field configs """
    def __init__(self, config):
        self._config = config

    @property
    def context(self):
        return Context(self._config.get('context'))

    @property
    def id(self):
        return self._config.get('id')

    @property
    def options(self):
        return Options(self._config.get('options'))


class Context(object):
    """ Context object model for Case Field config contexts """
    def __init__(self, context):
        self._context = context

    @property
    def is_global(self):
        return self._context.get('is_global')

    @property
    def project_ids(self):
        return self._context.get('project_ids')


class Options(object):
    """ Context object model for Case Field config options """
    def __init__(self, options):
        self._options = options

    @property
    def default_value(self):
        return self._options.get('default_value')

    @property
    def is_required(self):
        return self._options.get('is_required')
