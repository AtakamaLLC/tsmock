# tsmock

### Thread safe pything mocking wrapper around unittest.mock

Either monkey patch all mock classes:

```
from tsmock import thread_safe_mocks
thread_safe_mocks()
```

Or use a single mock class as needed:

```
from tsmock import MagicMock
```
