"""Attachment models for the client."""

from __future__ import annotations

import enum
from io import BufferedReader, IOBase
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, cast

from pydantic import AnyHttpUrl, BaseModel, Field

from asyncord.client.http.client import make_payload_form
from asyncord.client.http.models import FormField, FormPayload
from asyncord.snowflake import SnowflakeInputType

if TYPE_CHECKING:
    from asyncord.client.messages.models.requests.messages import BaseMessage


__ALL__ = (
    'AttachmentContentType',
    'AttachmentFlags',
    'Attachment',
    'make_attachment_payload',
)


type AttachmentContentType = bytes | bytearray | memoryview | BufferedReader | IOBase | Path
"""Attachment content type.

It can be raw data, a file-like object, or a path to a file.
"""


@enum.unique
class AttachmentFlags(enum.IntFlag):
    """Attachment flags.

    Reference:
    https://discord.com/developers/docs/resources/channel#attachment-object-attachment-flags
    """

    IS_REMIX = 1 << 2
    """This attachment has been edited using the remix feature on mobile."""


class Attachment(BaseModel, arbitrary_types_allowed=True):
    """Attachment object used for creating and editing messages.

    Reference:
    https://discord.com/developers/docs/resources/channel#attachment-object
    """

    id: int | SnowflakeInputType | None = None
    """Attachment ID."""

    filename: str | None = None
    """Name of the attached file."""

    description: Annotated[str | None, Field(max_length=1024)] = None
    """Description for the file.

    Max 1024 characters.
    """

    content_type: str | None = None
    """Media type of the file."""

    size: int | None = None
    """Size of the file in bytes."""

    url: AnyHttpUrl | None = None
    """Source URL of the file."""

    proxy_url: AnyHttpUrl | None = None
    """Proxied URL of the file."""

    height: int | None = None
    """Height of the file (if image)."""

    width: int | None = None
    """Width of the file (if image)."""

    ephemeral: bool | None = None
    """Whether this attachment is ephemeral.

    Ephemeral attachments will automatically be removed after a set period of time.
    Ephemeral attachments on messages are guaranteed to be available as long as
    the message itself exists.
    """

    duration_secs: float | None = None
    """Duration of the audio file (currently for voice messages)."""

    waveform: str | None = None
    """base64 encoded bytearray representing a sampled waveform.

    Currently for voice messages.
    """

    flags: AttachmentFlags | None = None
    """Attachment flags."""

    content: Annotated[AttachmentContentType | None, Field(exclude=True)] = None
    """Attachment content.

    This field is not part of the Discord API and will not be serialized.
    """

    do_not_attach: Annotated[bool, Field(exclude=True)] = False
    """Do not attach the file to the message.

    This field is not part of the Discord API and will not be serialized.

    If set to True, the file will not be attached as an image or video and will be sent as a raw file.
    You can use this to send files without embedding them.
    """


def make_attachment_payload(
    attachment_model_data: BaseMessage,
    root_payload: BaseModel | None = None,
) -> FormPayload | dict[str, Any]:
    """Convert an attachment to a form field.

    Args:
        attachment_model_data: Message model data with attachments.
        root_payload: Root payload model data which will be sent as json payload.
            It will replace the attachment content in the payload. But the attachment
            will still be sent as a form field.
    """
    payload_model_data = root_payload or attachment_model_data
    json_payload = payload_model_data.model_dump(mode='json', exclude_unset=True)
    if not attachment_model_data.attachments:  # type: ignore
        return json_payload

    # All base message models have attachments attribute.
    # We can safely cast it to a list of attachments.
    attachments = cast(list[Attachment], attachment_model_data.attachments)  # type: ignore

    file_form_fields = {
        f'files[{attachment.id}]': FormField(
            value=attachment.content,
            content_type=attachment.content_type,
            filename=attachment.filename,
        )
        for attachment in attachments
        if attachment.content is not None
    }
    return make_payload_form(json_payload=json_payload, **file_form_fields)
