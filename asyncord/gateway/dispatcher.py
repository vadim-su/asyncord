from typing import (  # noqa: WPS235  # Found too many imported names from a module
    Any,
    Generic,
    TypeVar,
    Callable,
    Awaitable,
    ParamSpec,
    Concatenate,
    MutableMapping,
    cast,
    overload,
    get_type_hints,
)
from collections import defaultdict

from loguru import logger
from rich.logging import RichHandler

from asyncord.gateway.events.base import GatewayEvent

_EVENT_T = TypeVar('_EVENT_T', bound=GatewayEvent)
_EVENT_HANDLERS_P = ParamSpec('_EVENT_HANDLERS_P')

EventHandlerType = Callable[Concatenate[_EVENT_T, _EVENT_HANDLERS_P], Awaitable[None]]

logger.configure(handlers=[{
    'sink': RichHandler(
        omit_repeated_times=False,
        rich_tracebacks=True,
    ),
    'format': '{message}',
    # 'level': 'INFO',
}])


class EventDispatcher(Generic[_EVENT_T]):
    """Dispatches events to registered handlers."""

    def __init__(self):
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

        Arguments:
            event_type (type[_EVENT_T]):  The event type to handle.
            event_handler (EventHandlerType[_EVENT_T] | None):
                The handler to call when the event is dispatched.

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

    def add_argument(self, arg_name: str, arg_value: Any) -> None:
        """Add an argument to be passed to all event handlers.

        Arguments:
            arg_name (str): The name of the argument.
            arg_value (Any): The value of the argument.
        """
        self._args[arg_name] = arg_value
        for event_handlers in self._handlers.values():
            for event_handler in event_handlers:
                self._update_handler_args(event_handler)

    async def dispatch(self, event: _EVENT_T) -> None:
        """Dispatch an event to all handlers.

        Arguments:
            event (_EVENT_T): The event to dispatch.
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

        Arguments:
            event_handler (EventHandlerType[_EVENT_T]): The event handler to update.
        """
        args = event_handler.__code__.co_varnames[1: event_handler.__code__.co_argcount]
        self._arg_map[event_handler] = {
            arg: self._args[arg]
            for arg in args
            if arg in self._args
        }
