"""Models for webhook requests."""

from typing import Any, Literal, Self

from pydantic import BaseModel, Field, model_validator

from asyncord.base64_image import Base64ImageInputType
from asyncord.client.messages.models.common import AllowedMentionType, MessageFlags
from asyncord.client.messages.models.requests.components import (
    Component,
)
from asyncord.client.messages.models.requests.embeds import Embed
from asyncord.client.messages.models.requests.messages import AttachedFile
from asyncord.snowflake import SnowflakeInputType


class CreateWebhookRequest(BaseModel):
    """Model for creating a webhook.

    Reference:
    https://discord.com/developers/docs/resources/webhook#create-webhook-json-params
    """

    name: str = Field(None, min_length=1, max_length=80)
    """Name of the webhook."""

    avatar: Base64ImageInputType | None = None
    """Image for the default webhook avatar."""


class UpdateWebhookRequest(BaseModel):
    """Model for updating a webhook.

    Reference:
    https://discord.com/developers/docs/resources/webhook#modify-webhook-json-params
    """

    name: str
    """Default name of the webhook."""

    avatar: Base64ImageInputType | None = None
    """Image for the default webhook avatar."""

    channel_id: SnowflakeInputType | None = None
    """New channel id this webhook should be moved to.

    This field is only availabe when modifying without token.
    """


class ExecuteWebhookRequest(BaseModel):
    """Model for executing webhook request.

    Reference:
    https://discord.com/developers/docs/resources/webhook#execute-webhook-jsonform-params
    """

    content: str | None = Field(None, max_length=2000)
    """The message contents (up to 2000 characters)."""

    username: str | None = None
    """Override the default username of the webhook."""

    avatar_url: str | None = None
    """Override the default avatar of the webhook."""

    tts: bool | None = None
    """True if this is a TTS message."""

    embeds: list[Embed] | None = Field(None, max_length=10)
    """Embedded rich content."""

    allowed_mentions: AllowedMentionType | None = None
    """Allowed mentions for the message."""

    components: list[Component] | None = None
    """The components to include with the message."""

    files: list[AttachedFile] = Field(default_factory=list, exclude=True)
    """The contents of the file being sent."""

    # FIXME: Partial attachment objects. No reference found.
    attachments: list[dict[str, Any]] | None = None
    """Attachment objects with filename and description."""

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS, MessageFlags.SUPPRESS_NOTIFICATIONS] | None = None
    """Message flags combined as a bitfield.

    (only SUPPRESS_EMBEDS and SUPPRESS_NOTIFICATIONS can be set).
    """

    thread_name: str | None = None
    """Name of thread to create.

    (requires the webhook channel to be a forum or media channel).
    """

    applied_tags: list[SnowflakeInputType] | None = None
    """Array of tag ids to apply to the thread.

    (requires the webhook channel to be a forum or media channel).
    """

    # FIXME: Add poll request model when it gets added.
    poll: dict[str, Any] | None = None
    """A poll."""

    @model_validator(mode='after')
    def validate_required(self) -> Self:
        """At least one of content, file, embeds, poll must be present."""
        if not any([self.content, self.files, self.embeds, self.poll]):
            raise ValueError(
                'At least one of content, file, embeds, poll must be present.',
            )

        return self


class UpdateWebhookMessageRequest(BaseModel):
    """Model for updating a webhook message.

    Reference:
    https://discord.com/developers/docs/resources/webhook#edit-webhook-message-jsonform-params
    """

    content: str | None = Field(None, max_length=2000)
    """The message contents (up to 2000 characters)."""

    embeds: list[Embed] | None = Field(None, max_length=10)
    """Embedded rich content."""

    allowed_mentions: AllowedMentionType | None = None
    """Allowed mentions for the message."""

    components: list[Component] | None = None
    """The components to include with the message."""

    files: list[AttachedFile] = Field(default_factory=list, exclude=True)
    """The contents of the file being sent."""

    # FIXME: Partial attachment objects. No reference found.
    attachments: list[dict[str, Any]] | None = None
    """Attachment objects with filename and description."""
