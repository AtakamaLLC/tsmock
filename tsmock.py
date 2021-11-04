"""
Drop in thread safe version of unittest mocking library.
"""

# pylint: disable=protected-access, unused-wildcard-import, arguments-differ, function-redefined

import threading
from unittest.mock import *  # pylint: disable=wildcard-import
import unittest.mock

# monkey patch mode

_OLD_GETATTR = unittest.mock.NonCallableMock.__getattr__


def thread_safe_mocks():
    """Change all mocks to use locks when inserting new functions into their dicts."""
    unittest.mock.NonCallableMock._mock_lock = threading.RLock()

    def locked_getattr(obj, *arg, **kw):
        with obj._mock_lock:
            return _OLD_GETATTR(obj, *arg, **kw)

    unittest.mock.NonCallableMock.__getattr__ = locked_getattr


def thread_unsafe_mocks():
    """Restore all mocks to original behavior."""
    unittest.mock.NonCallableMock._mock_lock = threading.RLock()
    unittest.mock.NonCallableMock.__getattr__ = _OLD_GETATTR


# derived class mode


class MagicMock(unittest.mock.MagicMock):
    """Threadsafe version of unittest.mock.MagicMock."""
    _mock_lock = threading.RLock()

    def __getattr__(self, *args, **kws):
        with self._mock_lock:
            return super().__getattr__(*args, **kws)


class NonCallableMock(unittest.mock.NonCallableMock):
    """Threadsafe version of unittest.mock.NonCallableMock."""
    _mock_lock = threading.RLock()

    def __getattr__(self, *args, **kws):
        with self._mock_lock:
            return super().__getattr__(*args, **kws)


class Mock(unittest.mock.Mock):
    """Threadsafe version of unittest.mock.Mock."""
    _mock_lock = threading.RLock()

    def __getattr__(self, *args, **kws):
        with self._mock_lock:
            return super().__getattr__(*args, **kws)


class PropertyMock(unittest.mock.PropertyMock):
    """Threadsafe version of unittest.mock.PropertyMock."""
    _mock_lock = threading.RLock()

    def __getattr__(self, *args, **kws):
        with self._mock_lock:
            return super().__getattr__(*args, **kws)


# export everything, with our changes
__all__ = unittest.mock.__all__
__all__ += ("thread_safe_mocks", "thread_unsafe_mocks")
