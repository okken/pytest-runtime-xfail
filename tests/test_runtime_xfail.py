import pytest


def test_fixture_docs(pytester):
    result = pytester.runpytest("--fixtures")
    result.stdout.fnmatch_lines([
        "*runtime_xfail*",
        "*Call runtime_xfail() to mark running test as xfail.*"
    ])

test_file_content = """
 def test_pass(runtime_xfail):
     runtime_xfail()
     assert True


def test_fail(runtime_xfail):
    runtime_xfail()
    assert False


def test_reason(runtime_xfail):
    runtime_xfail("I have my reasons")
    assert False
"""

@pytest.fixture()
def file_structure(pytester):
    pytester.makepyfile(test_xfail=test_file_content)

def test_xpass(pytester, file_structure):
    result = pytester.runpytest("test_xfail.py", '-k', 'test_pass')
    result.assert_outcomes(xpassed=1)


def test_xfail(pytester, file_structure):
    result = pytester.runpytest("test_xfail.py", '-k',  'test_fail')
    result.assert_outcomes(xfailed=1)


def test_fail(pytester, file_structure):
    pytester.makefile(".ini", pytest="[pytest]\nxfail_strict=true\n")
    result = pytester.runpytest("test_xfail.py", '-k test_pass')
    result.assert_outcomes(failed=1)


def test_reasons(pytester, file_structure):
    result = pytester.runpytest("test_xfail.py", '-v', '-k', 'test_reason')
    result.stdout.fnmatch_lines(["*I have my reasons*"])