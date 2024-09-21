"""Message response models."""

from __future__ import annotations

import datetime
import enum
from collections.abc import Sequence

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel

from asyncord.client.channels.models.common import ChannelType
from asyncord.client.channels.models.responses import ChannelResponse
from asyncord.client.emojis.models.responses import EmojiResponse
from asyncord.client.interactions.models.common import InteractionType
from asyncord.client.members.models.common import GuildMemberFlags
from asyncord.client.members.models.responses import MemberResponse
from asyncord.client.messages.models.common import MessageFlags, MessageType
from asyncord.client.messages.models.responses.components import ComponentOut
from asyncord.client.messages.models.responses.embeds import EmbedOut
from asyncord.client.models.attachments import AttachmentFlags
from asyncord.client.models.stickers import StickerFormatType
from asyncord.client.polls.models.responses import PollResponse
from asyncord.client.roles.models.responses import RoleResponse
from asyncord.client.threads.models.responses import ThreadMetadataOut
from asyncord.client.users.models.responses import UserResponse
from asyncord.color import Color
from asyncord.snowflake import Snowflake
from asyncord.yarl_url import HttpYarlUrl

__all__ = (
    'AttachmentOut',
    'ChannelMentionOut',
    'MessageActivityOut',
    'MessageActivityType',
    'MessageApplicationOut',
    'MessageInteractionOut',
    'MessageReferenceOut',
    'MessageResponse',
    'MessageStickerItemOut',
    'ReactionCountDetailsOut',
    'ReactionOut',
    'ResolvedChannelOut',
    'ResolvedDataOut',
    'ResolvedMemberOut',
    'ResolvedMessageOut',
    'RoleSubscriptionDataOut',
)


class MessageActivityType(enum.IntEnum):
    """Activity type.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-object-message-activity-types
    """

    JOIN = 1
    """Join a party."""

    SPECTATE = 2
    """Spectate a game."""

    LISTEN = 3
    """Listen along to a song."""

    JOIN_REQUEST = 5
    """Join a request to play a game."""


class MessageInteractionOut(BaseModel):
    """Message interaction object.

    This is sent on the message object when the message is a response to
    an Interaction without an existing message.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#message-interaction-object
    """

    id: Snowflake
    """ID of the interaction."""

    type: FallbackAdapter[InteractionType]
    """Type of interaction."""

    name: str
    """Name of the application command, including subcommands and subcommand groups."""

    user: UserResponse
    """User who invoked the interaction."""

    member: MemberResponse | None = None
    """Member who invoked the interaction."""


class MessageReferenceOut(BaseModel):
    """Message reference object.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-reference-object
    """

    message_id: Snowflake | None = None
    """ID of the originating message."""

    channel_id: Snowflake | None = None
    """ID of the originating message's channel."""

    guild_id: Snowflake | None = None
    """ID of the originating message's guild."""

    fail_if_not_exists: bool | None = None
    """Flag to tell the API to return an error object instead.

    When sending a message that references another message, this field determines
    whether to error if the referenced message doesn't exist instead of sending
    the message as a normal (non-reply) message.

    If None is set, the default serverside value is True.
    """


class ChannelMentionOut(BaseModel):
    """Channel mention object.

    Reference:
    https://discord.com/developers/docs/resources/channel#channel-mention-object
    """

    id: Snowflake
    """Channel id."""

    guild_id: Snowflake
    """Guild id containing the channel."""

    type: FallbackAdapter[ChannelType]
    """Channel type."""

    name: str
    """Channel name."""


class AttachmentOut(BaseModel):
    """Attachment object.

    Reference:
    https://discord.com/developers/docs/resources/channel#attachment-object
    """

    id: Snowflake
    """Attachment id."""

    filename: str
    """Name of file attached."""

    description: str | None = None
    """Description for the file."""

    content_type: str | None = None
    """Media type of the file."""

    size: int
    """Size of file in bytes."""

    url: HttpYarlUrl
    """Source url of file."""

    proxy_url: HttpYarlUrl
    """Proxied url of file."""

    height: int | None = None
    """Height of file (if image)."""

    width: int | None = None
    """Width of file (if image)."""

    ephemeral: bool | None = None
    """Whether this attachment is ephemeral.

    Ephemeral attachments will automatically be removed after a set period of time.
    Ephemeral attachments on messages are guaranteed to be available as long as
    the message itself exists.
    """

    duration_secs: float | None = None
    """Duration of the audio file.

    Currently for voice messages.
    """

    waveform: str | None = None
    """base64 encoded bytearray representing a sampled waveform.

    Currently for voice messages
    """

    flags: AttachmentFlags | None = None
    """Attachment flags."""


class MessageActivityOut(BaseModel):
    """Message activity object.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-object-message-activity-structure
    """

    type: MessageActivityType
    """Type of message activity."""

    party_id: str | None = None
    """Party ID from a Rich Presence event."""


class MessageStickerItemOut(BaseModel):
    """Smallest amount of data required to render a sticker.

    Reference:
    https://discord.com/developers/docs/resources/sticker#sticker-item-object
    """

    id: Snowflake
    """Id of the sticker."""

    name: str
    """Name of the sticker."""

    format_type: FallbackAdapter[StickerFormatType]
    """Type of sticker format."""


class RoleSubscriptionDataOut(BaseModel):
    """Role Subscription object.

    Reference:
    https://discord.com/developers/docs/resources/channel#role-subscription-data-object
    """

    role_subscription_listing_id: Snowflake
    """the id of the sku and listing that the user is subscribed to"""

    tier_name: str
    """name of the tier that the user is subscribed to."""

    total_months_subscribed: int
    """cumulative number of months that the user has been subscribed for."""

    is_renewal: bool
    """whether this notification is for a renewal rather than a new purchase"""


# FIXME: It's AI guess, need to be tested
class MessageApplicationOut(BaseModel):
    """Message application object."""

    id: Snowflake
    """ID of the application"""

    cover_image: str | None = None
    """ID of the embed's image asset"""

    description: str
    """Application's description"""

    icon: str | None = None
    """ID of the application's icon"""

    name: str
    """Name of the application"""


class ReactionCountDetailsOut(BaseModel):
    """Reaction Count Details object.

    The reaction count details object contains a breakdown of normal and
    super reaction counts for the associated emoji.
    """

    burst: int
    """Count of super reactions"""

    normal: int
    """Count of normal reactions"""


class ReactionOut(BaseModel):
    """Reaction object.

    Reference:
    https://discord.com/developers/docs/resources/channel#reaction-object
    """

    count: int
    """Times this emoji has been used to react."""

    count_details: ReactionCountDetailsOut
    """Times this emoji has been used to react."""

    me: bool
    """Whether the current user reacted using this emoji."""

    me_burst: bool
    """Whether the current user super-reacted using this emoji."""

    emoji: EmojiResponse
    """Emoji information."""

    burst_colors: list[Color]
    """HEX colors used for super reaction."""


class ResolvedMemberOut(BaseModel):
    """Resolved Member object.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-resolved-data-structure
    """

    nick: str | None = None
    """User's guild nickname"""

    avatar: str | None = None
    """Member's guild avatar hash."""

    roles: list[Snowflake]
    """List of role snowflakes."""

    joined_at: datetime.datetime
    """When the user joined the guild."""

    premium_since: datetime.datetime | None = None
    """When the user started boosting the guild."""

    flags: GuildMemberFlags
    """Guild member flags represented as a bit set, defaults to 0"""

    pending: bool | None = None
    """Whether the user has not yet passed the guild's Membership Screening requirements."""

    permissions: str | None = None
    """Total permissions of the member in the channel, including overwrites.

    Returned when in the interaction object.
    """

    communication_disabled_until: datetime.datetime | None = None
    """When the user's timeout will expire and the user will be able to communicate in the guild again.

    None or a time in the past if the user is not timed out.
    """


class ResolvedChannelOut(BaseModel):
    """Resolved Channel object.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-resolved-data-structure
    """

    id: Snowflake
    """Channel id."""

    type: FallbackAdapter[ChannelType]
    """Type of channel."""

    name: str | None = None
    """Channel name."""

    permissions: str | None = None
    """Computed permissions for the invoking user in the channel, including overwrites.

    Only included when part of the resolved data received on a slash command interaction.
    This does not include implicit permissions, which may need to be checked separately.
    """

    parent_id: Snowflake | None = None
    """Parent category or channel id.

    For guild channels: id of the parent category for a channel.
    for threads:
        id of the text channel this thread was created.
    Each parent category can contain up to 50 channels.
    """

    thread_metadata: ThreadMetadataOut | None = None
    """Thread-specific fields not needed by other channels."""


class ResolvedDataOut(BaseModel):
    """Resolved Data object.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-resolved-data-structure
    """

    users: dict[Snowflake, UserResponse] | None = None
    """Ids and User objects."""

    members: dict[Snowflake, ResolvedMemberOut] | None = None
    """Ids and partial Member objects."""

    roles: dict[Snowflake, RoleResponse] | None = None
    """Ids and Role objects."""

    channels: dict[Snowflake, ResolvedChannelOut] | None = None
    """Ids and partial Channel objects."""

    messages: dict[Snowflake, ResolvedMessageOut] | None = None
    """Ids and partial Message objects."""

    attachments: dict[Snowflake, AttachmentOut] | None = None
    """Ids and attachment objects."""


class MessageResponse(BaseModel):
    """Message object.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-object
    """

    id: Snowflake
    """ID of the message."""

    channel_id: Snowflake
    """ID of the channel the message was sent in."""

    author: UserResponse
    """Author of the message."""

    content: str
    """Contents of the message."""

    timestamp: datetime.datetime
    """When this message was sent."""

    edited_timestamp: datetime.datetime | None = None
    """When this message was edited (or null if never)."""

    tts: bool
    """Whether this was a TTS message."""

    mention_everyone: bool
    """Whether this message mentions everyone."""

    mentions: list[UserResponse]
    """Users specifically mentioned in the message."""

    mention_roles: list[Snowflake]
    """Roles specifically mentioned in this message."""

    mention_channels: list[ChannelMentionOut] | None = None
    """Channels specifically mentioned in this message."""

    attachments: list[AttachmentOut]
    """Any attached files."""

    embeds: list[EmbedOut]
    """Any embedded content."""

    reactions: list[ReactionOut] | None = None
    """Any reactions to the message."""

    nonce: int | str | None = None
    """Used for validating a message was sent."""

    pinned: bool
    """Whether this message is pinned."""

    webhook_id: Snowflake | None = None
    """If the message is generated by a webhook, this is the webhook's id."""

    type: FallbackAdapter[MessageType]
    """Type of message."""

    activity: MessageActivityOut | None = None
    """Sent with Rich Presence-related chat embeds."""

    application: MessageApplicationOut | None = None
    """Sent with Rich Presence-related chat embeds."""

    application_id: Snowflake | None = None
    """If the message is an Interaction or application-owned webhook.

    This is the id of the application.
    """

    message_reference: MessageReferenceOut | None = None
    """Reference data sent with crossposted messages."""

    flags: MessageFlags
    """Message flags combined as a bitfield."""

    referenced_message: MessageResponse | None = None
    """The message this message references, if the message is a reply."""

    interaction: MessageInteractionOut | None = None
    """Sent if the message is a response to an Interaction."""

    thread: ChannelResponse | None = None
    """The thread that was started from this message, includes thread member object."""

    components: Sequence[ComponentOut] | None = None
    """Sent if the message is a response to an Interaction."""

    sticker_items: list[MessageStickerItemOut] | None = None
    """Sent if the message contains stickers"""

    position: int | None = None
    """Generally increasing integer (there may be gaps or duplicates)

    Represents the approximate position of the message in a thread,
    it can be used to estimate the relative position of the message in a thread
    in company with total_message_sent on parent thread
    """

    role_subscription_data: RoleSubscriptionDataOut | None = None
    """Data of the role subscription purchase or renewal.

    That prompted this ROLE_SUBSCRIPTION_PURCHASE message.
    """

    resolved: ResolvedDataOut | None = None
    """Data for users, members, channels, and roles.

    In the message's auto-populated select menus.
    """

    poll: PollResponse | None = None
    """A poll."""


class ResolvedMessageOut(BaseModel):
    """Partial Message object.

    No documentation on this.
    The copy of the whole model, but all fields are optional.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-resolved-data-structure
    """

    id: Snowflake | None = None
    """ID of the message."""

    channel_id: Snowflake | None = None
    """ID of the channel the message was sent in."""

    author: UserResponse | None = None
    """Author of the message."""

    content: str | None = None
    """Contents of the message."""

    timestamp: datetime.datetime | None = None
    """When this message was sent."""

    edited_timestamp: datetime.datetime | None = None
    """When this message was edited (or null if never)."""

    tts: bool | None = None
    """Whether this was a TTS message."""

    mention_everyone: bool | None = None
    """Whether this message mentions everyone."""

    mentions: list[UserResponse] | None = None
    """Users specifically mentioned in the message."""

    mention_roles: list[Snowflake] | None = None
    """Roles specifically mentioned in this message."""

    mention_channels: list[ChannelMentionOut] | None = None
    """Channels specifically mentioned in this message."""

    attachments: list[AttachmentOut] | None = None
    """Any attached files."""

    embeds: list[EmbedOut] | None = None
    """Any embedded content."""

    reactions: list[ReactionOut] | None = None
    """Any reactions to the message."""

    nonce: int | str | None = None
    """Used for validating a message was sent."""

    pinned: bool | None = None
    """Whether this message is pinned."""

    webhook_id: Snowflake | None = None
    """If the message is generated by a webhook, this is the webhook's id."""

    type: FallbackAdapter[MessageType] | None = None
    """Type of message."""

    activity: MessageActivityOut | None = None
    """Sent with Rich Presence-related chat embeds."""

    application: MessageApplicationOut | None = None
    """Sent with Rich Presence-related chat embeds."""

    application_id: Snowflake | None = None
    """If the message is an Interaction or application-owned webhook.

    This is the id of the application.
    """

    message_reference: MessageReferenceOut | None = None
    """Reference data sent with crossposted messages."""

    flags: MessageFlags | None = None
    """Message flags combined as a bitfield."""

    referenced_message: MessageResponse | None = None
    """The message this message references, if the message is a reply."""

    interaction: MessageInteractionOut | None = None
    """Sent if the message is a response to an Interaction."""

    thread: ChannelResponse | None = None
    """The thread that was started from this message, includes thread member object."""

    components: Sequence[ComponentOut] | None = None
    """Sent if the message is a response to an Interaction."""

    sticker_items: list[MessageStickerItemOut] | None = None
    """Sent if the message contains stickers"""

    position: int | None = None
    """Generally increasing integer (there may be gaps or duplicates)

    Represents the approximate position of the message in a thread,
    it can be used to estimate the relative position of the message in a thread
    in company with total_message_sent on parent thread
    """

    role_subscription_data: RoleSubscriptionDataOut | None = None
    """Data of the role subscription purchase or renewal.

    That prompted this ROLE_SUBSCRIPTION_PURCHASE message.
    """

    resolved: ResolvedDataOut | None = None
    """Data for users, members, channels, and roles.

    In the message's auto-populated select menus.
    """

    poll: PollResponse | None = None
    """A poll."""
