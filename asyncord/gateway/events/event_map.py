import inspect
from collections.abc import Generator, Mapping
from types import MappingProxyType

from loguru import logger
from rich.pretty import pretty_repr

from asyncord.gateway.events import (
    application,
    base,
    channels,
    guilds,
    interactions,
    messages,
    moderation,
    presence,
    schedule,
)


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
    for event_class in _get_all_event_classes([
        application,
        base,
        channels,
        guilds,
        interactions,
        messages,
        moderation,
        presence,
        schedule,
    ])
})
"""Mapping of event names to event classes.

https://discord.com/developers/docs/topics/gateway-events#commands-and-events-gateway-events
"""

logger.debug(pretty_repr(EVENT_MAP))
