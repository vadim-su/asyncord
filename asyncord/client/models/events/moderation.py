"""All auto moderation related events are currently only sent to bot users
which have the MANAGE_GUILD permission.
"""
from asyncord.snowflake import Snowflake
from asyncord.client.models.events.base import GatewayEvent
from asyncord.client.models.automoderation import RuleAction, TriggerType, AutoModerationRule


class AutoModerationRuleCreateEvent(GatewayEvent, AutoModerationRule):
    """https://discord.com/developers/docs/topics/gateway#auto-moderation-rule-create"""


class AutoModerationRuleUpdateEvent(GatewayEvent, AutoModerationRule):
    """https://discord.com/developers/docs/topics/gateway#auto-moderation-rule-create"""


class AutoModerationRuleDeleteEvent(GatewayEvent, AutoModerationRule):
    """https://discord.com/developers/docs/topics/gateway#auto-moderation-rule-create"""


class AutoModerationActionExecutionEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#auto-moderation-action-execution"""

    guild_id: Snowflake
    """the id of the guild in which action was executed"""

    action: RuleAction
    """the action which was executed"""

    rule_id: Snowflake
    """the id of the rule which action belongs to"""

    rule_trigger_type: TriggerType
    """the trigger type of rule which was triggered"""

    user_id: Snowflake
    """the id of the user which generated the content which triggered the rule"""

    channel_id: Snowflake | None = None
    """the id of the channel in which user content was posted"""

    message_id: Snowflake | None = None
    """the id of any user message which content belongs to

    `message_id` will not exist if message was blocked by automod or
    content was not part of any message
    """

    alert_system_message_id: Snowflake | None = None
    """the id of any system auto moderation messages posted as a result of this action

    `alert_system_message_id` will not exist if this event does not correspond to
    an action with type `RuleActionType.SEND_ALERT_MESSAGE`
    """
    content: str
    """the user generated text content

    Required MESSAGE_CONTENT (1 << 15). Read the message content intent section
    for [details](https://discord.com/developers/docs/topics/gateway#message-content-intent).
    """
    matched_keyword: str | None
    """the word or phrase configured in the rule that triggered the rule"""

    matched_content: str | None
    """the substring in content that triggered the rule

    Required MESSAGE_CONTENT (1 << 15). Read the message content intent section
    for [details](https://discord.com/developers/docs/topics/gateway#message-content-intent).
    """
