import time

try:
    import mock
except ImportError:
    from unittest import mock


# Prevent calls to sleep
class SleepMock(object):
    def __init__(self):
        self.mock_obj = mock.MagicMock()

    def __call__(self, *args):
        self.mock_obj(*args)


time.sleep = SleepMock()
