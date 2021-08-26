"""
pytest plugin, providing a `runtime_xfail` fixture, which is callable as `runtime_xfail()`, to allow runtime decisions to mark a test as `xfail`.
"""
import pytest

__version__ = "1.0.2"


@pytest.fixture()
def runtime_xfail(request):
    """
    Call runtime_xfail() to mark running test as xfail.
    """
    def _xfail(reason=''):
        request.node.add_marker(pytest.mark.xfail(reason=reason))
    return _xfail