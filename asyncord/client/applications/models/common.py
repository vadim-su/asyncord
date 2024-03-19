"""This module contains the common models for the applications resources."""

import enum


@enum.unique
class ApplicationCommandPermissionType(enum.IntEnum):
    """Discord application command permission type.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-permissions-object-application-command-permission-type
    """

    ROLE = 1
    """Role permission type"""

    USER = 2
    """User permission type"""

    CHANNEL = 3
    """Channel permission type"""


@enum.unique
class MembershipState(enum.Enum):
    """Discord team member's membership state.

    https://discord.com/developers/docs/topics/teams#data-models-membership-state-enum
    """

    INVITED = 1
    """the user has been invited to the team but has not yet accepted"""

    ACCEPTED = 2
    """the user has accepted the team invite"""


@enum.unique
class ApplicationFlag(enum.IntFlag):
    """Discord application flag.

    https://discord.com/developers/docs/resources/application#application-object-application-flags
    """

    APPLICATION_AUTO_MODERATION_RULE_CREATE_BADGE = 1 << 6
    GATEWAY_PRESENCE = 1 << 12
    GATEWAY_PRESENCE_LIMITED = 1 << 13
    GATEWAY_GUILD_MEMBERS = 1 << 14
    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    EMBEDDED = 1 << 17
    GATEWAY_MESSAGE_CONTENT = 1 << 18
    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19
    APPLICATION_COMMAND_BADGE = 1 << 23
