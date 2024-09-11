import pytest

from asyncord.client.http.headers import HttpMethod
from asyncord.client.http.models import Request


@pytest.fixture
def request_obj() -> Request:
    """Return an instance of the request model."""
    return Request(method=HttpMethod.GET, url='https://example.com')
