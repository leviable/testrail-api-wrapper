
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

Currently supported endpoints:

- case type      - get by case type id
- case types     - get all
- configs        - get by project or project id, add, delete, update
- config groups  - add, delete, update
- milestone      - get by milestone id, add, delete, update
- milestones     - get all by project or project id
- priority       - get by priority id
- priorities     - get all
- project        - get by project id, add, delete, udpate
- projects       - get all (with active_only and completed_only filter)
- run            - get by run id
- status         - get by status id, get by label (with strict casing filter)
- statuses       - get all
- suite          - get by suite id
- suites         - get by project or project id
- templates      - get by project or project id
- test           - get by test id
- tests          - get by run or run id (both support with_status filter)
- user           - get by user id or user email
- users          - get all


Not yet supported:

- case           - get by case id, add, delete, update
- cases          - get by project or project id (* plus suite and section)
- case fields    - get all
- plan           - get by plan id, add, close, delete, update
- plan entry     - add, delete, update
- plans          - get by project or project id
- result         - add by test id, add by run and case
- results        - get by test or test id, get by run or run id, get by run and case, get by run id and case id, add by run, add by cases
- result fields  - get all
- run            - add, close, delete, update
- runs           - get by project or project id
- section        - get by section id, add, delete, update
- sections       - get by project or project id (* and suite or suite id)

Note: * Denotes endpoint variations dependent on if the project is or is not
  operating in single suite mode
