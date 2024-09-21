"""Attachment models for the client."""

from __future__ import annotations

import enum
import logging
import mimetypes
from collections.abc import Sequence
from io import BufferedReader, IOBase
from pathlib import Path
from typing import Annotated, Any

import filetype
from pydantic import BaseModel, Field
from yarl import URL

from asyncord.client.http.client import make_payload_form
from asyncord.client.http.models import FormField, FormPayload
from asyncord.snowflake import SnowflakeInputType
from asyncord.yarl_url import HttpYarlUrl

__ALL__ = (
    'AttachmentContentType',
    'AttachmentFlags',
    'Attachment',
    'make_attachment_payload',
)

logger = logging.getLogger(__name__)


AttachmentContentType = bytes | bytearray | memoryview | BufferedReader | IOBase | Path
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

    url: HttpYarlUrl | None = None
    """Source URL of the file."""

    proxy_url: HttpYarlUrl | None = None
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

    def make_path(self) -> URL | None:
        """Get the file path URL.

        It is necessary to relate the file to the message in some cases.
        For instance, when sending a message with an image embed, the image URL must be 'attachment://filename'.

        If file name is present, it will return the 'attachment://filename' URL.
        Otherwise, it will return none.
        """
        if self.filename:
            return URL(f'attachment://{self.filename}')
        return None


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


def get_content_mime(attachment: Attachment) -> str | None:
    """Guess the content type of the attachment.

    Args:
        attachment: Attachment object.

    Returns:
        The guessed content type.
    """
    if attachment.content_type:
        return attachment.content_type

    if attachment.filename:
        mime_type = mimetypes.guess_type(attachment.filename)[0]
        if mime_type:
            return mime_type

    if isinstance(attachment.content, bytes | bytearray | str | Path):
        mime_type = filetype.guess_mime(attachment.content)
        if mime_type:
            return mime_type

    logger.warning(
        'Could not guess content type for attachment %s',
        attachment.id or attachment.filename,
    )
    return None


def get_content_extension(attachment: Attachment) -> str | None:
    """Get the extension of the content type.

    Args:
        attachment: Attachment object.

    Returns:
        The extension of the content type.
    """
    if attachment.content_type:
        extension = mimetypes.guess_extension(attachment.content_type)
        if extension:
            return extension

    if isinstance(attachment.content, bytes | bytearray | str | Path):
        extension = filetype.guess_extension(attachment.content)
        if extension:
            return extension

    logger.warning('Could not guess extension for content type %s', attachment.id or attachment.filename)
    return None


def get_content_type(attachment: Attachment) -> tuple[str, str] | None:
    """Guess the content type of the attachment.

    Args:
        attachment: Attachment object.

    Returns:
        The guessed content type.
    """
    if attachment.content_type:
        extension = mimetypes.guess_extension(attachment.content_type)
        if extension:
            return attachment.content_type, extension

    if attachment.content:
        kind = filetype.guess(attachment.content)
        if kind:
            return kind.mime, kind.extension

    logger.warning(
        'Could not guess content type for attachment %s',
        attachment.id or attachment.filename,
    )
    return None
