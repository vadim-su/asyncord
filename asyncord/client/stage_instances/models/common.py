"""Common models for stage instances."""

import enum


@enum.unique
class StageInstancePrivacyLevel(enum.IntEnum):
    """Privacy level of a stage instance.

    Reference:
    https://discord.com/developers/docs/resources/stage-instance#stage-instance-object-privacy-level
    """

    GUILD_ONLY = 2
    """Stage instance is visible to only guild members."""
