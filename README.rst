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
    
(This project is now in beta testing: APIs will not change without a deprecation warning)

TRAW aims to be a feature complete python library for accessing TestRail's RESTful API.

Quick Reference
---------------

.. code-block:: python

    from datetime import datetime as dt
    import random
    
    import traw
    
    client = traw.Client(username='username', password='passwrod', url='url)
    
    project = client.project(15)  # Get Project with Project ID of 15
    
    new_run = client.run()
    new_run.name = "My new run name"
    new_run.description = "My new run description"
    new_run.include_all = True
    new_run.project = project
    
    run = client.add(new_run)  # Run is added to TestRail
    
    for test in client.tests(run):  # Get all tests for run
        begin = dt.now()
        
        # Do actual testing here, but lets pick a random status
        status_str = random.choice(['passed', 'failed', 'retest'])
        
        elapsed = dt.now() - begin
  
        result = client.result()
        result.test = test
        result.status = client.status(status_str)
        result.comment = "Setting {0} to {1}".format(test.title, result.status.label)
        result.elapsed = elapsed
        
        # Add the result to TestRail
        client.add(result)
        
    # Everything complete, close the run
    client.close(run)
    
    # Fín

Installation
------------
TRAW is availiable on PyPI and can be pip installed

.. code-block:: bash

    $ pip install traw    

Credentials
-----------
The TRAW Client can pull in credentials in three ways:

* Passing parameters to ``__init__`` during traw.Client instantiation

  .. code-block:: python

      client = traw.Client(username='user@email.com', password='password', url='url')
      # client = traw.Client(username='user@email.com', user_api_key='userapikey', url='url')

* Setting environment variables

  .. code-block:: bash

      $ export TRAW_USERNAME="user@email.com"
      $ export TRAW_PASSWORD="userapikey"
      $ # export TRAW_USER_API_KEY="userapikey"  # (Optional) - in place of TRAW_PASSWORD
      $ export TRAW_URL="https://example.testrail.net"

* Writing them to a configuration file in the user's home directory

  .. code-block:: bash

      $ cat ~/.traw_config
      [TRAW]
      username = <username>
      password = <password>
      # user_api_key = <user_api_key>  # (Optional) - in place of password
      url = <url>
    
You can create multiple clients to access different TestRail installations:

.. code-block:: python

    client1 = traw.Client(username='user1@email.com', password='password', url='https://example.testrail.net')
    client2 = traw.Client(username='user2@email.com', password='password', url='https://your.domain.com')
    
Creating/Adding/Closing/Deleting/Updating TestRail Objects
----------------------------------------------------------

TRAW uses a consistent pattern for creating new TestRail objects and adding them to TestRail:

* Call the relevant client method without any parameters, and a new/empty object is returned:

  .. code-block:: python

      new_run = client.run()
      new_result = client.result()
      new_section = client.section()
      new_milestone = client.milestone()
      # etc
      
* Configure the new object. Note most addable objects require at least one reference object in order for them to be added to TestRail. For instance, run objects require a reference to a project, result objects require a reference to a test, and sections objects require a reference to a project AND a suite if the project is not in single-suite mode:

  .. code-block:: python

      new_run.name = "Run Name"
      new_run.project = client.project(15)  # Project with Project ID 15
      
      new_result.comment = "Result added by TRAW"
      new_result.test = client.tests(123)  # Test with Test ID of 123
      new_result.status = client.status('passed')  # Status with Status Label of 'passed'
      
      new_section.name = "Suite Name"
      new_section.project = client.project(15)  # Project with Project ID 15, with suite-mode of 2
      new_section.suite = client.suite(456)  # Suite with Suite ID 456
      
* At this point the objects only exist locally, and have not been added to TestRail. To do so, call ``client.add()`` with the new object. TRAW will add the new object to TestRail, and upon success the TestRail API will return a new object:

  .. code-block:: python

      run = client.add(new_run)
      result = client.add(result)
      section = client.add(section)

* The returned objects will now have additional information set. Properties that have not yet been specified will be set to None:

  .. code-block:: python

      print("Run ID is: {0}".format(run.id))                           # "Run ID is: 12333"
      print("Run Name is: '{0}'".format(run.name))                     # "Run Name is: 'Run Name'"
      print("Run Created By user: '{0}'".format(run.created_by.name))  # "Run Created By user: 'Automation User'"
      print("Run Created On: '{0}'".format(run.created_on))            # "Run Created On: '2016-08-19 13:00:29'"
      print("Run Milestone: '{0}'".format(run.milestone))              # "Run Milestone: 'None'"
      
* Objects that support updating (runs, suites, milestones, etc) can be updated locally, and then the updates can be sent to TestRail:

  .. code-block:: python

      run.name = run.name + " - Updated by TRAW"
      run.milestone = client.milestone(789)
      
      updated_run = client.update(run)
      
      print("Run Name is: '{0}'".format(updated_run.name))             # "Run Name is: 'Run Name - Updated by TRAW'"
      print("Run Milestone: '{0}'".format(updated_run.milestone))      # "Run Milestone: 'Widget Testing 90% Complete'"
      print("Run Complete: '{0}'".format(updated_run.is_completed))    # "Run Completed: 'False'"
      
* Objects that can be closed (runs, plans) can be closed through the TRAW Client:

  .. code-block:: python

      closed_run = client.close(run)
      
      print("Run Complete: '{0}'".format(closed_run.is_completed))     # "Run Completed: 'True'"
      
* Objects that can be deleted (runs, plans, cases, etc) can be deleted through the TRAW Client. Note that no object is returned after calling ``client.delete()``. Also note that some things (runs, plans) can either be closed or deleted, but not both, while other things (projects) can be deleted after they have been closed (assuming your user has admin privileges):

  .. code-block:: python

      client.delete(run)


Client Side Object Caching
--------------------------

TODO

Automatic Response Pagination
-----------------------------

TODO

 

TestRail API Endpoint Coverage
==============================

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
- results        - get by run or run id, get by test or test id (with limit and with_status filters)
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
- results        - get by run and case, get by run id and case id, add by run, add by cases
- result fields  - get all
