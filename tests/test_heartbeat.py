import asyncio
import threading
from unittest.mock import Mock

from asyncord.gateway.client.client import ConnectionData, GatewayClient
from asyncord.gateway.client.heartbeat import Heartbeat, HeartbeatFactory


def test_heartbeat_factory_initialization():
    factory = HeartbeatFactory()
    assert isinstance(factory.loop, asyncio.AbstractEventLoop)
    assert isinstance(factory.thread, threading.Thread)


def test_heartbeat_factory_create():
    factory = HeartbeatFactory()
    client = Mock(spec=GatewayClient)
    conn_data = Mock(spec=ConnectionData)
    heartbeat = factory.create(client, conn_data)
    assert isinstance(heartbeat, Heartbeat)
    assert heartbeat.client == client
    assert heartbeat.conn_data == conn_data
    assert heartbeat._loop == factory.loop


def test_heartbeat_factory_start():
    factory = HeartbeatFactory()
    factory.start()
    assert factory.is_running
    assert factory.thread.is_alive()


def test_heartbeat_factory_stop():
    factory = HeartbeatFactory()
    factory.start()
    print(factory.thread.is_alive())
    factory.stop()
    print(factory.thread.is_alive())
    assert not factory.is_running
    assert not factory.thread.is_alive()


def test_multiple_heartbeats_same_thread():
    factory = HeartbeatFactory()
    session = Mock(spec=GatewayClient)
    conn_data = Mock(spec=ConnectionData)
    heartbeat1 = factory.create(session, conn_data)
    heartbeat2 = factory.create(session, conn_data)
    assert heartbeat1._loop == heartbeat2._loop


def test_multiple_heartbeats():
    factory = HeartbeatFactory()
    session = Mock(spec=GatewayClient)
    conn_data = Mock(spec=ConnectionData)
    heartbeat1 = factory.create(session, conn_data)
    heartbeat2 = factory.create(session, conn_data)
    assert heartbeat1 != heartbeat2


def test_heartbeat_continues_after_one_stops():
    factory = HeartbeatFactory()
    session = Mock(spec=GatewayClient)
    conn_data = Mock(spec=ConnectionData)
    heartbeat1 = factory.create(session, conn_data)
    heartbeat2 = factory.create(session, conn_data)
    heartbeat1.run(10)
    heartbeat2.run(10)
    heartbeat1.stop()
    assert not heartbeat1.is_running
    assert heartbeat2.is_running
