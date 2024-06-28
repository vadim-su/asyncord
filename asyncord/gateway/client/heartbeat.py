"""This module contains the heartbeat for the gateway client.

The heartbeat is used to keep the connection alive with the gateway and automatically
reconnect if the connection is lost.
"""

from __future__ import annotations

import asyncio
import datetime
import logging
import random
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncord.gateway.client.client import ConnectionData, GatewayClient

__all__ = ('Heartbeat', 'HeartbeatFactory')


logger = logging.getLogger(__name__)


class Heartbeat:
    """Heartbeat for the gateway."""

    def __init__(
        self,
        client: GatewayClient,
        conn_data: ConnectionData,
        _loop: asyncio.AbstractEventLoop | None = None,
    ):
        """Initialize the heartbeat."""
        self.client = client
        self.conn_data = conn_data

        self._loop = _loop or asyncio.get_event_loop()
        self._interval = datetime.timedelta(seconds=0)
        self._task = None
        self._ack_event = asyncio.Event()

    async def handle_heartbeat_ack(self) -> None:
        """Handle a heartbeat ack."""
        self._ack_event.set()

    def run(self, interval: int) -> None:
        """Run the heartbeat."""
        self.stop()
        self._interval = datetime.timedelta(milliseconds=interval)
        self._task = asyncio.run_coroutine_threadsafe(self._run(self._interval), self._loop)

    def stop(self) -> None:
        """Stop the heartbeat."""
        if not self._task:
            return

        self._task.cancel()
        self._task = None
        self._cleanup()

    @property
    def is_running(self) -> bool:
        """Whether the heartbeat is running."""
        return self._task is not None

    def __repr__(self) -> str:
        """Return the representation of the heartbeat."""
        return f'<Heartbeat interval={self._interval}>'

    def _cleanup(self) -> None:
        """Cleanup the heartbeat."""
        self._ack_event.clear()
        self._interval = datetime.timedelta(seconds=0)

    async def _run(self, interval: datetime.timedelta) -> None:
        """Run the heartbeat.

        Args:
            interval: Interval to send heartbeats at.
        """
        while self._task:
            last_ack = datetime.datetime.now(datetime.UTC)
            sleep_duration = self._jittered_sleep_duration
            await asyncio.sleep(sleep_duration)

            self._ack_event.clear()
            now = datetime.datetime.now(datetime.UTC)
            keep_interval = interval - (now - last_ack)

            logger.debug('Keep interval: %i', keep_interval.total_seconds())
            try:
                await asyncio.wait_for(self._wait_heartbeat_ack(), timeout=keep_interval.total_seconds())
            except TimeoutError:
                logger.error('Heartbeat ack not received in time. Reconnecting...')
                self.client.reconnect()
                self._task = None
                break
            except Exception as e:
                logger.error('An unexpected error occurred: %s', e)
                self.client.reconnect()
                self._task = None
                break

    async def _wait_heartbeat_ack(self) -> None:
        """Wait for a heartbeat ack."""
        for _ in range(100):
            await self.client.send_heartbeat(seq=self.conn_data.seq)
            logger.debug('Heartbeat sent')
            try:
                await asyncio.wait_for(self._ack_event.wait(), timeout=5)
                logger.debug('Heartbeat ack received')
                return
            except TimeoutError:
                pass
            logger.debug('Heartbeat ack not received')

        logger.error('Heartbeat ack not received after 100 attempts. Looks weird')

    @property
    def _jittered_sleep_duration(self) -> float:
        """Get the jittered sleep duration.

        The sleep duration is the heartbeat interval multiplied by a random
        factor between 0.3 and 0.90.
        """
        jitter = random.uniform(0.3, 0.9)  # noqa: S311  # It's okay to use random here.
        return self._interval.total_seconds() * jitter


class HeartbeatFactory:
    """Factory for creating heartbeats."""

    def __init__(self) -> None:
        """Initialize the factory."""
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._heartbeat_worker, daemon=True)

    def create(self, client: GatewayClient, conn_data: ConnectionData) -> Heartbeat:
        """Create a heartbeat."""
        return Heartbeat(client=client, conn_data=conn_data, _loop=self.loop)

    def start(self) -> None:
        """Start the heartbeat."""
        self.thread.start()

    def stop(self) -> None:
        """Stop the heartbeat."""
        if not self.thread.is_alive():
            return
        self.loop.call_soon_threadsafe(self.loop.stop)
        try:
            self.thread.join()
        except KeyboardInterrupt:
            logger.info('Heartbeat thread interrupted.')

    @property
    def is_running(self) -> bool:
        """Whether the heartbeat is running."""
        return self.thread.is_alive()

    def _heartbeat_worker(self) -> None:
        """Run the heartbeat."""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
