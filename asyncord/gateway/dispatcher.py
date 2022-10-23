from typing import Any, Generic, TypeVar, Protocol, MutableMapping, cast, overload, get_type_hints
from collections import defaultdict

from asyncord.gateway.events.base import GatewayEvent

EVENT_TYPE = TypeVar('EVENT_TYPE', bound=GatewayEvent)
EVENT_TYPE_T = TypeVar('EVENT_TYPE_T', contravariant=True, bound=GatewayEvent)


class HandlerType(Protocol[EVENT_TYPE_T]):
    async def __call__(self, event: EVENT_TYPE_T, *args, **kwargs) -> None:
        ...


class EventDispatcher(Generic[EVENT_TYPE]):
    """Dispatches events to registered handlers."""

    def __init__(self):
        """Initialize the event dispatcher."""
        self._handlers: MutableMapping[
            type[EVENT_TYPE], list[HandlerType[EVENT_TYPE]],
        ] = defaultdict(list)

        self._args: dict[str, Any] = {}

        self._arg_map: dict[
            HandlerType[EVENT_TYPE], dict[str, Any],
        ] = {}

    @overload
    def add_handler(
        self,
        event_type: type[EVENT_TYPE],
        event_handler: HandlerType[EVENT_TYPE],
    ) -> None:
        ...

    @overload
    def add_handler(self, event_type: HandlerType[EVENT_TYPE]) -> None:
        ...

    def add_handler(
        self,
        event_type: type[EVENT_TYPE] | HandlerType[EVENT_TYPE],
        event_handler: HandlerType[EVENT_TYPE] | None = None,
    ) -> None:
        """Add a handler for a specific event type.

        If the event type is not specified, the type will be inferred from
        the type hints of the event handler.

        Arguments:
            event_type (type[EVENT_TYPE]):  The event type to handle.
            event_handler (HandlerType[EVENT_TYPE] | None):
                The handler to call when the event is dispatched.

        Raises:
            ValueError: If the event type is not specified and cannot be inferred.
        """
        if event_handler is None:
            event_handler = cast(HandlerType[EVENT_TYPE], event_type)
            handler_arg_types = list(get_type_hints(event_handler).values())

            if not handler_arg_types:
                raise ValueError(
                    'Event handler must have at least one argument for the event',
                )

            event_type = cast(type[EVENT_TYPE], handler_arg_types[0])
            if not issubclass(event_type, GatewayEvent):
                raise ValueError(
                    'Event handler must have any gateway event as its first argument',
                )

        event_type = cast(type[EVENT_TYPE], event_type)
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

    async def dispatch(self, event: EVENT_TYPE) -> None:
        """Dispatch an event to all handlers.

        Arguments:
            event (EVENT_TYPE): The event to dispatch.
        """
        event_type = type(event)
        for event_handler in self._handlers.get(event_type, []):
            args = self._arg_map[event_handler]
            await event_handler(event, **args)

    def _update_handler_args(self, event_handler: HandlerType[EVENT_TYPE]) -> None:
        """Update the arguments to pass to an event handler.

        Arguments:
            event_handler (HandlerType[EVENT_TYPE]): The event handler to update.
        """
        args = event_handler.__code__.co_varnames[1: event_handler.__code__.co_argcount]
        self._arg_map[event_handler] = {
            arg: self._args[arg]
            for arg in args
            if arg in self._args
        }
