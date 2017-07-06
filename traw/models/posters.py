class Addable(object):
    """  """
    @property
    def add_params(self):
        """ Returns params necessary to add the subclass object to TestRail """
        return {field: self._content.get(field, None) for field in self.ADDABLE_FIELDS}


class Updatable(object):
    """  """
    @property
    def update_params(self):
        """ Returns params necessary to update the subclass object in TestRail """
        return {field: self._content.get(field, None) for field in self.UPDATABLE_FIELDS}
