"""Models for webhook requests."""

from collections.abc import Sequence
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from asyncord.base64_image import Base64ImageInputType
from asyncord.client.messages.models.common import AllowedMentionType, MessageFlags
from asyncord.client.messages.models.requests.base_message import BaseMessage, ListAttachmentType, SingleAttachmentType
from asyncord.client.messages.models.requests.components import MessageComponentType
from asyncord.client.messages.models.requests.embeds import Embed
from asyncord.client.polls.models.requests import Poll
from asyncord.snowflake import SnowflakeInputType

__ALL__ = (
    'CreateWebhookRequest',
    'ExecuteWebhookRequest',
    'UpdateWebhookMessageRequest',
    'UpdateWebhookRequest',
)


class CreateWebhookRequest(BaseModel):
    """Model for creating a webhook.

    Reference:
    https://discord.com/developers/docs/resources/webhook#create-webhook-json-params
    """

    name: str = Field(min_length=1, max_length=80)
    """Name of the webhook."""

    avatar: Base64ImageInputType | None = None
    """Image for the default webhook avatar."""


class UpdateWebhookRequest(BaseModel):
    """Model for updating a webhook.

    Reference:
    https://discord.com/developers/docs/resources/webhook#modify-webhook-json-params
    """

    name: str = Field(min_length=1, max_length=80)
    """Default name of the webhook."""

    avatar: Base64ImageInputType | None = None
    """Image for the default webhook avatar."""

    channel_id: SnowflakeInputType | None = None
    """New channel id this webhook should be moved to.

    This field is only availabe when modifying without token.
    """


class ExecuteWebhookRequest(BaseMessage):
    """Model for executing webhook request.

    Reference:
    https://discord.com/developers/docs/resources/webhook#execute-webhook-jsonform-params
    """

    content: Annotated[str | None, Field(max_length=2000)] = None
    """The message contents (up to 2000 characters)."""

    username: str | None = None
    """Override the default username of the webhook."""

    avatar_url: str | None = None
    """Override the default avatar of the webhook."""

    tts: bool | None = None
    """True if this is a TTS message."""

    embeds: Annotated[Embed | list[Embed], list[Embed], Field(max_length=10)] | None = None
    """Embedded rich content."""

    allowed_mentions: AllowedMentionType | None = None
    """Allowed mentions for the message."""

    components: MessageComponentType | Sequence[MessageComponentType] | None = None
    """The components to include with the message."""

    attachments: Annotated[
        ListAttachmentType | SingleAttachmentType | None,
        Field(validate_default=True),  # Necessary for the embedded attachment collection
    ] = None
    """List of attachment object.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """

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

    poll: Poll | None = None
    """A poll."""


class UpdateWebhookMessageRequest(BaseMessage):
    """Model for updating a webhook message.

    Reference:
    https://discord.com/developers/docs/resources/webhook#edit-webhook-message-jsonform-params
    """

    content: Annotated[str | None, Field(max_length=2000)] = None
    """The message contents (up to 2000 characters)."""

    embeds: Annotated[Embed | list[Embed], list[Embed], Field(max_length=10)] | None = None
    """Embedded rich content."""

    allowed_mentions: AllowedMentionType | None = None
    """Allowed mentions for the message."""

    components: MessageComponentType | Sequence[MessageComponentType] | None = None
    """The components to include with the message."""

    attachments: Annotated[
        ListAttachmentType | SingleAttachmentType | None,
        Field(validate_default=True),  # Necessary for the embedded attachment collection
    ] = None
    """List of attachment object.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """
