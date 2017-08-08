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
