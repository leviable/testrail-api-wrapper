from .model_base import ModelBase
from ..utils import duration_to_timedelta as dur_to_td


class Test(ModelBase):
    """ Object model for TestRail Tests

    To get an existing test from the TestRail API:

    .. code-block:: python

        # Locate an existing test by test ID
        test = traw_client.test(1234)

    To get all tests for a run from the TestRail API:

    .. code-block:: python

        # Locate an existing run by run ID
        run = traw_client.run(4321)
        tests = traw_client.tests(run)

    """
    @property
    def assigned_to(self):
        """ The user the test is assigned to """
        user_id = self._content.get('assignedto_id', None)
        return self.client.user(user_id) if user_id is not None else None

    @property
    def case(self):
        """ The test case related to this test """
        return self.client.case(self._content['case_id'])

    @property
    def estimate(self):
        """ The estimated duration of the test, e.g. "30s" or "1m 45s" """
        est = self._content.get('estimate', None)
        return dur_to_td(est) if est is not None else None

    @property
    def estimate_forecast(self):
        """ The forecasted, estimated duration of the test, e.g. "30s" or "1m 45s" """
        est_forecast = self._content.get('estimate_forecast', None)
        return dur_to_td(est_forecast) if est_forecast is not None else None

    @property
    def milestone(self):  # TODO: find out why API returns only None
        """ The milestone that is linked to the test case """
        milestone_id = self._content.get('milestone_id', None)
        return self.client.milestone(milestone_id) if milestone_id is not None else None

    @property
    def priority(self):
        """ The priority that is linked to the test case """
        return self.client.priority(self._content['priority_id'])

    @property
    def refs(self):
        """ Yields string references/requirements that are linked to the test case """
        refs_raw = self._content.get('refs', None)
        refs = refs_raw.split(',') if refs_raw is not None else list()

        for ref in refs:
            yield ref

    @property
    def run(self):
        """ The test run that is linked to the test case """
        return self.client.run(self._content['run_id'])

    @property
    def status(self):
        """ The current test status of the test case """
        return self.client.status(self._content['status_id'])

    @property
    def title(self):
        """ The test title that is linked to the test case """
        return self._content['title']

    @property
    def type(self):
        """ The test case type that is linked to the test case """
        return self.client.case_type(self._content['type_id'])
