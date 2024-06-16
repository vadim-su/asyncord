from types import MappingProxyType
from typing import Literal
from unittest.mock import Mock

import aiohttp
import pytest
from pytest_mock import MockFixture
from yarl import URL

from asyncord.client.http.middleware.auth import BotTokenAuthStrategy
from asyncord.gateway.client.client import ConnectionData, GatewayClient
from asyncord.gateway.client.heartbeat import Heartbeat, HeartbeatFactory
from asyncord.gateway.dispatcher import EventDispatcher
from asyncord.gateway.intents import DEFAULT_INTENTS, Intent
from asyncord.urls import GATEWAY_URL


@pytest.mark.parametrize('token', ['token', BotTokenAuthStrategy('token')])
@pytest.mark.parametrize('session', [Mock()])
@pytest.mark.parametrize('conn_data', [None, ConnectionData(token='token')])  # noqa: S106
@pytest.mark.parametrize('intents', [DEFAULT_INTENTS, Intent.GUILDS])
@pytest.mark.parametrize('heartbeat_class', [Heartbeat, HeartbeatFactory(), None])
@pytest.mark.parametrize('dispatcher', [None, EventDispatcher()])
@pytest.mark.parametrize('name', [None, 'TestClient'])
def test_init(  # noqa: PLR0917, PLR0913
    token: BotTokenAuthStrategy | Literal['token'],
    session: aiohttp.ClientSession,
    conn_data: None | ConnectionData,
    intents: Intent,
    heartbeat_class: type[Heartbeat] | HeartbeatFactory | None,
    dispatcher: None | EventDispatcher,
    name: None | Literal['TestClient'],
    mocker: MockFixture,
) -> None:
    """Test initializing the GatewayClient."""
    mocker.patch('asyncio.get_event_loop', return_value=Mock())
    if heartbeat_class:
        client = GatewayClient(
            token=token,
            session=session,
            conn_data=conn_data,
            intents=intents,
            heartbeat_class=heartbeat_class,
            dispatcher=dispatcher,
            name=name,
        )
    else:
        client = GatewayClient(
            token=token,
            session=session,
            conn_data=conn_data,
            intents=intents,
            dispatcher=dispatcher,
            name=name,
        )

    if isinstance(token, str):
        str_token = token
    else:
        str_token = token.token

    assert client.session == session
    assert client.conn_data == (conn_data or ConnectionData(token=str_token))
    assert client.intents == intents
    assert isinstance(client.heartbeat, Heartbeat)
    if dispatcher:
        assert client.dispatcher is dispatcher
    else:
        assert isinstance(client.dispatcher, EventDispatcher)
    assert not client.is_started
    assert client.name == name
    assert client._ws is None
    assert not client._need_restart.is_set()
    assert isinstance(client._opcode_handlers, MappingProxyType)
    assert len(client._opcode_handlers)


@pytest.mark.parametrize('token', ['token', ''])
@pytest.mark.parametrize('resume_url', ['ws://localhost', ''])
@pytest.mark.parametrize('session_id', ['session_id', None])
@pytest.mark.parametrize('seq', [1, 0])
def test_can_resume(token: str, resume_url: str, session_id: str | None, seq: int) -> None:
    """Test checking if the connection can be resumed."""
    conn_data = ConnectionData(
        token=token,
        resume_url=URL(resume_url),
        session_id=session_id,
        seq=seq,
    )
    assert conn_data.can_resume is bool(resume_url and session_id and seq)


def test_reset() -> None:
    """Test resetting connection data."""
    conn_data = ConnectionData(
        token='token',  # noqa: S106
        resume_url=URL('ws://localhost'),
        session_id='session_id',
        seq=1,
    )
    conn_data.reset()

    assert conn_data.resume_url == GATEWAY_URL
    assert conn_data.session_id is None
    assert conn_data.seq == 0
