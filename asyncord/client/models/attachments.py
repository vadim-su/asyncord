"""Attachment models for the client."""

from __future__ import annotations

import enum
from collections.abc import Sequence
from io import BufferedReader, IOBase
from pathlib import Path
from typing import Annotated, Any

from pydantic import AnyHttpUrl, BaseModel, Field

from asyncord.client.http.client import make_payload_form
from asyncord.client.http.models import FormField, FormPayload
from asyncord.snowflake import SnowflakeInputType

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


def make_payload_with_attachments(
    json_payload: BaseModel | dict[str, Any],
    attachments: Sequence[Attachment] | None = None,
    exclude_unset: bool = True,
    exclude_none: bool = False,
) -> FormPayload | dict[str, Any]:
    """Prepare a payload with possible attachments.

    !!! WARNING
        `json_payload` will be converted from model **excluding unset fields**!
        It means that if you want to send a message with saved unset values,
        you should pass the message already dumped to json or set `exclude_unset` to False.
        Be creful!

    If attachments are present in the message model data, the attachments will be converted
    to form fields and the message model data will be converted to a json payload field.
    Otherwise, the message model data will be converted to a json payload - dict.

    Args:
        json_payload: Base message model or raw dict data which will be sent as json payload.
        attachments: List of attachments to be sent with the message.
        exclude_unset: Whether to exclude unset fields from the json payload. Defaults to True.
        exclude_none: Whether to exclude None fields from the json payload. Defaults to False.
    """
    if isinstance(json_payload, BaseModel):
        json_payload = json_payload.model_dump(
            mode='json',
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
        )
    if not attachments:  # type: ignore
        return json_payload

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
