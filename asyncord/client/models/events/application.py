
from asyncord.client.models.events.base import GatewayEvent
from asyncord.client.models.applications import GuildApplicationCommandPermissions


class GuildApplicationCommandPermissionsUpdateEvent(GatewayEvent, GuildApplicationCommandPermissions):
    """https://discord.com/developers/docs/topics/gateway#application-command-permissions-update"""
