
TRAW: TestRail API Wrapper
==========================

|PyPIVersion| |TravisCI| |CoverageStatus| |CodeHealth| |PythonVersions|

Note that this project is currently in alpha: APIs can and will change without warning

.. |TravisCI| image:: https://travis-ci.org/levi-rs/traw.svg?branch=master
    :target: https://travis-ci.org/levi-rs/traw
.. |CoverageStatus| image:: https://coveralls.io/repos/github/levi-rs/traw/badge.svg
   :target: https://coveralls.io/github/levi-rs/traw
.. |CodeHealth| image:: https://landscape.io/github/levi-rs/traw/master/landscape.svg?style=flat
   :target: https://landscape.io/github/levi-rs/traw/master
.. |PyPIVersion| image:: https://badge.fury.io/py/traw.svg
    :target: https://badge.fury.io/py/traw
.. |PythonVersions| image:: https://img.shields.io/pypi/pyversions/traw.svg
    :target: https://wiki.python.org/moin/Python2orPython3

Currently supported functionality:

- Use credentials from Client instantiation, ENV vars, or configuration file
- case types - (get all)
- milestone (get_by_id)
- milestones (get all by project)
- priorities - (get all)
- project - (get_by_id)
- projects - (get all)
- statuses - (get all)
- templates - (get_by_project_id, get_by_project)
- user - (get_by_id, get_by_email)
- users - (get all)


Planned functionality in upcoming release(s):

- Fully support Run related APIs
- Fully support Run related API params: is_complete, limit, pagination, etc
