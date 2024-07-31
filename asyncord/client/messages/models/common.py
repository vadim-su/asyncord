"""Common models for messages."""

import enum
from typing import Literal


@enum.unique
class MessageType(enum.IntEnum):
    """Type of message.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-object-message-types
    """

    DEFAULT = 0
    """Default message."""

    RECIPIENT_ADD = 1
    """Recipient was added to a group DM."""

    RECIPIENT_REMOVE = 2
    """Recipient was removed from a group DM."""

    CALL = 3
    """Call was started in the channel."""

    CHANNEL_NAME_CHANGE = 4
    """Channel name was changed."""

    CHANNEL_ICON_CHANGE = 5
    """Channel icon was changed."""

    CHANNEL_PINNED_MESSAGE = 6
    """Message was pinned."""

    USER_JOIN = 7
    """User joined the guild."""

    GUILD_BOOST = 8
    """User started boosting the guild."""

    GUILD_BOOST_TIER_1 = 9
    """User boosted the guild to tier 1."""

    GUILD_BOOST_TIER_2 = 10
    """User boosted the guild to tier 2."""

    GUILD_BOOST_TIER_3 = 11
    """User boosted the guild to tier 3."""

    CHANNEL_FOLLOW_ADD = 12
    """Channel was followed into a news channel."""

    GUILD_DISCOVERY_DISQUALIFIED = 14
    """Guild discovery disqualification occurred."""

    GUILD_DISCOVERY_REQUALIFIED = 15
    """Guild discovery requalification occurred."""

    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    """Guild discovery grace period initial warning occurred."""

    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    """Guild discovery grace period final warning occurred."""

    THREAD_CREATED = 18
    """Thread was created."""

    REPLY = 19
    """Reply to another message."""

    CHAT_INPUT_COMMAND = 20
    """Message sent in response to an Interaction."""

    THREAD_STARTER_MESSAGE = 21
    """Message in a thread was published to the parent channel."""

    GUILD_INVITE_REMINDER = 22
    """Thread was created from an announcement message with the `HAS_THREAD` flag."""

    CONTEXT_MENU_COMMAND = 23
    """Context menu command was used."""

    AUTO_MODERATION_ACTION = 24
    """Auto moderation action was taken."""

    ROLE_SUBSCRIPTION_PURCHASE = 25
    """User purchased a Nitro subscription."""

    INTERACTION_PREMIUM_UPSELL = 26
    """User has upgraded their guild subscription."""

    STAGE_START = 27
    """Represents start of a stage in a voice channel."""

    STAGE_END = 28
    """Represents end of a stage in a voice channel."""

    STAGE_SPEAKER = 29
    """Represents speaker in a stage in a voice channel."""

    STAGE_TOPIC = 31
    """Represents topic change in a stage in a voice channel."""

    GUILD_APPLICATION_PREMIUM_SUBSCRIPTION = 32
    """Guild application premium subscription."""


@enum.unique
class EmbedType(enum.StrEnum):
    """Object representing the type of an embed.

    Embed types are "loosely defined" and, for the most part, are not used by clients for rendering.
    Embed attributes power what is rendered.
    Embed types should be considered deprecated and might be removed in a future API version.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-types
    """

    RICH = 'rich'
    """Generic embed rendered from embed attributes."""

    IMAGE = 'image'
    """Image embed."""

    VIDEO = 'video'
    """Video embed."""

    GIFV = 'gifv'
    """Animated gif image embed rendered as a video embed."""

    ARTICLE = 'article'
    """Article embed."""

    LINK = 'link'
    """Link embed."""


@enum.unique
class MessageFlags(enum.IntFlag):
    """Message flags.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-object-message-flags
    """

    CROSSPOSTED = 1
    """This message has been published to subscribed channels (via Channel Following)."""

    IS_CROSSPOST = 1 << 1
    """This message originated from a message in another channel (via Channel Following)."""

    SUPPRESS_EMBEDS = 1 << 2
    """Do not include any embeds when serializing this message."""

    SOURCE_MESSAGE_DELETED = 1 << 3
    """The source message for this crosspost has been deleted (via Channel Following)."""

    URGENT = 1 << 4
    """This message came from the urgent message system."""

    HAS_THREAD = 1 << 5
    """This message is part of a thread."""

    EPHEMERAL = 1 << 6
    """This message is ephemeral and only visible to the user who invoked the Interaction."""

    LOADING = 1 << 7
    """This message is an Interaction Response and the bot is 'thinking'."""

    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8
    """This message failed to mention some roles and add their members to the thread."""

    SUPPRESS_NOTIFICATIONS = 1 << 12
    """This message will not trigger push and desktop notifications"""

    IS_VOICE_MESSAGE = 1 << 13
    """This message is a voice message"""


@enum.unique
class AllowedMentionType(enum.Enum):
    """Type of allowed mention.

    Reference:
    https://discord.com/developers/docs/resources/channel#allowed-mentions-object-allowed-mention-types
    """

    ROLES = 'roles'
    """Controls role mentions."""

    USERS = 'users'
    """Controls user mentions."""

    EVERYONE = 'everyone'
    """Controls @everyone and @here mentions."""


@enum.unique
class ComponentType(enum.IntEnum):
    """Component types.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#component-object-component-types
    """

    ACTION_ROW = 1
    """Container for other components."""

    BUTTON = 2
    """Button object."""

    STRING_SELECT = 3
    """Select menu for picking from defined text options."""

    TEXT_INPUT = 4
    """Text input object."""

    USER_SELECT = 5
    """Select menu for users."""

    ROLE_SELECT = 6
    """Select menu for roles."""

    MENTIONABLE_SELECT = 7
    """Select menu for mentionables (users and roles)."""

    CHANNEL_SELECT = 8
    """Select menu for channels."""


SelectComponentType = Literal[
    ComponentType.STRING_SELECT,
    ComponentType.USER_SELECT,
    ComponentType.ROLE_SELECT,
    ComponentType.MENTIONABLE_SELECT,
    ComponentType.CHANNEL_SELECT,
]
"""Type of the component of select menu."""


class ButtonStyle(enum.IntEnum):
    """Button styles.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#button-object-button-styles
    """

    PRIMARY = 1
    """Blurple color.

    Reqired `custom_id`.
    """

    SECONDARY = 2
    """Grey color.

    Reqired `custom_id`.
    """

    SUCCESS = 3
    """Green color.

    Reqired `custom_id`.
    """

    DANGER = 4
    """Red color.

    Reqired `custom_id`.
    """

    LINK = 5
    """Grey with a link icon.

    Reqired `url`.
    """

    PREMIUM = 6
    """Blurple color.

    Reqired `sku_id`.
    """


class TextInputStyle(enum.IntEnum):
    """Text input styles.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#text-input-object-text-input-styles
    """

    SHORT = 1
    """Single-line input."""

    PARAGRAPH = 2
    """Multi-line input."""
