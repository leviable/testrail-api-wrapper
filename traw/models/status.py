from .model_base import ModelBase


class Status(ModelBase):
    """ Object model for TestRail Statuses

    To get all statuses

    .. code-block:: python

        statuses = list(traw_client.statuses())

    """
    @property
    def color_bright(self):
        """ The brightest shade of the status """
        return self._content.get('color_bright')

    @property
    def color_dark(self):
        """ The darkest shade of the status """
        return self._content.get('color_dark')

    @property
    def color_medium(self):
        """ The middle shade of the status """
        return self._content.get('color_medium')

    @property
    def is_final(self):
        """ True if this is a final status (e.g. not an intermediary status) """
        return self._content.get('is_final')

    @property
    def is_system(self):
        """ True if this is a system status (e.g. not a custom status) """
        return self._content.get('is_system')

    @property
    def is_untested(self):
        """ True if the status indicates an untested state """
        return self._content.get('is_untested')

    @property
    def label(self):
        """ The displayed label of the status """
        return self._content.get('label', None)

    @property
    def name(self):
        """ The name of the status """
        return self._content.get('name', None)
