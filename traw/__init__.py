from pbr.version import VersionInfo

__version__ = VersionInfo('instabrade').semantic_version().release_string()

from .client import Client  # NOQA
