"""Unittests for tsmock."""

# pylint: disable=protected-access, redefined-outer-name, unused-argument

import threading
import time
from unittest.mock import MagicMock

import pytest
from tsmock import thread_safe_mocks, thread_unsafe_mocks, MagicMock as TSMagicMock


@pytest.fixture
def gcm_patch():
    """Emulate a slow _get_child_mock function."""
    old_gcm = MagicMock._get_child_mock

    def slow_gcm(*arg, **kw):
        time.sleep(0.1)
        return old_gcm(*arg, **kw)

    MagicMock._get_child_mock = slow_gcm

    yield

    MagicMock._get_child_mock = old_gcm


@pytest.mark.parametrize("passing", [2, 1, 0])
def test_call_func(gcm_patch, passing):
    """Test calling the mock in parallel, with a slow gcm."""
    nb_threads = 10

    if passing == 1:
        thread_safe_mocks()
        mock = MagicMock()
    elif passing == 0:
        thread_unsafe_mocks()
        mock = MagicMock()
    else:
        thread_unsafe_mocks()
        mock = TSMagicMock()

    threads = []
    event = threading.Event()
    for _ in range(nb_threads):
        thread = threading.Thread(target=lambda: (event.wait(), mock.func.call_count))
        threads.append(thread)
        thread = threading.Thread(target=lambda: (event.wait(), mock.func()))
        threads.append(thread)

    for thread in threads:
        thread.start()

    event.set()

    for thread in threads:
        thread.join()

    if passing != 0:
        assert mock.func.call_count == nb_threads
    else:
        assert mock.func.call_count != nb_threads
