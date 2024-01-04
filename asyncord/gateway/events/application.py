
from asyncord.client.applications.models import GuildApplicationCommandPermissions
from asyncord.gateway.events.base import GatewayEvent


class GuildApplicationCommandPermissionsUpdateEvent(GatewayEvent, GuildApplicationCommandPermissions):
    """Sent when an application command's permissions are updated.

    https://discord.com/developers/docs/topics/gateway-events#application-command-permissions-update
    """
