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

    Reference:
    https://discord.com/developers/docs/topics/teams#data-models-membership-state-enum
    """

    INVITED = 1
    """the user has been invited to the team but has not yet accepted"""

    ACCEPTED = 2
    """the user has accepted the team invite"""


@enum.unique
class ApplicationFlag(enum.IntFlag):
    """Discord application flag.

    Reference:
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


@enum.unique
class ApplicationRoleConnectionMetadataType(enum.IntEnum):
    """Discord application role connection metadata type.

    Reference:
    https://discord.com/developers/docs/resources/application-role-connection-metadata#application-role-connection-metadata-object-application-role-connection-metadata-type
    """

    INTEGER_LESS_THAN_OR_EQUAL = 1
    """Metadata value is less than or equal to the guild's configured value."""

    INTEGER_GREATER_THAN_OR_EQUAL = 2
    """Metadata value is greater than or equal to the guild's configured value."""

    INTEGER_EQUAL = 3
    """Metadata value  is equal to the guild's configured value .
    """

    INTEGER_NOT_EQUAL = 4
    """Metadata value  is not equal to the guild's configured value."""

    DATETIME_LESS_THAN_OR_EQUAL = 5
    """Metadata value is less than or equal to the guild's configured value.

    Days besfore current date.
    """

    DATETIME_GREATER_THAN_OR_EQUAL = 6
    """Metadata value is greater than or equal to the guild's configured value.

    Days before current date.
    """

    BOOLEAN_EQUAL = 7
    """Metadata value is equal to the guild's configured value."""

    BOOLEAN_NOT_EQUAL = 8
    """Metadata value  is not equal to the guild's configured value."""
