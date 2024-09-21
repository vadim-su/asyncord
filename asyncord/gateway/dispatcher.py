"""This module defines the EventDispatcher class, which dispatches events to registered handlers."""

from __future__ import annotations

import logging
from collections import defaultdict
from collections.abc import Awaitable, Callable, MutableMapping
from typing import (
    Any,
    Concatenate,
    TypeVar,
    cast,
    get_type_hints,
    overload,
)

from asyncord.gateway.events.base import GatewayEvent

__all__ = (
    'EventDispatcher',
    'EventHandlerType',
)

logger = logging.getLogger(__name__)


EVENT_T = TypeVar('EVENT_T', bound=GatewayEvent)
"""Type variable for a gateway event.

This old generic alias format to make code complexity lower.
"""

type EventHandlerType[EVENT_T: GatewayEvent] = Callable[Concatenate[EVENT_T, ...], Awaitable[None]]
"""Type alias for an event handler."""


class EventDispatcher:
    """Dispatches events to registered handlers.

    Attributes:
        _handlers: Mapping of event types to event handlers.
        _args: Arguments can be passed to all event handlers.
        _cached_args: Cached arguments to pass to event handlers.
    """

    def __init__(self) -> None:
        """Initialize the event dispatcher."""
        self._handlers: _HandlersMutMapping = defaultdict(list)

        self._args: dict[str, Any] = {}
        self._cached_args: dict[EventHandlerType, dict[str, Any]] = {}

    # fmt: off
    @overload
    def add_handler(
        self,
        event_type: type[EVENT_T],
        event_handler: EventHandlerType[EVENT_T],
    ) -> None:
        ...

    @overload
    def add_handler(self, event_type: EventHandlerType[EVENT_T]) -> None:
        ...
    # fmt: on

    # fmt: on
    def add_handler(
        self,
        event_type: type[EVENT_T] | EventHandlerType[EVENT_T],
        event_handler: EventHandlerType[EVENT_T] | None = None,
    ) -> None:
        """Add a handler for a specific event type.

        If the event type is not specified, the type will be inferred from
        the type hints of the event handler.

        Args:
            event_type: Event type to handle.
            event_handler: Handler to call when the event is dispatched.

        Raises:
            ValueError: If the event type is not specified and cannot be inferred.
        """
        if event_handler is None:
            if callable(event_type):
                if isinstance(event_type, type):
                    event_handler = cast(EventHandlerType, event_type.__call__)
                else:
                    event_handler = cast(EventHandlerType, event_type)
            else:
                raise TypeError(
                    'Event handler must be specified if the event type is not callable',
                )

            event_type = self._infer_event_type(event_handler)

        if not isinstance(event_type, type) or not issubclass(event_type, GatewayEvent):
            raise TypeError(
                'Event type must be specified if the event handler is not',
            )

        if not callable(event_handler):
            raise TypeError('Event handler must be Callable')

        self._update_args_cache(event_handler)
        self._handlers[event_type].append(event_handler)

    def add_argument(self, arg_name: str, arg_value: Any) -> None:  # noqa: ANN401
        """Add an argument to be passed to all event handlers.

        Args:
            arg_name: Name of the argument.
            arg_value: Value of the argument.
        """
        self._args[arg_name] = arg_value
        for event_handlers in self._handlers.values():
            for event_handler in event_handlers:
                self._update_args_cache(event_handler)

    async def dispatch(self, event: GatewayEvent) -> None:
        """Dispatch an event to all handlers.

        Args:
            event: Event to dispatch.
        """
        event_type = type(event)
        for event_handler in self._handlers.get(event_type, []):
            kwargs = self._cached_args[event_handler]
            try:
                await event_handler(event, **kwargs)
            except Exception:
                logger.exception('Unhandled exception in event handler')

    def _update_args_cache(self, event_handler: EventHandlerType[EVENT_T]) -> None:
        """Update the arguments to pass to an event handler.

        Args:
            event_handler: Event handler to update.
        """
        arg_names = event_handler.__code__.co_varnames[1 : event_handler.__code__.co_argcount]

        # fmt: off
        self._cached_args[event_handler] = {
            arg_name: self._args[arg_name]
            for arg_name in arg_names
            if arg_name in self._args
        }
        # fmt: on

    @classmethod
    def _infer_event_type(cls, event_handler: EventHandlerType[EVENT_T]) -> type[EVENT_T]:
        """Infer the event type from the type hints of an event handler."""
        handler_arg_types = list(get_type_hints(event_handler).values())

        if not handler_arg_types:
            raise TypeError(
                'Event handler must have at least one argument for the event',
            )

        return cast(type[EVENT_T], handler_arg_types[0])


type _HandlersMutMapping[EVENT_T: GatewayEvent] = MutableMapping[
    type[EVENT_T],
    list[EventHandlerType[EVENT_T]],
]
"""Type alias for a mutable mapping of event types to event handlers."""
