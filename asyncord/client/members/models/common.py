"""This module contains common models for members."""

import enum


class GuildMemberFlags(enum.IntFlag):
    """Guild member flags.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-member-object-guild-member-flags
    """

    NONE = 0
    """No flags set."""

    DID_REJOIN = 1 << 0
    """Member has left and rejoined the guild"""

    COMPLETED_ONBOARDING = 1 << 1
    """Member has completed onboarding"""

    BYPASSES_VERIFICATION = 1 << 2
    """Member is exempt from guild verification requirements"""

    STARTED_ONBOARDING = 1 << 3
    """Member has started onboarding"""
