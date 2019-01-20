"""  TRAW: TestRail API Wrapper

TRAW is an API wrapper for Gurrock's TestRail test management suite

The intended way to begin is to instantiate the TRAW Client:

.. code-block:: python

    import traw
    testrail = traw.Client(username='username',
                           user_api_key='api_key',
                           url='url')

See the Client help documentation (`help(traw.Client)`) for more information
"""
import logging
from os.path import dirname, join, realpath

from .client import Client  # NOQA

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

try:
    with open(join(dirname(realpath(__file__)), 'VERSION'), 'r') as r:
        version = r.read()
except FileNotFoundError:
    version = '0.0.0'


__version__ = version
__all__ = ('__version__', 'Client')

logging.getLogger(__package__).addHandler(logging.NullHandler())
