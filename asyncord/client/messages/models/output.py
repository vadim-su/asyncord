from __future__ import annotations

import datetime
import enum

from pydantic import AnyHttpUrl, BaseModel, Field

from asyncord.client.channels.models.common import ChannelType
from asyncord.client.channels.models.output import ChannelOutput, ThreadMetadataOutput
from asyncord.client.interactions.models.common import InteractionType
from asyncord.client.members.models import GuildMemberFlags, MemberOutput
from asyncord.client.messages.models.common import AttachmentFlags, MessageFlags, MessageType
from asyncord.client.messages.models.components_output import ComponentOutput
from asyncord.client.messages.models.embed_output import EmbedOutput
from asyncord.client.models.emoji import Emoji
from asyncord.client.models.stickers import StickerFormatType
from asyncord.client.roles.models import RoleOutput
from asyncord.client.users.models import UserOutput
from asyncord.color import Color
from asyncord.snowflake import Snowflake


class MessageInteractionOutput(BaseModel):
    """Message interaction object.

    This is sent on the message object when the message is a response to
    an Interaction without an existing message.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#message-interaction-object
    """

    id: Snowflake
    """ID of the interaction."""

    type: InteractionType
    """Type of interaction."""

    name: str
    """Name of the application command, including subcommands and subcommand groups."""

    user: UserOutput
    """User who invoked the interaction."""

    member: MemberOutput | None = None
    """Member who invoked the interaction."""


class MessageReferenceOutput(BaseModel):
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


class ChannelMentionOutput(BaseModel):
    """Channel mention object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#channel-mention-object
    """

    id: Snowflake
    """Channel id."""

    guild_id: Snowflake
    """Guild id containing the channel."""

    type: ChannelType
    """Channel type."""

    name: str
    """Channel name."""


class AttachmentOutput(BaseModel):
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

    url: AnyHttpUrl
    """Source url of file."""

    proxy_url: AnyHttpUrl
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


class MessageActivity(BaseModel):
    """Message activity object.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-object-message-activity-structure
    """

    type: MessageActivityType
    """Type of message activity."""

    party_id: str | None = None
    """Party ID from a Rich Presence event."""


class MessageStickerItemOutput(BaseModel):
    """Smallest amount of data required to render a sticker.

    Reference:
    https://discord.com/developers/docs/resources/sticker#sticker-item-object
    """

    id: Snowflake
    """Id of the sticker."""

    name: str
    """Name of the sticker."""

    format_type: StickerFormatType
    """Type of sticker format."""


class RoleSubscriptionDataOutput(BaseModel):
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
class MessageApplicationOutput(BaseModel):
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


class ReactionCountDetailsOutput(BaseModel):
    """Reaction Count Details object.

    The reaction count details object contains a breakdown of normal and 
    super reaction counts for the associated emoji.
    """
    burst: int
    """Count of super reactions"""

    normal: int
    """Count of normal reactions"""


class ReactionOutput(BaseModel):
    """Reaction object.

    Reference:
    https://discord.com/developers/docs/resources/channel#reaction-object
    """

    count: int
    """Times this emoji has been used to react."""

    count_details: ReactionCountDetailsOutput
    """Times this emoji has been used to react."""

    me: bool
    """Whether the current user reacted using this emoji."""

    me_burst: bool
    """Whether the current user super-reacted using this emoji."""

    emoji: Emoji
    """Emoji information."""

    burst_colors: list[Color]
    """HEX colors used for super reaction."""


class ResolvedMember(BaseModel):
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


class ResolvedChannel(BaseModel):
    """Resolved Channel object.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-resolved-data-structure
    """
    id: Snowflake
    """Channel id."""

    type: ChannelType
    """Type of channel."""

    name: str | None = Field(None, min_length=1, max_length=100)
    """Channel name (1-100 characters)"""

    permissions: str | None = None
    """Computed permissions for the invoking user in the channel,
    including overwrites.
     
    Only included when part of the resolved data received 
    on a slash command interaction. This does not include implicit permissions, 
    which may need to be checked separately
    """

    parent_id: Snowflake | None = None
    """Parent category or channel id.

    For guild channels: id of the parent category for a channel.
    for threads:
        id of the text channel this thread was created.
    Each parent category can contain up to 50 channels.
    """

    thread_metadata: ThreadMetadataOutput | None = None
    """Thread-specific fields not needed by other channels."""


class ResolvedDataOutput(BaseModel):
    """Resolved Data object.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-resolved-data-structure
    """

    users: dict[Snowflake, UserOutput] | None = None
    """Ids and User objects."""

    members: dict[Snowflake, ResolvedMember] | None = None
    """Ids and partial Member objects."""

    roles: dict[Snowflake, RoleOutput] | None = None
    """Ids and Role objects."""

    channels: dict[Snowflake, ResolvedChannel] | None = None
    """Ids and partial Channel objects."""

    # FIXME: Partial Message object, not Message object
    # No ducomentation on this
    messages: dict[Snowflake, MessageOutput] | None = None
    """Ids and partial Message objects."""

    attachments: dict[Snowflake, AttachmentOutput] | None = None
    """Ids and attachment objects."""


class MessageOutput(BaseModel):
    """Message object.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-object
    """

    id: Snowflake
    """ID of the message."""

    channel_id: Snowflake
    """ID of the channel the message was sent in."""

    author: UserOutput
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

    mentions: list[UserOutput]
    """Users specifically mentioned in the message."""

    mention_roles: list[Snowflake]
    """Roles specifically mentioned in this message."""

    mention_channels: list[ChannelMentionOutput] | None = None
    """Channels specifically mentioned in this message."""

    attachments: list[AttachmentOutput]
    """Any attached files."""

    embeds: list[EmbedOutput]
    """Any embedded content."""

    reactions: list[ReactionOutput] | None = None
    """Any reactions to the message."""

    nonce: int | str | None = None
    """Used for validating a message was sent."""

    pinned: bool
    """Whether this message is pinned."""

    webhook_id: Snowflake | None = None
    """If the message is generated by a webhook, this is the webhook's id."""

    type: MessageType
    """Type of message."""

    activity: MessageActivity | None = None
    """Sent with Rich Presence-related chat embeds."""

    application: MessageApplicationOutput | None = None
    """Sent with Rich Presence-related chat embeds."""

    application_id: Snowflake | None = None
    """If the message is an Interaction or application-owned webhook.

    This is the id of the application.
    """

    message_reference: MessageReferenceOutput | None = None
    """Reference data sent with crossposted messages."""

    flags: MessageFlags
    """Message flags combined as a bitfield."""

    referenced_message: MessageOutput | None = None
    """The message this message references, if the message is a reply."""

    interaction: MessageInteractionOutput | None = None
    """Sent if the message is a response to an Interaction."""

    thread: ChannelOutput | None = None
    """The thread that was started from this message, includes thread member object."""

    components: list[ComponentOutput] | None = None
    """Sent if the message is a response to an Interaction."""

    sticker_items: list[MessageStickerItemOutput] | None = None
    """Sent if the message contains stickers"""

    position: int | None = None
    """Generally increasing integer (there may be gaps or duplicates)
     
    Represents the approximate position of the message in a thread,
    it can be used to estimate the relative position of the message in a thread
    in company with total_message_sent on parent thread
    """

    role_subscription_data: RoleSubscriptionDataOutput | None = None
    """Data of the role subscription purchase or renewal.
    
    That prompted this ROLE_SUBSCRIPTION_PURCHASE message.
    """

    resolved: ResolvedDataOutput | None = None
    """Data for users, members, channels, and roles.
     
    In the message's auto-populated select menus.
    """
