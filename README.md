# pytest-runtime-xfail

pytest allows you to mark tests as expected to fail, or xfail, in two ways.

1. `@pytest.mark.xfail`. This allows you to mark tests or test parametrizations as `xfail` during test collection time.
   * pytest runs tests marked with `xfail` just like any other test.
   * If the test fails, it will result in `XFAIL`. 
   * If it passes, `XPASS`. Unless you have `xfail_strict=true` or `@pytest.mark.xfail(strict=True)`, in which case, passing xfail-marked tests will result in `FAIL`.
      * This is useful to be alerted when an expected failing test starts to pass.
   
2. `pytest.xfail()`. If you need information only known at runtime to decide if `xfail` is appropriate, you can call `pytest.xfail()` during a test or fixture. 
   * pytest runs the test as normal UNTIL `pytest.xfail()` is called.
   * When `pytest.xfail()` is called, the test execution stops and the test results in `XFAIL`.
   * The rest of the test is not run.
   * There is no way to get `XPASS` from `pytest.xfail()`.
   * `xfail_strict` has no effect.


There are times where we want a combination of these behaviors.

* We don't know until runtime if we should mark a test as `xfail`.
* We want the test run.
* We want the possibility of both `XFAIL` and `XPASS` results.
* We want to be able to use `xfail_strict=true` to alert us when the test starts passing.


This plugin fills that gap.

## Installation

Install with pip:

    pip install pytest-runtime-xfail

## Usage

Include the fixture, then call it if you want to mark a test as `xfail` during runtime.

```python
 def test_something(runtime_xfail):
     if (runtime_condition):
        runtime_xfail()
     # ... the rest of your test
```

Can also be used in a fixture, of course.

```python
@pytest.fixture()
def foo(runtime_xfail):
  if (runtime_condition):
     runtime_xfail()
  # ... the rest of your fixture

def test_something(foo):
  # ... the rest of your test
```

## Example found in example/test_xfail.py

```python
"""
Run this with
* pytest -v
* pytest -v -o xfail_strict=true
"""

import pytest

@pytest.mark.xfail()
def test_marker_pass():
    'Can be XPASS or FAIL (if xfail_strict)'
    assert True

@pytest.mark.xfail()
def test_marker_fail():
    'Will always be XFAIL'
    assert False  # this statememt will be run

def test_old_xfail_pass():
    'Will always be XFAIL'
    pytest.xfail()
    assert True  # this statememt will NOT be run

def test_old_xfail_fail():
    'Will always be XFAIL'
    pytest.xfail()
    assert False  # this statememt will NOT be run

def test_runtime_xfail_pass(runtime_xfail):
    runtime_xfail()
    assert True  # this statement will be run

def test_runtime_xfail_fail(runtime_xfail):
    runtime_xfail()
    assert False  # this statement will be run

def test_runtime_xfail_reason(runtime_xfail):
    runtime_xfail(reason="for demo")
    assert False  # this statement will be run
```

**Output:**

```
(venv) $ pytest -v test_xfail.py 
========================= test session starts ==========================
collected 7 items                                                      

test_xfail.py::test_marker_pass XPASS                            [ 14%]
test_xfail.py::test_marker_fail XFAIL                            [ 28%]
test_xfail.py::test_old_xfail_pass XFAIL                         [ 42%]
test_xfail.py::test_old_xfail_fail XFAIL                         [ 57%]
test_xfail.py::test_runtime_xfail_pass XPASS                     [ 71%]
test_xfail.py::test_runtime_xfail_fail XFAIL                     [ 85%]
test_xfail.py::test_runtime_xfail_reason XFAIL (for demo)        [100%]

==================== 5 xfailed, 2 xpassed in 0.05s =====================
(venv) $ pytest -v test_xfail.py -o xfail_strict=true
========================= test session starts ==========================
collected 7 items                                                      

test_xfail.py::test_marker_pass FAILED                           [ 14%]
test_xfail.py::test_marker_fail XFAIL                            [ 28%]
test_xfail.py::test_old_xfail_pass XFAIL                         [ 42%]
test_xfail.py::test_old_xfail_fail XFAIL                         [ 57%]
test_xfail.py::test_runtime_xfail_pass FAILED                    [ 71%]
test_xfail.py::test_runtime_xfail_fail XFAIL                     [ 85%]
test_xfail.py::test_runtime_xfail_reason XFAIL (for demo)        [100%]

===================== 2 failed, 5 xfailed in 0.04s =====================
```