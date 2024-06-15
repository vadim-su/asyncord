"""This module contains moderation events for the gateway.

All auto moderation related events are currently only sent to bot users which have the MANAGE_GUILD permission.
"""

from fbenum.adapter import FallbackAdapter

from asyncord.client.models.automoderation import AutoModerationRule, RuleAction, TriggerType
from asyncord.gateway.events.base import GatewayEvent
from asyncord.snowflake import Snowflake

__all__ = (
    'AutoModerationActionExecutionEvent',
    'AutoModerationRuleCreateEvent',
    'AutoModerationRuleDeleteEvent',
    'AutoModerationRuleUpdateEvent',
)


class AutoModerationRuleCreateEvent(GatewayEvent, AutoModerationRule):
    """Sent when a new auto moderation rule is created.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-create
    """


class AutoModerationRuleUpdateEvent(GatewayEvent, AutoModerationRule):
    """Sent when an auto moderation rule is updated.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-create
    """


class AutoModerationRuleDeleteEvent(GatewayEvent, AutoModerationRule):
    """Sent when an auto moderation rule is deleted.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-create
    """


class AutoModerationActionExecutionEvent(GatewayEvent):
    """Sent when an auto moderation action is executed.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#auto-moderation-action-execution
    """

    guild_id: Snowflake
    """Guild id in which action was executed."""

    action: RuleAction
    """Action which was executed."""

    rule_id: Snowflake
    """Rule id which action belongs to."""

    rule_trigger_type: FallbackAdapter[TriggerType]
    """Trigger type of rule which was triggered."""

    user_id: Snowflake
    """User id which generated the content which triggered the rule."""

    channel_id: Snowflake | None = None
    """Channel id in which user content was posted."""

    message_id: Snowflake | None = None
    """Id of any user message which content belongs to.

    `message_id` will not exist if message was blocked by automod or
    content was not part of any message.
    """

    alert_system_message_id: Snowflake | None = None
    """Id of any system auto moderation messages posted as a result of this action.

    `alert_system_message_id` will not exist if this event does not correspond to
    an action with type `RuleActionType.SEND_ALERT_MESSAGE`.
    """

    content: str
    """User generated text content.

    Required MESSAGE_CONTENT (1 << 15).

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#message-content-intent
    """
    matched_keyword: str | None
    """the word or phrase configured in the rule that triggered the rule."""

    matched_content: str | None
    """Substring in content that triggered the rule.

    Required MESSAGE_CONTENT (1 << 15).

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#message-content-intent
    """
