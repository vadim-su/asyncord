
from asyncord.client.applications.models.responses import GuildApplicationCommandPermissionsOut
from asyncord.gateway.events.base import GatewayEvent


class GuildApplicationCommandPermissionsUpdateEvent(GatewayEvent, GuildApplicationCommandPermissionsOut):
    """Sent when an application command's permissions are updated.

    https://discord.com/developers/docs/topics/gateway-events#application-command-permissions-update
    """
