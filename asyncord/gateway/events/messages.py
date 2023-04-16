from __future__ import annotations

import typing
import datetime

from pydantic import Field, BaseModel

from asyncord.snowflake import Snowflake
from asyncord.client.models import messages
from asyncord.client.models.users import User
from asyncord.gateway.events.base import GatewayEvent
from asyncord.client.models.members import Member
from asyncord.client.models.channels import Channel
from asyncord.client.models.stickers import Sticker
from asyncord.client.models.components import Component


class MessageCreateEvent(GatewayEvent, messages.Message):
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

    mentions: list[MessageUser]
    """Users specifically mentioned in the message."""


class MessageUpdateEvent(GatewayEvent):
    """Sent when a message is updated.

    https://discord.com/developers/docs/topics/gateway-events#message-update.
    """

    id: Snowflake
    """Message id."""

    channel_id: Snowflake
    """Channel id the message was sent in."""

    author: User | None = None
    """Author of the message."""

    content: str | None = None  # noqa WPS110 # Found wrong variable name
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

    mention_channels: list[messages.ChannelMention] | None = None
    """Channels specifically mentioned in this message."""

    attachments: list[messages.Attachment] | None = None
    """Any attached files."""

    embeds: list[messages.Embed] | None = None
    """Any embedded content."""

    reactions: list[messages.Reaction] | None = None
    """Any reactions to the message."""

    nonce: int | str | None = None
    """Used for validating a message was sent."""

    pinned: bool | None = None
    """Whether this message is pinned."""

    webhook_id: Snowflake | None = None
    """Webhook id.

    Not none if the message is generated by a webhook.
    """

    type: messages.MessageType | None = None
    """Type of message."""

    activity: messages.MessageActivity | None = None
    """Sent with Rich Presence-related chat embeds."""

    application: messages.MessageApplication | None = None
    """Sent with Rich Presence-related chat embeds."""

    application_id: Snowflake | None = None
    """Application id.

    If the message is an Interaction or application-owned webhook.
    """

    message_reference: messages.MessageReference | None = None
    """Reference data sent with crossposted messages."""

    flags: messages.MessageFlags | None = None
    """Message flags combined as a bitfield."""

    stickers: list[Sticker] | None = None
    """Message stickers."""

    referenced_message: messages.Message | None = None
    """The message this message references, if the message is a reply."""

    thread: Channel | None = None
    """The thread that was started from this message, includes thread member object."""

    components: list[Component] | None = None
    """Sent if the message is a response to an Interaction."""

    interaction: messages.MessageInteraction | None = None
    """Sent if the message is a response to an Interaction."""

    message: str | None = None
    """Error message."""

    guild_id: Snowflake | None = None
    """Guild id the message was sent in - unless it is an ephemeral message."""

    member: MessageMember | None = None
    """Member properties for this message's author - only included when the message is in a guild."""

    mentions: list[MessageUser] | None = None
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

    member: Member | None = None
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


class MessageMember(BaseModel):
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


class MessageUser(BaseModel):
    id: Snowflake
    """The user's id."""

    username: str
    """User's username, not unique across the platform."""

    discriminator: typing.Annotated[str, Field(min_len=4, max_len=4)]
    """User's 4 - digit discord-tag."""

    avatar: str | None
    """User's avatar hash."""

    avatar_decoration: str | None = None
    """User's avatar decoration hash."""

    member: MessageMember
    """User's member properties in the guild."""


MessageCreateEvent.update_forward_refs()
MessageUpdateEvent.update_forward_refs()
