"""Represents the AutoModeration system models."""

from __future__ import annotations

import enum
from typing import Annotated

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel, Field

from asyncord.snowflake import Snowflake

__all__ = (
    'AutoModerationRule',
    'AutoModerationRuleEventType',
    'RuleAction',
    'RuleActionMetadata',
    'RuleActionType',
    'TriggerMetadata',
    'TriggerType',
)

FOUR_WEEKS_SECS = 2419200
"""4 weeks in seconds."""


@enum.unique
class AutoModerationRuleEventType(enum.IntEnum):
    """Indicates in what event context a rule should be checked.

    Reference:
    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-event-types
    """

    MESSAGE_SEND = 1
    """When a member sends or edits a message in the guild."""


@enum.unique
class TriggerType(enum.IntEnum):
    """Indicates what triggers a rule.

    Reference:
    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-trigger-types
    """

    KEYWORD = 1
    """Check if content contains words from a user defined list of keywords.

    Maxiumum of 10.
    """

    SPAM = 3
    """Check if content represents generic spam.

    Maximum of 1.
    """

    KEYWORD_PRESET = 4
    """Check if content contains words from internal pre-defined wordsets.

    Maximum of 1.
    """

    MENTION_SPAM = 5
    """Check if content contains more mentions than allowed.

    Maximum of 1.
    """


class TriggerMetadata(BaseModel):
    """Represents the metadata for a rule's trigger.

    Reference:
    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-trigger-metadata
    """

    keyword_filter: list[str] | None = None
    """Substrings which will be searched for in content.

    Associated with `TriggerType.KEYWORD`.

    A keyword can be a phrase which contains multiple words. Wildcard symbols
    (not available to allow lists) can be used to customize how each keyword
    will be matched.

    Reference:
    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-keyword-matching-strategies
    """

    regex_patterns: Annotated[list[str] | None, Field(max_length=10)] = None
    """regular expression patterns which will be matched against content (Maximum of 10)

    Associated with `TriggerType.KEYWORD`.

    Only Rust flavored regex is currently supported,
    which can be tested in online editors such as Rustexp.
    Each regex pattern must be 260 characters or less.
    """

    presets: int | None = None
    """Internally pre-defined wordsets which will be searched for in content.

    Associated with `TriggerType.KEYWORD_PRESET`.
    """

    allow_list: Annotated[list[str] | None, Field(max_length=1000)] = None
    """Substrings which will be exempt from triggering the preset trigger type.

    Associated with `TriggerType.KEYWORD` and `TriggerType.KEYWORD_PRESET`.

    Maximum of 100/1000 for `TriggerType.KEYWORD`/`TriggerType.KEYWORD_PRESET`.

    A keyword can be a phrase which contains multiple words. Wildcard symbols
    (not available to allow lists) can be used to customize how each keyword
    will be matched.

    Reference:
    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-keyword-matching-strategies
    """

    mention_total_limit: Annotated[int | None, Field(le=50)] = None
    """Total number of mentions(role & user) allowed per message.

    Maximum of 50.
    Associated with `TriggerType.MENTION_SPAM`.
    """

    mention_raid_protection_enabled: bool | None = None
    """Whether to automatically detect mention raids.

    Associated with `TriggerType.MENTION_SPAM`.
    """


@enum.unique
class RuleActionType(enum.IntEnum):
    """Indicates what action to take when a rule is triggered.

    Reference:
    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-action-object-action-types
    """

    BLOCK_MESSAGE = 1
    """Blocks the content of a message according to the rule."""

    SEND_ALERT_MESSAGE = 2
    """Logs user content to a specified channel."""

    TIMEOUT = 3
    """Timeout user for a specified duration.

    The MODERATE_MEMBERS permission is required to use the TIMEOUT action type.
    """


class RuleActionMetadata(BaseModel):
    """Additional data used when an action is executed.

    Different fields are relevant based on the value of `RuleActionType`.

    Reference:
    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-action-object-action-metadata
    """

    channel_id: Snowflake | None = None
    """Channel to which user content should be logged."""

    duration_seconds: int | None = Field(None, le=FOUR_WEEKS_SECS)
    """Timeout duration in seconds.

    Maximum of 2419200 seconds or 4 weeks.
    """

    custom_message: str | None = Field(None, max_length=150)
    """Additional explanation that will be shown to members whenever their message is blocked

    Maximum of 150 characters
    """


class RuleAction(BaseModel):
    """Represents an action which will execute when a rule is triggered.

    Reference:
    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-action-object-auto-moderation-action-structure
    """

    type: RuleActionType
    """Type of action."""

    metadata: RuleActionMetadata | None = None
    """Action metadata."""


class AutoModerationRule(BaseModel):
    """Represents a rule for AutoModeration system.

    Reference:
    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object
    """

    id: Snowflake
    """Rule's id."""

    guild_id: Snowflake
    """ID of guild which this rule belongs to."""

    name: str
    """Name of the rule."""

    creator_id: Snowflake
    """ID of the user who created this rule."""

    event_type: FallbackAdapter[AutoModerationRuleEventType]
    """Rule event type."""

    trigger_type: FallbackAdapter[TriggerType]
    """Rule trigger type."""

    trigger_metadata: TriggerMetadata
    """Rule trigger metadata."""

    actions: list[RuleAction]
    """Actions which will execute when the rule is triggered."""

    enabled: bool
    """Whether the rule is enabled."""

    exempt_roles: list[Snowflake] = Field(max_length=20)
    """Role ids that should not be affected by the rule.

    Maximum of 20.
    """

    exempt_channels: list[Snowflake] = Field(max_length=50)
    """Channel ids that should not be affected by the rule.

    Maximum of 50.
    """
