import logging
from unittest.mock import AsyncMock, Mock

import pytest

from asyncord.gateway.client.client import ConnectionData
from asyncord.gateway.client.opcode_handlers import (
    DispatchHandler,
    HeartbeatAckHandler,
    HelloHandler,
    InvalidSessionHandler,
    ReconnectHandler,
)
from asyncord.gateway.commands import IdentifyCommand, ResumeCommand
from asyncord.gateway.events.base import ReadyEvent
from asyncord.gateway.message import DispatchMessage


@pytest.fixture
def client() -> Mock:
    """Return a mock client."""
    client = AsyncMock()
    client.conn_data = ConnectionData(
        token='token',  # noqa: S106
        seq=0,
        session_id='session_id',
    )
    client.reconnect = Mock()
    return client


async def test_dispatch_unhandled_event(
    client: Mock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test dispatching an unhandled event."""
    handler = DispatchHandler(client, logging.getLogger('asyncord.gateway.client.opcode_handlers'))
    message = DispatchMessage(t='unhandled_event', d={}, s=1)  # type: ignore
    with caplog.at_level(logging.WARNING):
        await handler.handle(message)
    assert 'Unhandled event: unhandled_event' in caplog.text


async def test_dispatch_ready_event(client: Mock) -> None:
    """Test dispatching a ready event."""
    handler = DispatchHandler(client, logging.getLogger('asyncord.gateway.client.opcode_handlers'))
    event_data = {
        'v': 9,
        'user': {
            'id': '1234567890',
            'username': 'example_user',
            'global_name': 'example_user#1234',
            'discriminator': '1234',
            'avatar': 'example_avatar',
        },
        'guilds': [
            {
                'id': '123',
                'unavailable': True,
            },
            {
                'id': '123',
                'unavailable': False,
            },
        ],
        'session_id': 'example_session_id',
        'resume_gateway_url': 'example_gateway_url',
        'shard': {
            'shard_id': 0,
            'num_shards': 1,
        },
        'application': {
            'id': '1234567890',
            'flags': 0,
        },
    }

    message = DispatchMessage(t=ReadyEvent.__event_name__, d=event_data, s=1)  # type: ignore
    await handler.handle(message)
    assert client.conn_data.seq == 1
    assert client.conn_data.session_id == 'example_session_id'
    client.dispatcher.dispatch.assert_called_once()


async def test_reconnect_handler_handle(client: Mock) -> None:
    """Test handling the RECONNECT opcode."""
    handler = ReconnectHandler(client, Mock())
    await handler.handle(Mock())
    client.reconnect.assert_called_once()


async def test_invalid_session_handler_handle(client: Mock) -> None:
    """Test handling the INVALID_SESSION opcode."""
    client.conn_data = Mock()
    handler = InvalidSessionHandler(client, Mock())
    message = Mock(data=True)
    await handler.handle(message)
    client.reconnect.assert_called_once()
    client.conn_data.reset.assert_not_called()


async def test_invalid_session_handler_handle_no_data(client: Mock) -> None:
    """Test handling the INVALID_SESSION opcode."""
    client.conn_data = Mock()
    handler = InvalidSessionHandler(client, Mock())
    message = Mock(data=False)
    await handler.handle(message)
    client.reconnect.assert_called_once()
    client.conn_data.reset.assert_called_once()


async def test_hello_handler_handle_can_resume(client: Mock) -> None:
    """Test handling the HELLO opcode."""
    client.heartbeat = Mock()
    client.hearbeat.run = AsyncMock()
    client.conn_data.seq = 1
    handler = HelloHandler(client, Mock())

    await handler.handle(Mock())
    client.heartbeat.run.assert_called_once()
    client.send_resume.assert_called_once_with(
        ResumeCommand(
            token=client.conn_data.token,
            session_id=client.conn_data.session_id,
            seq=client.conn_data.seq,
        ),
    )
    client.identify.assert_not_called()


async def test_hello_handler_handle_cannot_resume(client: Mock) -> None:
    """Test handling the HELLO opcode."""
    client.heartbeat = Mock()
    client.hearbeat.run = AsyncMock()
    handler = HelloHandler(client, Mock())

    await handler.handle(Mock())
    client.heartbeat.run.assert_called_once()
    client.send_resume.assert_not_called()
    client.identify.assert_called_once_with(
        IdentifyCommand(
            token=client.conn_data.token,
            intents=client.intents,
        ),
    )


async def test_heartbeat_ack_handler_handle(client: Mock) -> None:
    """Test handling the HEARTBEAT_ACK opcode."""
    handler = HeartbeatAckHandler(client, Mock())
    await handler.handle(Mock())
    client.heartbeat.handle_heartbeat_ack.assert_called_once()
