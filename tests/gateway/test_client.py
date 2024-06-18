import asyncio
from types import MappingProxyType
from typing import Literal
from unittest.mock import AsyncMock, Mock, patch

import aiohttp
import pytest
from pytest_mock import MockFixture

from asyncord.client.http.middleware.auth import BotTokenAuthStrategy
from asyncord.gateway.client.client import ConnectionData, GatewayClient, GatewayCommandOpcode
from asyncord.gateway.client.errors import ConnectionClosedError
from asyncord.gateway.client.heartbeat import Heartbeat, HeartbeatFactory
from asyncord.gateway.commands import IdentifyCommand, PresenceUpdateData, ResumeCommand
from asyncord.gateway.dispatcher import EventDispatcher
from asyncord.gateway.intents import DEFAULT_INTENTS, Intent


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
    """Test initializing the GatewayClient.

    Init logic looks like overkill, but it's working fine at the moment.
    I don't think that is a good idea to make separate tests for each parameter
    for at the moment.
    Candidate for refactoring.
    """
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


async def test_connect_when_already_started(gw_client: GatewayClient) -> None:
    """Test connecting when the client is already started."""
    gw_client.is_started = True
    with pytest.raises(RuntimeError, match='Client is already started'):
        await gw_client.connect()


async def test_connect_when_not_started(gw_client: GatewayClient, mocker: MockFixture) -> None:
    """Test connecting when the client is not started."""
    gw_client.is_started = False

    mock_connect = mocker.patch.object(gw_client, '_connect', return_value=asyncio.Future())
    mock_connect.return_value.set_result(None)

    await gw_client.connect()

    assert gw_client.is_started
    mock_connect.assert_called_once()


async def test_close_when_not_started_and_no_ws(gw_client: GatewayClient, mocker: MockFixture) -> None:
    """Test closing when the client is not started and no websocket."""
    gw_client.is_started = False
    gw_client._ws = None
    mock_stop = mocker.patch.object(gw_client.heartbeat, 'stop')
    await gw_client.close()
    assert not gw_client.is_started
    assert not gw_client._need_restart.is_set()
    mock_stop.assert_not_called()


async def test_close_when_started_and_no_ws(gw_client: GatewayClient, mocker: MockFixture) -> None:
    """Test closing when the client is started and no websocket."""
    gw_client.is_started = True
    gw_client._ws = None
    mock_stop = mocker.patch.object(gw_client.heartbeat, 'stop')
    await gw_client.close()
    assert not gw_client.is_started
    assert gw_client._need_restart.is_set()
    mock_stop.assert_called_once()


async def test_close_when_started_and_ws(gw_client: GatewayClient, mocker: MockFixture) -> None:
    """Test closing when the client is started and websocket exists."""
    gw_client.is_started = True
    gw_client._ws = Mock()
    mock_stop = mocker.patch.object(gw_client.heartbeat, 'stop')
    mock_close = mocker.patch.object(gw_client._ws, 'close', return_value=asyncio.Future())
    mock_close.return_value.set_result(None)
    await gw_client.close()
    assert not gw_client.is_started
    assert gw_client._need_restart.is_set()
    mock_stop.assert_called_once()
    mock_close.assert_called_once()


async def test_send_command_no_ws(gw_client: GatewayClient) -> None:
    """Test sending a command when the websocket is not connected."""
    gw_client._ws = None
    with pytest.raises(RuntimeError, match='Client is not connected'):
        await gw_client.send_command(GatewayCommandOpcode.HEARTBEAT, {})


async def test_send_command_with_ws(gw_client: GatewayClient) -> None:
    """Test sending a command when the websocket is connected."""
    mock_ws = AsyncMock()
    gw_client._ws = mock_ws
    opcode = GatewayCommandOpcode.HEARTBEAT
    data = {'test': 'data'}
    await gw_client.send_command(opcode, data)
    mock_ws.send_json.assert_called_once_with({'op': opcode, 'd': data})


async def test_reconnect_no_ws(gw_client: GatewayClient) -> None:
    """Test reconnecting when the websocket is not connected."""
    gw_client._ws = None
    with pytest.raises(RuntimeError, match='Client is not started'):
        gw_client.reconnect()


async def test_reconnect_with_ws(gw_client: GatewayClient, mocker: MockFixture) -> None:
    """Test reconnecting when the websocket is connected."""
    gw_client._ws = Mock()
    mock_stop = mocker.patch.object(gw_client.heartbeat, 'stop')
    gw_client.reconnect()
    assert gw_client._need_restart.is_set()
    mock_stop.assert_called_once()


async def test_identify(gw_client: GatewayClient, mocker: MockFixture) -> None:
    """Test identifying with the gateway."""
    mock_send_command = mocker.patch.object(gw_client, 'send_command', return_value=asyncio.Future())
    mock_send_command.return_value.set_result(None)
    command_data = IdentifyCommand(
        token='token',  # noqa: S106
        properties={},  # type: ignore
        compress=False,
        large_threshold=250,
    )
    await gw_client.identify(command_data)
    payload = command_data.model_dump(mode='json', exclude_none=True)
    mock_send_command.assert_called_once_with(GatewayCommandOpcode.IDENTIFY, payload)


async def test_send_resume_no_ws(gw_client: GatewayClient) -> None:
    """Test sending a resume command when the websocket is not connected."""
    gw_client._ws = None
    command_data = ResumeCommand(
        token='token',  # noqa: S106
        session_id='session_id',
        seq=1,
    )
    with pytest.raises(RuntimeError, match='Client is not connected'):
        await gw_client.send_resume(command_data)


async def test_send_resume_with_ws(gw_client: GatewayClient, mocker: MockFixture) -> None:
    """Test sending a resume command when the websocket is connected."""
    mock_ws = AsyncMock()
    gw_client._ws = mock_ws
    command_data = ResumeCommand(
        token='token',  # noqa: S106
        session_id='session_id',
        seq=1,
    )
    mock_send_command = mocker.patch.object(gw_client, 'send_command', return_value=asyncio.Future())
    mock_send_command.return_value.set_result(None)
    await gw_client.send_resume(command_data)
    mock_send_command.assert_called_once_with(GatewayCommandOpcode.RESUME, command_data.model_dump(mode='json'))


async def test_update_presence(gw_client: GatewayClient) -> None:
    """Test updating the client's presence."""
    mock_presence_data = Mock(spec=PresenceUpdateData)
    # can't set model_dump attribute for pydantic models
    mock_presence_data.model_dump = Mock(return_value={'test': 'data'})

    with patch.object(gw_client, 'send_command', new_callable=AsyncMock) as mock_send_command:
        await gw_client.update_presence(mock_presence_data)

    mock_send_command.assert_called_once_with(GatewayCommandOpcode.PRESENCE_UPDATE, {'test': 'data'})


async def test_send_heartbeat_no_ws(gw_client: GatewayClient) -> None:
    """Test send_heartbeat when the client is not connected."""
    gw_client._ws = None
    with pytest.raises(RuntimeError, match='Client is not connected'):
        await gw_client.send_heartbeat(1)


async def test_send_heartbeat_with_ws(gw_client: GatewayClient, mocker: MockFixture) -> None:
    """Test send_heartbeat when the client is connected."""
    mock_ws = mocker.Mock()
    mock_send_json = mocker.AsyncMock()
    mock_ws.send_json = mock_send_json
    gw_client._ws = mock_ws
    seq = 1
    await gw_client.send_heartbeat(seq)
    mock_send_json.assert_called_once_with({'op': GatewayCommandOpcode.HEARTBEAT, 'd': seq})


async def test__connect_when_not_started(gw_client: GatewayClient, mocker: MockFixture) -> None:
    """Test _connect when the client is not started."""
    gw_client.is_started = False
    mock_ws_connect = mocker.patch.object(gw_client.session, 'ws_connect', new_callable=AsyncMock)
    await gw_client._connect()
    mock_ws_connect.assert_not_called()


async def test__connect_when_started_and_connection_closed_immediately(
    gw_client: GatewayClient,
    mocker: MockFixture,
) -> None:
    """Test _connect when the client is started and the connection is closed immediately."""
    gw_client.is_started = True
    mock_ws = AsyncMock()
    mock_ws.__aenter__.return_value = mock_ws
    mock_ws_connect = mocker.patch.object(gw_client.session, 'ws_connect', return_value=mock_ws)

    def _stop(_ws: object) -> None:
        gw_client.is_started = False

    mocker.patch.object(gw_client, '_ws_recv_loop', side_effect=_stop)
    await gw_client._connect()
    mock_ws_connect.assert_called_once()


async def test__connect_when_started_and_connection_closed_with_error(
    gw_client: GatewayClient,
    mocker: MockFixture,
) -> None:
    """Test _connect when the client is started and the connection is closed with an error."""
    gw_client.is_started = True
    mock_ws = AsyncMock()
    mock_ws.__aenter__.return_value = mock_ws
    mock_ws_connect = mocker.patch.object(gw_client.session, 'ws_connect', return_value=mock_ws)

    def _raise(_ws: object) -> None:
        gw_client.is_started = False
        raise ConnectionClosedError

    mock_ws_recv_loop = mocker.patch.object(gw_client, '_ws_recv_loop', side_effect=_raise)

    await gw_client._connect()
    mock_ws_connect.assert_called_once()
    mock_ws_recv_loop.assert_called_once()


async def test__handle_heartbeat_ack(gw_client: GatewayClient, mocker: MockFixture) -> None:
    """Test handling the heartbeat acknowledgement."""
    mock_handle_heartbeat_ack = mocker.patch.object(gw_client.heartbeat, 'handle_heartbeat_ack', new_callable=AsyncMock)
    await gw_client._handle_heartbeat_ack(Mock())
    mock_handle_heartbeat_ack.assert_called_once()


async def test__ws_recv_loop_not_started(gw_client: GatewayClient, mocker: MockFixture) -> None:
    """Test _ws_recv_loop when the client is not started."""
    gw_client.is_started = False
    mock_get_message = mocker.patch.object(gw_client, '_get_message', return_value=asyncio.Future())
    mock_get_message.return_value.set_result(None)
    mock_handle_message = mocker.patch.object(gw_client, '_handle_message')

    await gw_client._ws_recv_loop(Mock())

    mock_get_message.assert_not_called()
    mock_handle_message.assert_not_called()


async def test__ws_recv_loop_need_restart(gw_client: GatewayClient, mocker: MockFixture) -> None:
    """Test _ws_recv_loop when _need_restart is set."""
    gw_client.is_started = True
    gw_client._need_restart.set()
    mock_get_message = mocker.patch.object(gw_client, '_get_message', return_value=asyncio.Future())
    mock_get_message.return_value.set_result(None)
    mock_handle_message = mocker.patch.object(gw_client, '_handle_message')

    await gw_client._ws_recv_loop(Mock())

    mock_get_message.assert_not_called()
    mock_handle_message.assert_not_called()
