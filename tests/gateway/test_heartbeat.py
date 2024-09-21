import datetime
import logging
from collections.abc import AsyncGenerator
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from asyncord.gateway.client.client import ConnectionData, GatewayClient
from asyncord.gateway.client.heartbeat import Heartbeat


@pytest.fixture
def gw_client() -> GatewayClient:
    """Return a mock client."""
    return Mock(spec=GatewayClient)


@pytest.fixture
def conn_data() -> ConnectionData:
    """Return a mock connection data."""
    return Mock(spec=ConnectionData)


@pytest.fixture
async def heartbeat(
    gw_client: GatewayClient,
    conn_data: ConnectionData,
) -> AsyncGenerator[Heartbeat, None]:
    """Return a mock heartbeat."""
    heratbeat = Heartbeat(client=gw_client, conn_data=conn_data)
    yield heratbeat
    heratbeat.stop()


def test_heartbeat_init(
    heartbeat: Heartbeat,
    gw_client: GatewayClient,
    conn_data: ConnectionData,
) -> None:
    """Test initializing the heartbeat."""
    assert heartbeat.client is gw_client
    assert heartbeat.conn_data is conn_data
    assert heartbeat._interval.total_seconds() == 0
    assert heartbeat._task is None


async def test_handle_heartbeat_ack(
    heartbeat: Heartbeat,
) -> None:
    """Test handling a heartbeat ack."""
    await heartbeat.handle_heartbeat_ack()
    assert heartbeat._ack_event.is_set()


def test_run_stop_cycle(
    heartbeat: Heartbeat,
) -> None:
    """Test running and stopping the heartbeat."""
    heartbeat.run(1000)
    assert heartbeat._interval.total_seconds() == 1
    assert heartbeat._task is not None

    heartbeat.stop()
    assert heartbeat._task is None
    assert not heartbeat._ack_event.is_set()
    assert heartbeat._interval.total_seconds() == 0


def test_is_running(
    heartbeat: Heartbeat,
) -> None:
    """Test is_running property."""
    assert not heartbeat.is_running

    heartbeat.run(1000)
    assert heartbeat.is_running

    heartbeat.stop()
    assert not heartbeat.is_running


def test_jittered_sleep_duration(
    heartbeat: Heartbeat,
) -> None:
    """Test jittered sleep duration."""
    interval = 5
    heartbeat._interval = datetime.timedelta(seconds=interval)

    sleep_duration = heartbeat._jittered_sleep_duration
    assert isinstance(sleep_duration, float)
    assert interval * 0.3 <= sleep_duration <= interval * 0.9


async def test_run(
    heartbeat: Heartbeat,
    mocker: MockerFixture,
) -> None:
    """Test the _run method."""
    heartbeat._task = Mock()

    def _stop_loop() -> None:
        heartbeat._task = None

    mock_wait_heartbeat_ack = mocker.patch.object(heartbeat, '_wait_heartbeat_ack', side_effect=_stop_loop)
    mocker.patch('asyncio.sleep', return_value=None)

    await heartbeat._run(
        interval=datetime.timedelta(seconds=1),
    )

    mock_wait_heartbeat_ack.assert_called_once()


async def test_run_with_exception(
    heartbeat: Heartbeat,
    mocker: MockerFixture,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the _run method when an exception is raised."""
    heartbeat._task = Mock()
    mock_wait_heartbeat_ack = mocker.patch.object(
        heartbeat,
        '_wait_heartbeat_ack',
        side_effect=Exception('Some exception occurred'),
    )
    mock_sleep = mocker.patch('asyncio.sleep', return_value=None)

    interval = datetime.timedelta(seconds=1)
    with caplog.at_level(logging.ERROR):
        await heartbeat._run(interval)

    mock_wait_heartbeat_ack.assert_called_once()
    mock_sleep.assert_called_once()

    assert 'An unexpected error occurred: Some exception occurred' in caplog.text


async def test_run_with_timeout(
    heartbeat: Heartbeat,
    mocker: MockerFixture,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the _run method when a timeout occurs."""
    heartbeat._task = Mock()
    mock_wait_heartbeat_ack = mocker.patch.object(
        heartbeat,
        '_wait_heartbeat_ack',
        side_effect=TimeoutError(),
    )
    mock_sleep = mocker.patch('asyncio.sleep', return_value=None)

    interval = datetime.timedelta(seconds=1)
    with caplog.at_level(logging.ERROR):
        await heartbeat._run(interval)

    mock_wait_heartbeat_ack.assert_called_once()
    mock_sleep.assert_called_once()

    assert 'Heartbeat ack not received in time. Reconnecting...' in caplog.text


async def test_wait_heartbeat_ack_received(
    heartbeat: Heartbeat,
    conn_data: ConnectionData,
    mocker: MockerFixture,
) -> None:
    """Test the _wait_heartbeat_ack method when the ack is received."""
    conn_data.seq = 1
    heartbeat._ack_event = Mock()  # suppress the RuntimeWarning

    mock_send_heartbeat = mocker.patch.object(heartbeat.client, 'send_heartbeat', return_value=None)

    # if the ack is received, the method should return without raising an error
    # this mock emilates the ack being received
    mock_wait_for = mocker.patch('asyncio.wait_for', return_value=None)

    await heartbeat._wait_heartbeat_ack()

    mock_send_heartbeat.assert_called_once()
    mock_wait_for.assert_called_once()


async def test_wait_heartbeat_ack_no_ack_received(
    heartbeat: Heartbeat,
    conn_data: ConnectionData,
    mocker: MockerFixture,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the _wait_heartbeat_ack method when no ack is received."""
    conn_data.seq = 1
    heartbeat._ack_event = Mock()  # suppress the RuntimeWarning

    mock_send_heartbeat = mocker.patch.object(heartbeat.client, 'send_heartbeat', return_value=None)
    mock_wait_for = mocker.patch('asyncio.wait_for', side_effect=TimeoutError())

    with caplog.at_level(logging.ERROR):
        await heartbeat._wait_heartbeat_ack()

    assert mock_send_heartbeat.call_count == 100
    assert mock_wait_for.call_count == 100

    assert 'ack not received after 100 attempts' in caplog.text
