"""Represents the AutoModeration system models."""

from __future__ import annotations

import enum
from typing import Self

from pydantic import BaseModel, Field, FieldValidationInfo, field_validator, model_validator

from asyncord.snowflake import Snowflake

FOUR_WEEKS = 2419200


@enum.unique
class AutoModerationRuleEventType(enum.IntEnum):
    """Indicates in what event context a rule should be checked.

    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-event-types
    """

    MESSAGE_SEND = 1
    """when a member sends or edits a message in the guild"""


@enum.unique
class TriggerType(enum.IntEnum):
    """Indicates what triggers a rule.

    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-trigger-types
    """

    KEYWORD = 1
    """check if content contains words from a user defined list of keywords. Max 3."""

    SPAM = 3
    """check if content represents generic spam. Max 1."""

    KEYWORD_PRESET = 4
    """check if content contains words from internal pre - defined wordsets. Max 1."""

    MENTION_SPAM = 5
    """check if content contains more mentions than allowed. Max 1."""


class TriggerMetadata(BaseModel):
    """Represents the metadata for a rule's trigger.

    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-trigger-metadata
    """

    keyword_filter: list[str]
    """substrings which will be searched for in content.

    Associated with `TriggerType.KEYWORD`.

    A keyword can be a phrase which contains multiple words. Wildcard symbols
    (not available to allow lists) can be used to customize how each keyword
    will be matched.

    See keyword matching [strategies](https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-keyword-matching-strategies).
    """

    presets: int
    """the internally pre - defined wordsets which will be searched for in content.

    Associated with `TriggerType.KEYWORD_PRESET`.
    """

    allow_list: list[str]
    """substrings which will be exempt from triggering the preset trigger type.

    Associated with `TriggerType.KEYWORD_PRESET`.

    A keyword can be a phrase which contains multiple words. Wildcard symbols
    (not available to allow lists) can be used to customize how each keyword
    will be matched.

    See keyword matching [strategies](https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-keyword-matching-strategies).
    """

    mention_total_limit: int = Field(le=50)
    """total number of mentions(role & user) allowed per message (Maximum of 50).

    Associated with `TriggerType.MENTION_SPAM`.
    """


@enum.unique
class RuleActionType(enum.IntEnum):
    """Indicates what action to take when a rule is triggered.

    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-action-object-action-types
    """

    BLOCK_MESSAGE = 1
    """blocks the content of a message according to the rule"""

    SEND_ALERT_MESSAGE = 2
    """logs user content to a specified channel"""

    TIMEOUT = 3
    """timeout user for a specified duration

    The MODERATE_MEMBERS permission is required to use the TIMEOUT action type.
    """


class RuleActionMetadata(BaseModel):
    """Additional data used when an action is executed.

    Different fields are relevant based on the value of `RuleActionType`.

    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-action-object-action-metadata
    """

    channel_id: Snowflake | None = None
    """channel to which user content should be logged"""

    duration_seconds: int | None = Field(None, le=FOUR_WEEKS)
    """timeout duration in seconds (Maximum of 2419200 seconds or 4 weeks)"""


class RuleAction(BaseModel):
    """Represents an action which will execute when a rule is triggered.

    https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-action-object-auto-moderation-action-structure
    """
    type: RuleActionType
    """the type of action"""

    metadata: RuleActionMetadata | None = None
    """the action metadata"""

    @model_validator(mode='after')
    def validate_metadata(self) -> Self:
        """Validate the metadata for the action."""
        match self.type:
            case RuleActionType.BLOCK_MESSAGE:
                if self.metadata:
                    raise ValueError('Metadata is not allowed for `RuleActionType.BLOCK_MESSAGE`')

            case RuleActionType.SEND_ALERT_MESSAGE:
                if not self.metadata or self.metadata.channel_id is None:
                    raise ValueError(
                        '`Metadata.channel_id` is required for `RuleActionType.SEND_ALERT_MESSAGE`',
                    )

            case RuleActionType.TIMEOUT:
                if not self.metadata or self.metadata.duration_seconds is None:
                    raise ValueError('`Metadata.duration_seconds` is required for `RuleActionType.TIMEOUT`')

        return self


class AutoModerationRule(BaseModel):
    """Represents a rule for the AutoModeration system."""

    id: Snowflake
    """The rule's id."""

    guild_id: Snowflake
    """the id of the guild which this rule belongs to"""

    name: str
    """the name of the rule"""

    creator_id: Snowflake
    """the id of the user who created this rule"""

    event_type: AutoModerationRuleEventType
    """the rule event type"""

    trigger_type: TriggerType
    """the rule trigger type"""

    trigger_metadata: TriggerMetadata
    """the rule trigger metadata"""

    actions: list[RuleAction]
    """the actions which will execute when the rule is triggered"""

    enabled: bool
    """whether the rule is enabled"""

    exempt_roles: list[Snowflake] = Field(max_length=20)
    """the role ids that should not be affected by the rule (Maximum of 20)"""

    exempt_channels: list[Snowflake] = Field(max_length=50)
    """the channel ids that should not be affected by the rule (Maximum of 50)"""

    @field_validator('actions')
    def check_actions(cls, actions: list[RuleAction], field_info: FieldValidationInfo) -> list[RuleAction]:
        """Validate actions for the rule."""
        trigger_type: TriggerType = field_info.data['trigger_type']

        keyword_or_mention_spam = trigger_type in {
            TriggerType.KEYWORD,
            TriggerType.MENTION_SPAM,
        }
        for action in actions:
            if action.type is RuleActionType.TIMEOUT and not keyword_or_mention_spam:
                raise ValueError(
                    'Timeout actions can only be used with `TriggerType.KEYWORD` '
                    + 'and `TriggerType.MENTION_SPAM` triggers.',
                )

        return actions
