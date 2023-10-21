"""This module defines the EventDispatcher class, which dispatches events to registered handlers."""

import logging
from collections import defaultdict
from collections.abc import Awaitable, Callable, MutableMapping
from typing import (
    Any,
    Concatenate,
    Generic,
    ParamSpec,
    TypeVar,
    cast,
    get_type_hints,
    overload,
)

from asyncord.gateway.events.base import GatewayEvent

_EVENT_T = TypeVar('_EVENT_T', bound=GatewayEvent)
_EVENT_HANDLERS_P = ParamSpec('_EVENT_HANDLERS_P')

EventHandlerType = Callable[Concatenate[_EVENT_T, _EVENT_HANDLERS_P], Awaitable[None]]

logger = logging.getLogger(__name__)


class EventDispatcher(Generic[_EVENT_T]):
    """Dispatches events to registered handlers."""

    def __init__(self) -> None:
        """Initialize the event dispatcher."""
        self._handlers: MutableMapping[
            type[_EVENT_T], list[EventHandlerType[_EVENT_T, ...]],
        ] = defaultdict(list)

        self._args: dict[str, Any] = {}

        self._arg_map: dict[
            EventHandlerType[_EVENT_T, ...], dict[str, Any],
        ] = {}

    @overload
    def add_handler(
        self,
        event_type: type[_EVENT_T],
        event_handler: EventHandlerType[_EVENT_T, ...],
    ) -> None:
        ...

    @overload
    def add_handler(self, event_type: EventHandlerType[_EVENT_T, ...]) -> None:
        ...

    def add_handler(
        self,
        event_type: type[_EVENT_T] | EventHandlerType[_EVENT_T, ...],
        event_handler: EventHandlerType[_EVENT_T, ...] | None = None,
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
            event_handler = cast(EventHandlerType[_EVENT_T, ...], event_type)
            handler_arg_types = list(get_type_hints(event_handler).values())

            if not handler_arg_types:
                raise ValueError(
                    'Event handler must have at least one argument for the event',
                )

            event_type = cast(type[_EVENT_T], handler_arg_types[0])
            if not issubclass(event_type, GatewayEvent):
                raise ValueError(
                    'Event handler must have any gateway event as its first argument',
                )

        event_type = cast(type[_EVENT_T], event_type)
        self._update_handler_args(event_handler)
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
                self._update_handler_args(event_handler)

    async def dispatch(self, event: _EVENT_T) -> None:
        """Dispatch an event to all handlers.

        Args:
            event: Event to dispatch.
        """
        event_type = type(event)
        for event_handler in self._handlers.get(event_type, []):
            kwargs = self._arg_map[event_handler]
            try:
                await event_handler(event, **kwargs)
            except Exception as exc:
                logger.exception(exc)

    def _update_handler_args(self, event_handler: EventHandlerType[_EVENT_T, ...]) -> None:
        """Update the arguments to pass to an event handler.

        Args:
            event_handler: Event handler to update.
        """
        args = event_handler.__code__.co_varnames[1: event_handler.__code__.co_argcount]
        self._arg_map[event_handler] = {
            arg: self._args[arg]
            for arg in args
            if arg in self._args
        }
