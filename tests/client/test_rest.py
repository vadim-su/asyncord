from unittest.mock import Mock

import pytest

from asyncord.client.rest import RestClient


def test_create_with_http_and_session_fail() -> None:
    """Test creating RestClient with both session and http_client."""
    with pytest.raises(ValueError, match='Cannot pass both session and http_client'):
        RestClient('token', session=Mock(), http_client=Mock())


def test_create_with_http_client() -> None:
    """Test creating RestClient with http_client."""
    http_client = Mock()
    client = RestClient('token', http_client=http_client)
    assert client._http_client == http_client


def test_create_without_auth_fail() -> None:
    """Test creating RestClient without auth."""
    with pytest.raises(ValueError, match='Auth strategy is required'):
        RestClient(None)


def test_create_with_http_client_and_no_auth() -> None:
    """Test creating RestClient with http_client and no auth."""
    RestClient(None, http_client=Mock())


def test_create_with_no_rate_limit_strategy() -> None:
    """Test creating RestClient with no rate limit strategy."""
    RestClient('token', http_client=Mock(), ratelimit_strategy=None)


def test_create_with_castom_auth_strategy() -> None:
    """Test creating RestClient with custom auth strategy."""
    auth = Mock()
    client = RestClient(auth, http_client=Mock())
    mdlwr_append: Mock = client._http_client.system_middlewares.append  # type: ignore
    assert mdlwr_append.call_count == 2
    assert mdlwr_append.call_args_list[0][0][0] == auth
