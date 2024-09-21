"""This module contains models for thread requests."""

from collections.abc import Sequence
from typing import Annotated, Literal

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from asyncord.client.channels.models.common import MAX_RATELIMIT
from asyncord.client.messages.models.common import MessageFlags
from asyncord.client.messages.models.requests.base_message import BaseMessage, ListAttachmentType, SingleAttachmentType
from asyncord.client.messages.models.requests.components import MessageComponentType
from asyncord.client.messages.models.requests.embeds import Embed
from asyncord.client.messages.models.requests.messages import AllowedMentions
from asyncord.client.threads.models.common import ThreadType
from asyncord.snowflake import SnowflakeInputType

__all__ = (
    'CreateMediaForumThreadRequest',
    'CreateThreadFromMessageRequest',
    'CreateThreadRequest',
    'ThreadMessage',
    'UpdateThreadRequest',
)


class CreateThreadRequest(BaseModel):
    """Request model for creating a thread."""

    name: str = Field(min_length=1, max_length=100)
    """Thread name."""

    auto_archive_duration: Literal[60, 1440, 4320, 10080] | None = None
    """Duration in minutes to automatically archive the thread after recent activity."""

    type: ThreadType
    """Type of thread."""

    invitable: bool | None = None
    """Whether non-moderators can add other non-moderators to a thread.

    Only available when creating a private thread.
    """

    rate_limit_per_user: Annotated[int, Field(ge=0, le=MAX_RATELIMIT)] | None = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    @field_validator('invitable')
    @classmethod
    def validate_invitable(cls, invitable: bool | None, field_info: ValidationInfo) -> bool | None:
        """Validate invitable field."""
        if field_info.data['type'] is not ThreadType.GUILD_PRIVATE_THREAD:
            raise ValueError('invitable is only available when creating a private thread.')
        return invitable


class CreateThreadFromMessageRequest(BaseModel):
    """Request model for creating a thread from a message."""

    name: str = Field(min_length=1, max_length=100)
    """Thread name."""

    auto_archive_duration: Literal[60, 1440, 4320, 10080] | None = None
    """Duration in minutes to automatically archive the thread after recent activity."""

    rate_limit_per_user: Annotated[int, Field(ge=0, le=MAX_RATELIMIT)] | None = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """


class ThreadMessage(BaseMessage):
    """Message model for a media/forum thread."""

    content: Annotated[str | None, Field(max_length=2000)] = None
    """Message content."""

    embeds: Annotated[Embed | list[Embed], list[Embed], Field(max_length=10)] | None = None
    """Embedded rich content."""

    allowed_mentions: AllowedMentions | None = None
    """Allowed mentions for the message."""

    components: Sequence[MessageComponentType] | MessageComponentType | None = None
    """Components to include with the message."""

    sticker_ids: list[SnowflakeInputType] | None = None
    """Sticker ids to include with the message."""

    attachments: Annotated[
        ListAttachmentType | SingleAttachmentType | None,
        Field(validate_default=True),  # Necessary for the embedded attachment collection
    ] = None
    """List of attachment object.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS, MessageFlags.SUPPRESS_NOTIFICATIONS] | None = None
    """The flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """


class CreateMediaForumThreadRequest(BaseModel):
    """Request model for creating a media/forum thread."""

    name: str = Field(min_length=1, max_length=100)
    """Thread name."""

    auto_archive_duration: Literal[60, 1440, 4320, 10080] | None = None
    """Duration in minutes to automatically archive the thread after recent activity."""

    rate_limit_per_user: Annotated[int, Field(ge=0, le=MAX_RATELIMIT)] | None = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    message: ThreadMessage
    """Message to send when creating the thread."""

    applied_tags: list[SnowflakeInputType] | None = None
    """Set of tag ids that have been applied to a thread."""


class UpdateThreadRequest(BaseModel):
    """Request model for updating a thread."""

    name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    """Thread name."""

    archived: bool | None = None
    """Whether the thread is archived."""

    locked: bool | None = None
    """Whether the thread is locked."""

    invitable: bool | None = None
    """Whether non-moderators can add other non-moderators to a thread.

    Only available when updating a private thread.
    """

    auto_archive_duration: Literal[60, 1440, 4320, 10080] | None = None
    """Duration in minutes to automatically archive the thread after recent activity."""

    rate_limit_per_user: Annotated[int, Field(ge=0, le=MAX_RATELIMIT)] | None = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """
