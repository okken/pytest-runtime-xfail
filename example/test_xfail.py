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
