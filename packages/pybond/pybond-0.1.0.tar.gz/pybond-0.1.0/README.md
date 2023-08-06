# pybond

`pybond` is a spying and stubbing library inspired heavily by the
[clojure `bond` library](https://github.com/circleci/bond/).

```python
# src/my_module.py
from typing import Any
from other_package import make_a_network_request, write_to_disk


def foo(x: Any) -> None:
    response = make_a_network_request(x)
    write_to_disk(response)
    return response


def bar(x: Any) -> None:
    return foo(x)
```

```python
# tests/test_my_module.py
from bond import calls, called_with_args, spy, stub, times_called

import other_package
import src.my_module
from src.my_module import bar


def test_foo_is_called():
    with spy([src.my_module, "foo"]):
        assert times_called(src.my_module.foo, 0)
        bar(42)
        assert times_called(src.my_module.foo, 1)
        bar(42)
        bar(42)
        assert times_called(src.my_module.foo, 3)


def test_bar_handles_response():
    with stub(
        [other_package, "make_a_network_request", lambda x: {"result": x * 2}],
        [other_package, "write_to_disk", lambda _: None],
    ), spy(
        [src.my_module, "foo"],
    ):
        assert times_called(src.my_module.foo, 0)
        assert times_called(other_package.make_a_network_request, 0)
        assert bar(21) == 42
        assert times_called(src.my_module.foo, 1)
        assert times_called(other_package.make_a_network_request, 1)
        assert called_with_args(src.my_module.foo, args=[21])
        assert bar(20) == 40
        assert calls(src.my_module.foo) == [
            {"args": [21] "kwargs": None "return": 42 "error": None},
            {"args": [20] "kwargs": None "return": 40 "error": None},
        ]
```

## License

Distributed under the
[Eclipse Public License](http://www.eclipse.org/legal/epl-v10.html).
