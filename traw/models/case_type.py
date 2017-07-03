from .model_base import ModelBase


class CaseType(ModelBase):
    """ Object model for TestRail Case Types

    To get all case types

    .. code-block:: python

        case_types = list(traw_client.case_types())

    """
    @property
    def is_default(self):
        """ True if the case type is the default """
        return self._content.get('is_default', None)

    @property
    def name(self):
        """ The full name of the case type """
        return self._content.get('name', None)
