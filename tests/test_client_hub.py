import logging
from unittest.mock import AsyncMock, Mock

import pytest
from pytest_mock import MockerFixture

from asyncord.client_hub import ClientHub


async def test_create_hub_without_session() -> None:
    """Test creating a hub without a session."""
    hub = ClientHub()
    assert not hub._is_outer_session
    assert hub.session


async def test_connect(mocker: MockerFixture) -> None:
    """Test setup_single_client_group method."""
    mock_gather = mocker.patch('asyncio.gather', new=mocker.async_stub('gather'))
    mock_client_group_class = mocker.patch('asyncord.client_hub.ClientGroup')
    mock_client_group_class.return_value.close = AsyncMock()

    async with ClientHub.connect(auth='token', session=Mock()) as client_group:
        mock_client_group_class.assert_called_once()
        mock_client_group = mock_client_group_class.return_value
        assert client_group is mock_client_group

    mock_gather.assert_called_once()
    mock_client_group.connect.assert_called_once()


async def test_connect_with_dispatcher(mocker: MockerFixture, caplog: pytest.LogCaptureFixture) -> None:
    """Test setup method with a dispatcher."""
    mock_gather = mocker.patch('asyncio.gather', new=mocker.async_stub('gather'))
    hub_context = ClientHub.connect(auth='token', session=Mock(), dispatcher=Mock())
    mock_client_group_class = mocker.patch('asyncord.client_hub.ClientGroup')
    mock_client_group_class.return_value.close = AsyncMock()

    with caplog.at_level(logging.WARNING):
        async with hub_context:
            pass

    mock_gather.assert_called_once()
    assert 'dispatcher is passed' in caplog.text


@pytest.mark.skip(reason='Not implemented yet. https://github.com/pytest-dev/pytest/discussions/12540')
async def test_start_handles_exceptions(mocker: MockerFixture) -> None:
    """Test start method handles exceptions."""
    # Setup ClientHub instance
    hub = ClientHub()
    hub.heartbeat_factory = AsyncMock()

    client1 = AsyncMock()
    # Simulate KeyboardInterrupt during asyncio.gather
    client1.connect.side_effect = KeyboardInterrupt

    hub.client_groups = {
        'client1': client1,
        'client2': AsyncMock(),
    }

    # Mock logger
    mock_logger = mocker.patch('asyncord.client_hub.logger')

    await hub.start()

    # Assertions
    mock_logger.info.assert_any_call('Shutting down...')
    hub.heartbeat_factory.start.assert_called_once()
    for client in hub.client_groups.values():
        client.connect.assert_called()  # type: ignore
