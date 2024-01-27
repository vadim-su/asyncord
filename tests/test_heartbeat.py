import asyncio
import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from pytest_mock import MockerFixture

from asyncord.gateway.client.heartbeat import Heartbeat


@pytest.fixture
def heartbeat():
    return Heartbeat(MagicMock())


async def test_heartbeat_run(heartbeat: Heartbeat):
    heartbeat._run = AsyncMock()
    heartbeat.run()
    assert heartbeat._task is not None
    heartbeat._run.assert_called_once()


async def test_heartbeat_stop(heartbeat: Heartbeat):
    heartbeat._task = asyncio.create_task(asyncio.sleep(0.1))
    await heartbeat.stop()
    assert heartbeat._task is None


async def test_handle_heartbeat_ack(heartbeat: Heartbeat):
    interval = 10
    await heartbeat.handle_heartbeat_ack(interval)
    assert heartbeat._interval == interval
    assert heartbeat._ack_event.is_set()


def test_repr(heartbeat: Heartbeat):
    heartbeat._interval = 10
    assert repr(heartbeat) == '<Heartbeat interval=10>'


async def test_run(heartbeat: Heartbeat, mocker: MockerFixture):
    heartbeat._interval = 1
    heartbeat._last_ack = datetime.datetime.now(datetime.UTC)
    heartbeat.commander.heartbeat = AsyncMock()

    async def task_side_effect():
        await asyncio.sleep(0.1)
        heartbeat._task = None

    heartbeat._task = asyncio.create_task(task_side_effect())

    mocker.patch.object(heartbeat._ack_event, 'wait', new_callable=AsyncMock)
    mocker.patch.object(heartbeat._ack_event, 'clear')

    await asyncio.gather(heartbeat._run(), heartbeat._task)

    heartbeat.commander.heartbeat.assert_called()
    heartbeat._ack_event.wait.assert_called()
    heartbeat._ack_event.clear.assert_called()


def test_sleep_duration(heartbeat: Heartbeat):
    heartbeat._interval = 10
    for _ in range(1000):
        # try 1000 times to make sure the jitter is working correctly
        assert 3 <= heartbeat._jittered_sleep_duration <= 9
