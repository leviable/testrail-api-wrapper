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
