
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
- case type  - get by id
- case types - get all
- milestone  - get by id, add, delete, update
- milestones - get all by project, get all by project id
- priority   - get by id
- priorities - get all
- project    - get by id, add, delete, udpate
- projects   - get all (with active_only and completed_only filter)
- run        - get by id
- status     - get by id, get by label (by label with strict casing filter)
- statuses   - get all
- templates  - get by project, get by project id
- test       - get by test id
- tests      - get by run, by run id (both support with_status filter)
- user       - get by id, get by email
- users      - get all


Planned functionality in upcoming release(s):

- Fully support Run related APIs
- Fully support Run related API params: is_complete, limit, pagination, etc
