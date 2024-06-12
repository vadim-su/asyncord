"""This module contains the common models for a poll."""

import enum


class PollLayoutType(enum.IntEnum):
    """Poll layout type.

    Reference:
    https://discord.com/developers/docs/resources/poll#layout-type
    """

    DEFAULT = 1
