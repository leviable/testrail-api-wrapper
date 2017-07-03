from .model_base import ModelBase


class Priority(ModelBase):
    """ Object model for TestRail Priorities

    To get priorities

    .. code-block:: python

        priorities = list(traw_client.priorities())

    """
    @property
    def is_default(self):
        """ Reports if priority is default """
        return self._content.get('is_default')

    @property
    def name(self):
        """ The (long) name of the priority: `1 - Don't Test`"""
        return self._content.get('name')

    @property
    def priority(self):
        """ The priority number """
        return self._content.get('priority')

    @property
    def short_name(self):
        """ The short name of the priority: `1 - Don't` """
        return self._content.get('short_name')
