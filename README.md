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

### Example of an atomic mock:

![image](https://user-images.githubusercontent.com/50769/226943776-9eb18323-55ac-4a82-80ca-334f68d3d3ec.png)
