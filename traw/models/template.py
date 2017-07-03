from .model_base import ModelBase


class Template(ModelBase):
    """ Object model for TestRail Templates

    To get all templates for a project:

    .. code-block:: python

        target_project = traw_client.project(12)  # Get project with id 12
        templates_for_project = list(traw_client.template(target_project))

    """
    @property
    def is_default(self):
        """ True if this is a default template """
        return self._content.get('is_default')

    @property
    def name(self):
        """ The name of the template """
        return self._content.get('name')
