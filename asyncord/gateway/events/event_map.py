"""Mapping of event names to event classes."""

import inspect
import logging
from collections.abc import Generator, Mapping
from types import MappingProxyType

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
    scheduled_events,
)

logger = logging.getLogger(__name__)


def _get_all_event_classes(modules: list[object]) -> Generator[type[base.GatewayEvent], None, None]:
    for module in modules:
        for name, some_obj in inspect.getmembers(module):
            is_event_class = (
                name.endswith('Event')
                and issubclass(some_obj, base.GatewayEvent)
                and some_obj is not base.GatewayEvent
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
        scheduled_events,
    ])
})
"""Mapping of event names to event classes.

https://discord.com/developers/docs/topics/gateway-events#commands-and-events-gateway-events
"""

logger.debug("The EVENT_MAP contains %d events:\n%s", len(EVENT_MAP), pretty_repr(EVENT_MAP))
