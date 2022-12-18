
from asyncord.gateway.events.base import GatewayEvent
from asyncord.client.models.applications import GuildApplicationCommandPermissions


class GuildApplicationCommandPermissionsUpdateEvent(GatewayEvent, GuildApplicationCommandPermissions):
    """Sent when an application command's permissions are updated.

    https://discord.com/developers/docs/topics/gateway-events#application-command-permissions-update
    """
