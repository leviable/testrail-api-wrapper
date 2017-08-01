
TRAW: TestRail API Wrapper
==========================

|PyPIVersion| |TravisCI| |CoverageStatus| |CodeHealth| |PythonVersions|

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
    
This project is now in beta testing: APIs will not change without a deprecation warning

TRAW is availiable on PyPI and can be pip installed

.. code-block:: bash

    $ pip install traw
    
Using TRAW:

.. code-block:: python

    import traw

    # Instantiate the TRAW client
    # Note that you can use also specify credentials using environment vars
    # or a configuration file
    client = traw.Client(username='<username>', password='<password>', url='<url')
    
    # Locate the target project by project ID
    automation_project = client.project(15)  # This makes a call to the TestRail API and returns
                                             # project with ID 15

    # Add a new suite to this project
    # Only Projects configured for multi suite mode can have new suites added
    assert automation_project.suite_mode == 3
    
    # First create a new suite object
    new_suite = client.suite()  # Parameterless calls to most non-plural client methods will return a
                                # new instance of that type. A new Suite instance in this case.
                                
    # The suite name and description and associated project must be set
    new_suite.name = "My new Automation suite"
    new_suite.description = "This new suite was added via the TRAW client"
    new_suite.project = automation_project
    
    # Note that new_suite doesn't have an ID, as it hasn't been added to TestRail yet
    assert new_suite.id is None

    # Use the client to add the suite to testrail
    suite = client.add(new_suite)  # TRAW returns an updated Suite instance with additional parameters
                                   # that were returned from TestRail after the suite was added
                                   
    # Now our suite matches new_suite, but has an ID
    assert suit.name == new_suite.name
    assert suite.description == new_suite.description
    assert suite.id is not None
    
Additional, more comprehensive examples are available in the `examples folder`_.

.. _examples folder: examples/
   

Currently supported endpoints:

- case           - get by case id
- cases          - get by project or project id (with suite, section, case_type, created after/before/by, milestone, priority, template, and updated after/before/by filters )
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
- result         - add by test id
- results        - get by test or test id (with limit and with_status filters)
- run            - get by run id, add, close, delete, update
- runs           - get by project or project id (with created after/before/by, is completed, limit, milestone, and suite filters)
- status         - get by status id, get by label (with strict casing filter)
- statuses       - get all
- section        - get by section id, add, delete, update
- sections       - get by project or project id (optionally by suite or suite id)
- suite          - get by suite id
- suites         - get by project or project id
- templates      - get by project or project id
- test           - get by test id
- tests          - get by run or run id (both support with_status filter)
- user           - get by user id or user email
- users          - get all


Not yet supported:

- case           - add, delete, update
- case fields    - get all
- plan           - get by plan id, add, close, delete, update
- plan entry     - add, delete, update
- plans          - get by project or project id
- result         - add by run and case
- results        - get by run or run id, get by run and case, get by run id and case id, add by run, add by cases
- result fields  - get all
