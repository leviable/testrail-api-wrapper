from datetime import datetime as dt, timedelta

from .. import const
from .case_type import CaseType
from .milestone import Milestone
from .model_base import ModelBase
from .posters import Addable, Deleteable, Updatable
from .priority import Priority
from .section import Section
from .suite import Suite
from .template import Template
from ..utils import duration_to_timedelta as dur_to_td


class Case(Addable, Deleteable, Updatable, ModelBase):
    """ Object model for TestRail Cases

    To create new case

    .. code-block:: python

        new_case = traw_client.case()
        new_case.title = "My new TestRail Case"
        new_case.section = section

        case = client.add(new_case)

    """
    _ADDABLE_FIELDS = const.CASE_ADD_FIELDS
    _UPDATABLE_FIELDS = const.CASE_UPDATE_FIELDS

    @property
    def created_by(self):
        """ The user who created the test case """
        user_id = self._content.get('created_by', None)
        return self.client.user(user_id) if user_id is not None else None

    @property
    def created_on(self):
        """ The date/time when the test case was created
            (as datetime.datetime object)
        """
        co = self._content.get('created_on', None)
        return dt.fromtimestamp(co) if co is not None else None

    @property
    def estimate(self):
        """ The estimated duration of the test case, e.g. "30s" or "1m 45s" """
        est = self._content.get('estimate', None)
        return dur_to_td(est) if est is not None else None

    @estimate.setter
    def estimate(self, val):
        if not isinstance(val, timedelta):
            raise TypeError(const.SETTER_ERR.format(timedelta, type(val)))
        self._content['estimate'] = val.seconds

    @property
    def estimate_forecast(self):
        """ The forecasted, estimated duration of the test case,
            e.g. "30s" or "1m 45s"
        """
        est_forecast = self._content.get('estimate_forecast', None)
        return dur_to_td(est_forecast) if est_forecast is not None else None

    @property
    def milestone(self):  # TODO: find out why API returns only None
        """ The  milestone this test case belongs to """
        milestone_id = self._content.get('milestone_id', None)
        return self.client.milestone(milestone_id) if milestone_id is not None else None

    @milestone.setter
    def milestone(self, val):
        if not isinstance(val, Milestone):
            raise TypeError(const.SETTER_ERR.format(Milestone, type(val)))
        self._content['milestone_id'] = val.id

    @property
    def priority(self):  # TODO: find out why API returns only None
        """ The  priority that is linked to the test case """
        priority_id = self._content.get('priority_id', None)
        return self.client.priority(priority_id) if priority_id is not None else None

    @priority.setter
    def priority(self, val):
        if not isinstance(val, Priority):
            raise TypeError(const.SETTER_ERR.format(Priority, type(val)))
        self._content['priority_id'] = val.id

    @property
    def refs(self):
        """ Yields string references/requirements that are linked to the
            test case
        """
        refs_raw = self._content.get('refs', None)
        refs = refs_raw.split(',') if refs_raw is not None else list()

        for ref in refs:
            yield ref

    @refs.setter
    def refs(self, val):
        """ Add references/requirements associated with the test case

            Refs can be added as follows:
             - A reference string: ``result.refs = "REF01"``
             - A comma separated string: ``result.refs = "REF01,REF02"
             - A list of reference strings: ["REF01", "REF02"]
        """
        if isinstance(val, str):
            refs_ = val
        elif isinstance(val, list) and all(map(lambda x: isinstance(x, str), val)):
            refs_ = ','.join(val)
        else:
            msg = ("References must be either a single string of one or more "
                   "comma separated references ('REF01' or 'REF01,REF02') or "
                   "a list of reference strings (['REF01', 'REF02']). Found {0}")
            raise TypeError(msg.format(val))

        self._content['refs'] = refs_

    @property
    def section(self):
        """ The section that the test case belongs to """
        section_id = self._content.get('section_id', None)
        return self.client.section(section_id) if section_id is not None else None

    @section.setter
    def section(self, val):
        if not isinstance(val, Section):
            raise TypeError(const.SETTER_ERR.format(Section, type(val)))
        self._content['section_id'] = val.id

    @property
    def suite(self):
        """ The suite that the test case belongs to """
        suite_id = self._content.get('suite_id', None)
        return self.client.suite(suite_id) if suite_id is not None else None

    @suite.setter
    def suite(self, val):
        if not isinstance(val, Suite):
            raise TypeError(const.SETTER_ERR.format(Suite, type(val)))
        self._content['suite_id'] = val.id

    @property
    def template(self):
        """ The template that the test case uses """
        template_id = self._content.get('template_id', None)
        return self.client.template(template_id) if template_id is not None else None

    @template.setter
    def template(self, val):
        if not isinstance(val, Template):
            raise TypeError(const.SETTER_ERR.format(Template, type(val)))
        self._content['template_id'] = val.id

    @property
    def title(self):
        """ The title of the test case """
        return self._content.get('title', None)

    @title.setter
    def title(self, val):
        if not isinstance(val, str):
            raise TypeError(const.SETTER_ERR.format(str, type(val)))
        self._content['title'] = val

    @property
    def case_type(self):
        """ The case type that is linked to the test case """
        type_id = self._content.get('type_id', None)
        return self.client.case_type(type_id) if type_id is not None else None

    @case_type.setter
    def case_type(self, val):
        if not isinstance(val, CaseType):
            raise TypeError(const.SETTER_ERR.format(CaseType, type(val)))
        self._content['type_id'] = val.id

    @property
    def updated_by(self):
        """ The user who updated the test case """
        user_id = self._content.get('updated_by', None)
        return self.client.user(user_id) if user_id is not None else None

    @property
    def updated_on(self):
        """ The date/time when the test case was updated
            (as datetime.datetime object)
        """
        co = self._content.get('updated_on', None)
        return dt.fromtimestamp(co) if co is not None else None
