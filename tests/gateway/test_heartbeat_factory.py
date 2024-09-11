import asyncio
import threading
from collections.abc import AsyncGenerator
from unittest.mock import Mock

import pytest
from pytest_mock import MockFixture

from asyncord.gateway.client.client import ConnectionData, GatewayClient
from asyncord.gateway.client.heartbeat import HeartbeatFactory


@pytest.fixture
def gw_client() -> GatewayClient:
    """Return a mock client."""
    return Mock(spec=GatewayClient)


@pytest.fixture
def conn_data() -> ConnectionData:
    """Return a mock connection data."""
    return Mock(spec=ConnectionData)


@pytest.fixture
async def factory() -> AsyncGenerator[HeartbeatFactory, None]:
    """Return a heartbeat factory."""
    factory = HeartbeatFactory()
    yield factory
    factory.stop()


def test_heartbeat_factory_initialization(factory: HeartbeatFactory) -> None:
    """Test that the heartbeat factory initializes correctly."""
    assert isinstance(factory.loop, asyncio.AbstractEventLoop)
    assert isinstance(factory.thread, threading.Thread)


def test_heartbeat_factory_create(factory: HeartbeatFactory) -> None:
    """Test that the heartbeat factory creates a heartbeat correctly."""
    client = Mock(spec=GatewayClient)
    conn_data = Mock(spec=ConnectionData)
    heartbeat = factory.create(client, conn_data)

    assert heartbeat.client is client
    assert heartbeat.conn_data is conn_data
    assert heartbeat._loop is factory.loop


def test_heartbeat_factory_cycles(factory: HeartbeatFactory) -> None:
    """Test that the heartbeat process cycles."""
    factory.start()
    assert factory.is_running
    assert factory.thread.is_alive()

    factory.stop()
    assert not factory.is_running
    assert not factory.thread.is_alive()


def test_multiple_heartbeats_loop_sharing(factory: HeartbeatFactory) -> None:
    """Test that multiple heartbeats share the same thread."""
    session = Mock(spec=GatewayClient)
    conn_data = Mock(spec=ConnectionData)
    heartbeat1 = factory.create(session, conn_data)
    heartbeat2 = factory.create(session, conn_data)
    assert heartbeat1._loop is heartbeat2._loop


def test_heartbeat_continues_after_one_stops(factory: HeartbeatFactory, mocker: MockFixture) -> None:
    """Test that a heartbeat continues after another stops."""
    mock_run_coroutine = mocker.patch('asyncord.gateway.client.heartbeat.asyncio.run_coroutine_threadsafe')
    mocker.patch('asyncord.gateway.client.heartbeat.Heartbeat._run', new=Mock())
    session = Mock(spec=GatewayClient)
    conn_data = Mock(spec=ConnectionData)
    heartbeat1 = factory.create(session, conn_data)
    heartbeat2 = factory.create(session, conn_data)

    heartbeat1.run(10)
    heartbeat2.run(10)
    factory.start()

    try:
        heartbeat1.stop()
        assert not heartbeat1.is_running
        assert heartbeat2.is_running
        assert mock_run_coroutine.call_count == 2
    finally:
        factory.stop()
