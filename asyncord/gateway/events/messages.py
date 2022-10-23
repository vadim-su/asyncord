from __future__ import annotations

import typing
import datetime

from pydantic import Field, BaseModel

from asyncord.snowflake import Snowflake
from asyncord.client.models.members import Member
from asyncord.client.models.messages import Message
from asyncord.gateway.events.base import GatewayEvent


class MessageCreateEvent(GatewayEvent, Message):
    """https://discord.com/developers/docs/topics/gateway#message-create"""

    guild_id: Snowflake | None = None
    """	id of the guild the message was sent in - unless it is an ephemeral message"""

    member: MessageMember | None = None
    """	member properties for this message's author - only included when the message is in a guild"""

    mentions: list[MessageUser]
    """	users specifically mentioned in the message"""


class MessageUpdateEvent(GatewayEvent, Message):
    """https://discord.com/developers/docs/topics/gateway#message-update"""

    guild_id: Snowflake | None = None
    """	id of the guild the message was sent in - unless it is an ephemeral message"""

    member: MessageMember | None = None
    """	member properties for this message's author - only included when the message is in a guild"""

    mentions: list[MessageUser]
    """	users specifically mentioned in the message"""


class MessageDeleteEvent(GatewayEvent):
    """Sent when a message is deleted.

    https://discord.com/developers/docs/topics/gateway#message-delete
    """

    id: Snowflake
    """id of the message"""

    channel_id: Snowflake
    """the id of the channel"""

    guild_id: Snowflake | None = None
    """the id of the guild"""


class MessageDeleteBulkEvent(GatewayEvent):
    """Sent when multiple messages are deleted at once.

    https://discord.com/developers/docs/topics/gateway#message-delete-bulk
    """

    ids: list[Snowflake]
    """the ids of the messages"""

    channel_id: Snowflake
    """the id of the channel"""

    guild_id: Snowflake | None = None
    """the id of the guild"""


class MessageReactionAddEvent(GatewayEvent):
    """Sent when a user adds a reaction to a message.

    https://discord.com/developers/docs/topics/gateway#message-reaction-add
    """

    user_id: Snowflake
    """the id of the user"""

    channel_id: Snowflake
    """the id of the channel"""

    message_id: Snowflake
    """the id of the message"""

    guild_id: Snowflake | None = None
    """the id of the guild"""

    member: Member | None = None
    """member properties for this reaction's user - only included when the message is in a guild"""

    emoji: MessageReactionEmoji
    """the emoji used to react"""


class MessageReactionEmoji(BaseModel):
    """https://discord.com/developers/docs/topics/gateway#message-reaction-add-message-reaction-add-event-fields"""

    name: str
    """the name of the emoji"""

    id: Snowflake | None = None
    """the id of the emoji"""

    animated: bool | None = None
    """whether this emoji is animated"""


class MessageReactionRemoveEvent(GatewayEvent):
    """Sent when a user removes a reaction from a message.

    https://discord.com/developers/docs/topics/gateway#message-reaction-remove
    """

    user_id: Snowflake
    """the id of the user"""

    channel_id: Snowflake
    """the id of the channel"""

    message_id: Snowflake
    """the id of the message"""

    guild_id: Snowflake | None = None
    """the id of the guild"""

    emoji: MessageReactionEmoji
    """the emoji used to react"""


class MessageReactionRemoveAllEvent(GatewayEvent):
    """Sent when all reactions are explicitly removed from a message.

    https://discord.com/developers/docs/topics/gateway#message-reaction-remove-all
    """

    channel_id: Snowflake
    """the id of the channel"""

    message_id: Snowflake
    """the id of the message"""

    guild_id: Snowflake | None = None
    """the id of the guild"""


class MessageReactionRemoveEmojiEvent(GatewayEvent):
    """Sent when all reactions for a given emoji are explicitly removed from a message.

    https://discord.com/developers/docs/topics/gateway#message-reaction-remove-emoji
    """

    channel_id: Snowflake
    """the id of the channel"""

    guild_id: Snowflake | None = None
    """the id of the guild"""

    message_id: Snowflake
    """the id of the message"""

    emoji: MessageReactionEmoji
    """the emoji that was removed"""


class MessageMember(BaseModel):
    nick: str | None = None
    """this user's guild nickname"""

    avatar: str | None = None
    """the member's guild avatar hash"""

    roles: list[Snowflake]
    """array of snowflakes"""

    joined_at: datetime.datetime
    """when the user joined the guild"""

    premium_since: datetime.datetime | None = None
    """when the user started boosting the guild"""

    deaf: bool
    """whether the user is deafened in voice channels"""

    mute: bool
    """whether the user is muted in voice channels"""

    pending: bool | None = None
    """whether the user has not yet passed the guild's Membership Screening requirements"""

    communication_disabled_until: datetime.datetime | None = None
    """when the user's timeout will expire and the user will be able to communicate in the guild again.

    None or a time in the past if the user is not timed out.
    """


class MessageUser(BaseModel):
    id: Snowflake
    """The user's id."""

    username: str
    """The user's username, not unique across the platform."""

    discriminator: typing.Annotated[str, Field(min_len=4, max_len=4)]
    """The user's 4 - digit discord-tag."""

    avatar: str
    """The user's avatar hash."""

    avatar_decoration: str | None = None
    """The user's avatar decoration hash."""

    member: MessageMember
    """The user's member properties in the guild."""


MessageCreateEvent.update_forward_refs()
MessageUpdateEvent.update_forward_refs()
