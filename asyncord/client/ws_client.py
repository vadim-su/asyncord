from __future__ import annotations

import enum
import random
import asyncio
from typing import Any, Final, Callable, cast, overload, get_type_hints
from datetime import datetime, timedelta
from contextlib import suppress
from collections import defaultdict
from collections.abc import Awaitable

import aiohttp
from pydantic import Field, BaseModel, validator

from asyncord.urls import GATEWAY_URL
from asyncord.typedefs import StrOrURL


@enum.unique
class GatewayOpcodes(enum.IntEnum):
    DISPATCH = 0
    """An event was dispatched."""

    HEARTBEAT = 1
    """Fired periodically by the client to keep the connection alive."""

    IDENTIFY = 2
    """Starts a new session during the initial handshake."""

    PRESENCE_UPDATE = 3
    """Update the client's presence."""

    VOICE_STATE_UPDATE = 4
    """Used to join / leave or move between voice channels."""

    RESUME = 6
    """Resume a previous session that was disconnected."""

    RECONNECT = 7
    """You should attempt to reconnect and resume immediately."""

    REQUEST_GUILD_MEMBERS = 8
    """Request information about offline guild members in a large guild."""

    INVALID_SESSION = 9
    """The session has been invalidated. You should reconnect and identify / resume accordingly."""

    HELLO = 10
    """Sent immediately after connecting, contains the heartbeat_interval to use."""

    HEARTBEAT_ACK = 11
    """Sent in response to receiving a heartbeat to acknowledge that it has been received."""


class GatewayEvent(BaseModel):
    """Base class for all gateway events."""

    opcode: GatewayOpcodes
    event_data: Any
    sequence_number: int
    name: str


EventHandler = Callable[[GatewayEvent], Awaitable[None]]


class GatewayMessage(BaseModel):
    opcode: GatewayOpcodes = Field(alias='op')
    msg_data: Any = Field(alias='d')
    sequence_number: int | None = Field(alias='s')
    event_name: str | None = Field(alias='t')
    trace: Any = Field(default=None, alias='_trace')

    @validator('event_name', 'sequence_number')
    def check_values_are_not_none(cls, value, values):  # noqa: N805,WPS110
        if values['opcode'] == GatewayOpcodes.DISPATCH:
            if value is None:
                raise ValueError('Event name and sequence number must be set')

        elif value is not None:
            raise ValueError('Event name and sequence number must be None')

        return value


class EventDispatcher:
    def __init__(self):
        self._handlers = defaultdict(list)

    @overload
    def add_handler(self, event_type: type[GatewayEvent], event_handler: EventHandler):
        ...

    @overload
    def add_handler(self, event_type: EventHandler):
        ...

    def add_handler(
        self,
        event_type: type[GatewayEvent] | EventHandler,
        event_handler: EventHandler | None = None,
    ):
        if event_handler is None:
            event_handler = cast(EventHandler, event_type)
            handler_arg_types = list(get_type_hints(event_handler).values())
            if not handler_arg_types:
                raise ValueError(
                    'Event handler must have at least one argument for the event',
                )

            event_type = cast(type, handler_arg_types[0])
            if not issubclass(event_type, GatewayEvent):
                raise ValueError(
                    'Event handler must have any gateway event as its first argument',
                )

        self._handlers[event_type].append(event_handler)

    def dispatch(self, event: GatewayEvent):
        event_type = type(event)
        for event_handler in self._handlers.get(event_type, []):
            event_handler(event)


class Periodic:
    CHECK_PERIOD: Final[float] = 0.2

    def __init__(self, func: Callable[..., Awaitable[None]], time: timedelta):
        self.func = func
        self.run_period = time
        self.is_started = False
        self.last_run = None

        self._task = None
        self._jitter = random.random()

    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.ensure_future(self._run())
            self.last_run = None

    async def stop(self):
        if self.is_started:
            self.is_started = False
            # Stop task and await it stopped:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    def update_period(self, time: timedelta):
        self.run_period = time
        self.last_run = datetime.now()

    async def _run(self):
        while True:
            now = datetime.now()
            if self.last_run and (now - self.last_run >= self.time_to_wait):
                await self.func()
                self.last_run = now
                self._jitter = random.random()

            await asyncio.sleep(self.CHECK_PERIOD)

    @property
    def time_to_wait(self) -> timedelta:
        return self.run_period * self._jitter


class AsyncGatewayClient:
    def __init__(self, ws_url: StrOrURL):
        self.ws_url = ws_url
        self._session: aiohttp.ClientSession | None = None
        self._dispatcher = EventDispatcher()
        self.ws_

    def add_handler(self, event_type, event_handler):
        self._dispatcher.add_handler(event_type, event_handler)

    async def

    async def start(self):
        self._session = aiohttp.ClientSession()
        async with self._session.ws_connect(self.ws_url) as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    self._handle_message(GatewayMessage(**msg.json()))
            else:
                print('Connection closed')

    def _handle_message(self, msg: GatewayMessage):
        match msg.opcode:
            case GatewayOpcodes.DISPATCH:
                pass
            case GatewayOpcodes.HELLO:

        print(msg)


async def main():
    client = AsyncGatewayClient(GATEWAY_URL)
    await client.start()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
