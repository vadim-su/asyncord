from __future__ import annotations

import datetime

from pydantic import BaseModel

from asyncord.client.channels.models.responses import ChannelResponse
from asyncord.client.members.models.responses import MemberResponse
from asyncord.client.messages.models.common import MessageFlags, MessageType
from asyncord.client.messages.models.responses.components import ComponentOut
from asyncord.client.messages.models.responses.embeds import EmbedOut
from asyncord.client.messages.models.responses.messages import (
    AttachmentOut,
    ChannelMentionOut,
    MessageActivityOut,
    MessageApplicationOut,
    MessageInteractionOut,
    MessageReferenceOut,
    MessageResponse,
    ReactionOut,
)
from asyncord.client.models.stickers import Sticker
from asyncord.client.users.models.responses import UserResponse
from asyncord.gateway.events.base import GatewayEvent
from asyncord.snowflake import Snowflake


class MessageMember(BaseModel):
    """Mentioned user object."""

    nick: str | None = None
    """User's guild nickname."""

    avatar: str | None = None
    """Member's guild avatar hash."""

    roles: list[Snowflake]
    """Array of snowflakes."""

    joined_at: datetime.datetime
    """When the user joined the guild."""

    premium_since: datetime.datetime | None = None
    """When the user started boosting the guild."""

    deaf: bool
    """Whether the user is deafened in voice channels."""

    mute: bool
    """Whether the user is muted in voice channels."""

    pending: bool | None = None
    """Whether the user has not yet passed the guild's Membership Screening requirements."""

    communication_disabled_until: datetime.datetime | None = None
    """When the user's timeout will expire and the user will be able to communicate in the guild again.

    None or a time in the past if the user is not timed out.
    """


class MentionUser(BaseModel):
    id: Snowflake
    """The user's id."""

    username: str
    """User's username, not unique across the platform."""

    discriminator: str
    """User's 4 - digit discord-tag or 0 if the user has no tag."""

    avatar: str | None
    """User's avatar hash."""

    avatar_decoration: str | None = None
    """User's avatar decoration hash."""

    member: MessageMember | None = None
    """User's member properties in the guild."""


class MessageCreateEvent(GatewayEvent, MessageResponse):
    """Sent when a message is created.

    https://discord.com/developers/docs/topics/gateway-events#message-create
    """

    guild_id: Snowflake | None = None
    """Guild id the message was sent in.

    Unless it is an ephemeral message.
    """

    member: MessageMember | None = None
    """Member properties for this message's author.

    Only included when the message is in a guild."""

    mentions: list[MentionUser]
    """Users specifically mentioned in the message."""


class MessageUpdateEvent(GatewayEvent):
    """Sent when a message is updated.

    https://discord.com/developers/docs/topics/gateway-events#message-update.
    """

    id: Snowflake
    """Message id."""

    channel_id: Snowflake
    """Channel id the message was sent in."""

    author: UserResponse | None = None
    """Author of the message."""

    content: str | None = None
    """Contents of the message."""

    timestamp: datetime.datetime | None = None
    """When this message was sent."""

    edited_timestamp: datetime.datetime | None = None
    """When this message was edited.

    None if never.
    """

    tts: bool | None = None
    """Whether this was a TTS message."""

    mention_everyone: bool | None = None
    """Whether this message mentions everyone."""

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
    """Webhook id.

    Not none if the message is generated by a webhook.
    """

    type: MessageType | None = None
    """Type of message."""

    activity: MessageActivityOut | None = None
    """Sent with Rich Presence-related chat embeds."""

    application: MessageApplicationOut | None = None
    """Sent with Rich Presence-related chat embeds."""

    application_id: Snowflake | None = None
    """Application id.

    If the message is an Interaction or application-owned webhook.
    """

    message_reference: MessageReferenceOut | None = None
    """Reference data sent with crossposted messages."""

    flags: MessageFlags | None = None
    """Message flags combined as a bitfield."""

    stickers: list[Sticker] | None = None
    """Message stickers."""

    referenced_message: MessageResponse | None = None
    """The message this message references, if the message is a reply."""

    thread: ChannelResponse | None = None
    """The thread that was started from this message, includes thread member object."""

    components: list[ComponentOut] | None = None
    """Sent if the message is a response to an Interaction."""

    interaction: MessageInteractionOut | None = None
    """Sent if the message is a response to an Interaction."""

    message: str | None = None
    """Error message."""

    guild_id: Snowflake | None = None
    """Guild id the message was sent in - unless it is an ephemeral message."""

    member: MessageMember | None = None
    """Member properties for this message's author - only included when the message is in a guild."""

    mentions: list[MentionUser] | None = None
    """Users specifically mentioned in the message."""


class MessageDeleteEvent(GatewayEvent):
    """Sent when a message is deleted.

    https://discord.com/developers/docs/topics/gateway-events#message-delete
    """

    id: Snowflake
    """Message id."""

    channel_id: Snowflake
    """Channel id the message was sent in."""

    guild_id: Snowflake | None = None
    """Guild id."""


class MessageDeleteBulkEvent(GatewayEvent):
    """Sent when multiple messages are deleted at once.

    https://discord.com/developers/docs/topics/gateway-events#message-delete-bulk
    """

    ids: list[Snowflake]
    """Ids of the messages."""

    channel_id: Snowflake
    """Id of the channel."""

    guild_id: Snowflake | None = None
    """Guild id."""


class MessageReactionEmoji(BaseModel):
    """https://discord.com/developers/docs/topics/gateway-events#message-reaction-add-message-reaction-add-event-fields."""

    name: str
    """Name of the emoji."""

    id: Snowflake | None = None
    """Id of the emoji."""

    animated: bool | None = None
    """Whether this emoji is animated."""


class MessageReactionAddEvent(GatewayEvent):
    """Sent when a user adds a reaction to a message.

    https://discord.com/developers/docs/topics/gateway-events#message-reaction-add
    """

    user_id: Snowflake
    """Id of the user."""

    channel_id: Snowflake
    """Idd of the channel."""

    message_id: Snowflake
    """Id of the message."""

    guild_id: Snowflake | None = None
    """Guild id."""

    member: MemberResponse | None = None
    """<ember properties for this reaction's user.

    Included only when the message is in a guild.
    """

    emoji: MessageReactionEmoji
    """Emoji used to react."""


class MessageReactionRemoveEvent(GatewayEvent):
    """Sent when a user removes a reaction from a message.

    https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove
    """

    user_id: Snowflake
    """User id."""

    channel_id: Snowflake
    """Channel id."""

    message_id: Snowflake
    """Message id."""

    guild_id: Snowflake | None = None
    """Guild id."""

    emoji: MessageReactionEmoji
    """Emoji used to react."""


class MessageReactionRemoveAllEvent(GatewayEvent):
    """Sent when all reactions are explicitly removed from a message.

    https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove-all
    """

    channel_id: Snowflake
    """Channel id."""

    message_id: Snowflake
    """Message id."""

    guild_id: Snowflake | None = None
    """Guild id."""


class MessageReactionRemoveEmojiEvent(GatewayEvent):
    """Sent when all reactions for a given emoji are explicitly removed from a message.

    https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove-emoji
    """

    channel_id: Snowflake
    """Channel id."""

    guild_id: Snowflake | None = None
    """Guild id."""

    message_id: Snowflake
    """Message id."""

    emoji: MessageReactionEmoji
    """Emoji that was removed."""
