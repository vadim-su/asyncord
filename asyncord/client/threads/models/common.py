"""Common models for threads."""

import enum


@enum.unique
class ThreadType(enum.IntEnum):
    """Thread type.

    Reference:
    https://discord.com/developers/docs/resources/channel#channel-object-channel-types
    """

    ANNOUNCEMENT_THREAD = 10
    """Temporary sub-channel within a GUILD_ANNOUNCEMENT channel."""

    GUILD_PUBLIC_THREAD = 11
    """Temporary sub-channel within a GUILD_TEXT channel."""

    GUILD_PRIVATE_THREAD = 12
    """Temporary sub-channel within a `GUILD_TEXT` channel.

    The channel is only viewable by those invited and those with
    the `MANAGE_THREADS` permission.
    """
