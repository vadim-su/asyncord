import inspect
from types import MappingProxyType
from typing import Mapping, Generator

from loguru import logger
from rich.pretty import pretty_repr

from asyncord.client.models.events import base, guilds, channels


def _get_all_event_classes(modules: list[object]) -> Generator[type[base.GatewayEvent], None, None]:
    for module in modules:
        for name, some_obj in inspect.getmembers(module):
            is_event_class = (
                name.endswith('Event')
                and issubclass(some_obj, base.GatewayEvent)
                and some_obj != base.GatewayEvent
            )
            if is_event_class:
                yield some_obj


EVENT_MAP: Mapping[str, type[base.GatewayEvent]] = MappingProxyType({
    event_class.__event_name__: event_class
    for event_class in _get_all_event_classes([base, guilds, channels])
})
"""Mapping of event names to event classes.

https://discord.com/developers/docs/topics/gateway#commands-and-events-gateway-events
"""

logger.debug(pretty_repr(EVENT_MAP))
