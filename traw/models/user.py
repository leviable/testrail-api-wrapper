from .model_base import ModelBase


class User(ModelBase):
    """ Object model for TestRail Users

    To get all users

    .. code-block:: python

        users = traw_client.users()

    """
    @property
    def email(self):
        """ The email address of the user as configured in TestRail """
        return self._content.get('email', None)

    @property
    def is_active(self):
        """ True if the user is active and false otherwise """
        return self._content.get('is_active', None)

    @property
    def name(self):
        """ The full name of the user """
        return self._content.get('name', None)
