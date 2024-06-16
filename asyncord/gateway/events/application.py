"""This module contains application events for the gateway."""

from asyncord.client.applications.models.responses import GuildApplicationCommandPermissionsOut
from asyncord.gateway.events.base import GatewayEvent

__all__ = ('GuildApplicationCommandPermissionsUpdateEvent',)


class GuildApplicationCommandPermissionsUpdateEvent(GatewayEvent, GuildApplicationCommandPermissionsOut):
    """Sent when an application command's permissions are updated.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#application-command-permissions-update
    """
