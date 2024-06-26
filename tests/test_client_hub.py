import logging
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from asyncord.client_hub import ClientHub


async def test_create_hub_without_session() -> None:
    """Test creating a hub without a session."""
    hub = ClientHub()
    assert not hub._is_outer_session
    assert hub.session


async def test_setup_single_client_group(mocker: MockerFixture) -> None:
    """Test setup_single_client_group method."""
    mock_gather = mocker.patch('asyncio.gather', new=mocker.async_stub('gather'))
    mock_client_group_class = mocker.patch('asyncord.client_hub.ClientGroup')

    async with ClientHub.setup_single_client_group(auth='token', session=Mock()) as client_group:
        mock_client_group_class.assert_called_once()
        mock_client_group = mock_client_group_class.return_value
        assert client_group is mock_client_group

    mock_gather.assert_called_once()
    mock_client_group.connect.assert_called_once()


async def test_setup_with_dispatcher(mocker: MockerFixture, caplog: pytest.LogCaptureFixture) -> None:
    """Test setup method with a dispatcher."""
    mock_gather = mocker.patch('asyncio.gather', new=mocker.async_stub('gather'))
    hub_context = ClientHub.setup_single_client_group(auth='token', session=Mock(), dispatcher=Mock())
    mocker.patch('asyncord.client_hub.ClientGroup')
    with caplog.at_level(logging.WARNING):
        async with hub_context:
            pass

    mock_gather.assert_called_once()
    assert 'dispatcher is passed' in caplog.text


async def test_create_client_group(mocker: MockerFixture) -> None:
    """Test creation of a client group."""
    mock_client_group_class = mocker.patch('asyncord.client_hub.ClientGroup')
    hub = ClientHub(session=Mock())
    hub.create_client_group('group_name', 'token')

    mock_client_group_class.assert_called_once()

    with pytest.raises(ValueError, match=r'Client group group_name already exists'):
        hub.create_client_group('group_name', auth='token')
