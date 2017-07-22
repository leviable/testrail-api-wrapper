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
from pbr.version import VersionInfo

from .client import Client  # NOQA


__version__ = VersionInfo('traw').semantic_version().release_string()
__all__ = ('__version__', 'Client')
