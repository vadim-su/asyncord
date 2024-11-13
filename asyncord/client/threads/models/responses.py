"""This module contains models for thread responses."""

from __future__ import annotations

from pydantic import BaseModel

from asyncord.client.channels.models.responses import ThreadMemberResponse, ThreadMetadataOut, ThreadResponse

# We export ThreadResponse and ThreadMetadataOut from asyncord.client.channels.models.responses to save
# identical code style and expected behavior.
# We moved ThreadResponse to channels because in general, threads are a type of channel and it makes sense to
# keep them together to avoid circular imports.
__all__ = ('ThreadMetadataOut', 'ThreadResponse', 'ThreadsResponse')


class ThreadsResponse(BaseModel):
    """Guild active threads response object.

    Reference:
    https://discord.com/developers/docs/resources/guild#list-active-guild-threads-response-body
    """

    threads: list[ThreadResponse]
    """List of thread objects."""

    members: list[ThreadMemberResponse]
    """List of thread member objects."""

    has_more: bool | None = None
    """Whether there are potentially additional threads that could be returned on a subsequent call."""
