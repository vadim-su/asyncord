"""Module for handling the heartbeat loop."""

from __future__ import annotations

import asyncio
import datetime
import logging
import random
from collections.abc import Awaitable, Callable

from asyncord.gateway import errors

logger = logging.getLogger(__name__)

MAX_TIMEOUT_IN_ROW = 3
"""Maximum number of timeouts in a row before failing."""


class Heartbeat:
    """A class for handling the heartbeat loop.

    Attributes:
        heartbeat_command: Command to send a heartbeat.
        timeout_callback: Callback to call when a heartbeat ack is not received.
        is_started: Whether the heartbeat loop is started.
    """

    def __init__(
        self,
        heartbeat_command: Callable[..., Awaitable[None]],
        timeout_callback: Callable[..., Awaitable[None]],
    ) -> None:
        """Initialize the heartbeat processor.

        Args:
            heartbeat_command: Command to send a heartbeat.
            timeout_callback: Callback to call when a heartbeat ack is not received.
        """
        self.heartbeat_command = heartbeat_command
        self.timeout_callback = timeout_callback
        self.is_started = False
        self._heartbeat_task = None
        self._event = asyncio.Event()

    async def start(self, heartbeat_period: float) -> None:
        """Start the heartbeat loop.

        Args:
            heartbeat_period: Period of the heartbeat in seconds.
        """
        logger.debug('Starting heartbeat loop')
        if self.is_started:
            raise RuntimeError('Heartbeat loop is already started')
        self.is_started = True
        self._heartbeat_task = asyncio.create_task(self._hb_loop(heartbeat_period))
        logger.debug('Heartbeat loop started')

    async def stop(self) -> None:
        """Stop the heartbeat loop."""
        logger.debug('Stopping heartbeat loop')
        self.is_started = False
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            await self._heartbeat_task
        logger.debug('Heartbeat loop stopped')

    async def reset_heartbeat(self, heartbeat_period: float) -> None:
        """Reset the heartbeat loop.

        Args:
            heartbeat_period: Period of the heartbeat in seconds.
        """
        if self.is_started:
            await self.stop()

        await self.start(heartbeat_period)

    async def ack(self) -> None:
        """Handle a heartbeat ack."""
        logger.debug('Heartbeat ack received')
        self._event.set()

    async def _hb_loop(self, heartbeat_period: float) -> None:
        """Heartbeat loop.

        Args:
            heartbeat_period: Period of the heartbeat in seconds.
        """
        timeout = 0
        while self.is_started:
            got_timeout = False
            try:
                await self._loop_iteration(heartbeat_period)
            except asyncio.TimeoutError:
                got_timeout = True
            except asyncio.CancelledError:
                break

            if got_timeout:
                timeout += 1
            else:
                timeout = 0

            if timeout >= MAX_TIMEOUT_IN_ROW:
                logger.error('Heartbeat timeout limit reached')
                raise errors.HeartbeatAckTimeoutError

    async def _loop_iteration(self, heartbeat_period: float) -> None:
        """Heartbeat loop iteration.

        Args:
            heartbeat_period: Period of the heartbeat in seconds.
        """
        self._event.clear()
        await self.heartbeat_command()

        next_run = max(heartbeat_period * random.random(), heartbeat_period / 4, 10)  # noqa: S311
        next_run = round(next_run, 3)
        next_run_time = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(seconds=next_run)

        logger.debug('Heartbeat sent. Next run in %s seconds', next_run)

        try:
            # wait for heartbeat ack or timeout in next_run seconds
            await asyncio.wait_for(self._event.wait(), next_run)
        except asyncio.TimeoutError:
            logger.debug('Heartbeat ack timeout for %s seconds', next_run)
            raise

        logger.debug('Heartbeat ack event received')

        # if we got heartbeat ack, recalculate next run time
        next_run = (next_run_time - datetime.datetime.now(tz=datetime.UTC)).total_seconds()
        await asyncio.sleep(next_run)
