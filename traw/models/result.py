from datetime import datetime as dt, timedelta

from .. import const
from .model_base import ModelBase
from .posters import Addable
from .status import Status
from .test import Test
from .user import User
from ..utils import duration_to_timedelta as dur_to_td


class Result(Addable, ModelBase):
    """ Object model for TestRail Results

    """
    _ADDABLE_FIELDS = const.RESULT_ADD_FIELDS

    @property
    def assigned_to(self):
        """ The assignee (user) of the test result """
        user_id = self._content.get('assignedto_id', None)
        return self.client.user(user_id) if user_id is not None else None

    @assigned_to.setter
    def assigned_to(self, val):
        if not isinstance(val, User):
            raise TypeError(const.SETTER_ERR.format(User, type(val)))
        self._content['assignedto_id'] = val.id

    @property
    def comment(self):
        """ The comment or error message of the test result """
        return self._content.get('comment', None)

    @comment.setter
    def comment(self, val):
        if not isinstance(val, str):
            raise TypeError(const.SETTER_ERR.format(str, type(val)))
        self._content['comment'] = val

    @property
    def created_by(self):
        """ The user who created the test result """
        user_id = self._content.get('created_by', None)
        return self.client.user(user_id) if user_id is not None else None

    @property
    def created_on(self):
        """ The date/time when the test result was created
            (as datetime.datetime object)
        """
        co = self._content.get('created_on', None)
        return dt.fromtimestamp(co) if co is not None else None

    @property
    def defects(self):
        """ Yields string defects that are linked to the test result """
        defs_raw = self._content.get('defects', None)
        defects = defs_raw.split(',') if defs_raw is not None else list()

        for defect in defects:
            yield defect

    @defects.setter
    def defects(self, val):
        """ Add defects associated with the test result

            Defects can be added as follows:
             - A defect string: ``result.defects = "DEFECT1"``
             - A comma separated string: ``result.defects = "DEFECT1,DEFECT2"
             - A list of defect strings: ["DEFECT1", "DEFECT2"]
        """
        if isinstance(val, str):
            defects_ = val
        elif isinstance(val, list) and all(map(lambda x: isinstance(x, str), val)):
            defects_ = ','.join(val)
        else:
            msg = ("Defects must be either a single string of one or more comma "
                   "separated defects ('DEFECT1' or 'DEFECT1,DEFECT2') or a list "
                   "of defect strings (['DEFECT1', 'DEFECT2']). Found {0}")
            raise TypeError(msg.format(val))

        self._content['defects'] = defects_

    @property
    def elapsed(self):
        """ The amount of time it took to execute the test e.g. "30s" or "1m 45s"
            (As a datetime.timedelta object)
        """
        elapsed = self._content.get('elapsed', None)
        return dur_to_td(elapsed) if elapsed is not None else None

    @elapsed.setter
    def elapsed(self, val):
        if not isinstance(val, timedelta):
            raise TypeError(const.SETTER_ERR.format(timedelta, type(val)))
        self._content['elapsed'] = val.seconds

    @property
    def status(self):
        """ The test status """
        status_id = self._content.get('status_id', None)
        return self.client.status(status_id) if status_id is not None else None

    @status.setter
    def status(self, val):
        if not isinstance(val, Status):
            raise TypeError(const.SETTER_ERR.format(Status, type(val)))
        self._content['status_id'] = val.id

    @property
    def test(self):
        """ The test this test result belongs to """
        test_id = self._content.get('test_id', None)
        return self.client.test(test_id) if test_id is not None else None

    @test.setter
    def test(self, val):
        if not isinstance(val, Test):
            raise TypeError(const.SETTER_ERR.format(Test, type(val)))
        self._content['test_id'] = val.id

    @property
    def version(self):
        """ The (build) version the test was executed against """
        return self._content.get('version', None)

    @version.setter
    def version(self, val):
        if not isinstance(val, str):
            raise TypeError(const.SETTER_ERR.format(str, type(val)))
        self._content['version'] = val
