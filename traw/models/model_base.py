class ModelBase(object):
    """ Base class for all TRAW models """
    def __init__(self, client, content=None):
        self.client = client
        self._content = content or dict()

    def __repr__(self):  # pragma: no cover
        return str(self)

    def __str__(self):  # pragma: no cover
        class_name = self.__class__.__name__
        return "{0}-{1}".format(class_name, self.id)

    @property
    def id(self):
        """ The unique ID of the project """
        return self._content.get('id', None)
