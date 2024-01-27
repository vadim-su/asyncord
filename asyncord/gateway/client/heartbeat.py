import asyncio
import datetime
import logging
import random
from typing import Protocol

from asyncord.gateway.client.commander import GatewayCommander


class HeartbeatProto(Protocol):
    """Protocol for a heartbeat."""

    async def run(self) -> None:
        """Run the heartbeat."""

    async def stop(self) -> None:
        """Stop the heartbeat."""

    async def handle_heartbeat_ack(self, interval: int) -> None:
        """Handle a heartbeat ack."""


class Heartbeat(HeartbeatProto):
    """Heartbeat implementation."""

    def __init__(self, commander: GatewayCommander) -> None:
        """Initialize the heartbeat."""
        self.commander = commander
        self._task: asyncio.Task | None = None
        self._ack_event = asyncio.Event()
        self._interval = 0
        self._last_ack = None

    def run(self) -> None:
        """Start the heartbeat task."""
        self._task = asyncio.create_task(self._run())
        logging.debug("Heartbeat task started.")

    async def stop(self) -> None:
        """Stop the heartbeat task."""
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                logging.debug("Heartbeat task cancelled.")
            self._task = None

    async def handle_heartbeat_ack(self, interval: int) -> None:
        """Handle a heartbeat acknowledgement.

        Update the heartbeat interval and set the acknowledgement event.
        """
        self._interval = interval
        self._last_ack = datetime.datetime.now(datetime.UTC)
        self._ack_event.set()
        logging.debug(f"Heartbeat acknowledgement handled. Interval set to {interval}.")

    def __repr__(self) -> str:
        """Return the representation of the heartbeat."""
        return f'<Heartbeat interval={self._interval}>'

    async def _run(self) -> None:
        """Run the heartbeat task.

        This method is run in a separate task and handles sending heartbeats
        and waiting for acknowledgements.
        """
        self._last_ack = datetime.datetime.now(datetime.UTC)

        while self._task:
            await asyncio.sleep(self._jittered_sleep_duration)
            await self.commander.heartbeat()

            elapsed_time = datetime.datetime.now(datetime.UTC) - self._last_ack
            wait_duration = elapsed_time - datetime.timedelta(seconds=self._interval)

            await asyncio.wait_for(self._ack_event.wait(), timeout=wait_duration.seconds)
            self._ack_event.clear()

    @property
    def _jittered_sleep_duration(self) -> int:
        """Get the jittered sleep duration.

        The sleep duration is the heartbeat interval multiplied by a random
        factor between 0.25 and 0.95.
        """
        jitter = random.uniform(0.3, 0.9)
        return int(self._interval * jitter)
