"""This module contains resource classes for interacting with threads."""

from __future__ import annotations

from asyncord.client.channels.models.responses import ThreadMemberResponse
from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.messages.resources import MessageResource
from asyncord.client.resources import ClientResource, ClientSubresource
from asyncord.client.threads.models.requests import (
    CreateMediaForumThreadRequest,
    CreateThreadFromMessageRequest,
    CreateThreadRequest,
    UpdateThreadRequest,
)
from asyncord.client.threads.models.responses import ThreadResponse, ThreadsResponse
from asyncord.snowflake import SnowflakeInputType
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL


class ThreadResource(ClientSubresource):  # noqa: PLR0904
    """Resource to interact with threads.

    Attributes:
        channel_id: Channel id for the thread.
        channels_url: URL for the channels resource.
        guilds_url: URL for the guilds resource.
        threads_url: 'main' URL for the threads resource.
    """

    channels_url = REST_API_URL / 'channels'
    guilds_url = REST_API_URL / 'guilds'

    def __init__(self, parent: ClientResource, channel_id: SnowflakeInputType) -> None:
        """Initialize the thread resource."""
        super().__init__(parent)
        self.channel_id = channel_id
        self.threads_url = self.channels_url / str(channel_id) / 'threads'

    def messages(self, thread_id: SnowflakeInputType) -> MessageResource:
        """Get the messages resource for a thread.

        Args:
            thread_id: ID of the thread.

        Returns:
            Messages resource for the thread.
        """
        return MessageResource(self, thread_id)

    async def get(self, thread_id: SnowflakeInputType) -> ThreadResponse:
        """Get a thread."""
        url = self.channels_url / str(thread_id)
        resp = await self._http_client.get(url)
        return ThreadResponse.model_validate(resp.body)

    async def get_active_threads(self, guild_id: SnowflakeInputType) -> ThreadsResponse:
        """Get the active theads.

        Yeah, this endpoint is weird. We can only get the active threads for a guild,
        not a channel.

        Returns:
            Thread list resource for the channel.
        """
        url = self.guilds_url / str(guild_id) / 'threads' / 'active'
        resp = await self._http_client.get(url)
        return ThreadsResponse.model_validate(resp.body)

    async def get_archived_threads(
        self,
        private: bool = False,
        before: SnowflakeInputType | None = None,
        limit: int | None = None,
    ) -> ThreadsResponse:
        """Get the archived thread threads.

        Args:
            private: Whether to include private threads.
            before: Get threads before this id.
            limit: Maximum number of threads to return.

        Returns:
            Thread list resource for the channel.
        """
        params = {}
        if before is not None:
            params['before'] = before
        if limit is not None:
            params['limit'] = limit

        if private:
            url = self.threads_url / 'archived' / 'private' % params
        else:
            url = self.threads_url / 'archived' / 'public' % params
        resp = await self._http_client.get(url)

        return ThreadsResponse.model_validate(resp.body)

    async def get_joined_private_archive_threads(
        self,
        before: SnowflakeInputType | None = None,
        limit: int | None = None,
    ) -> ThreadsResponse:
        """Get the joined private archived thread resource for a channel.

        Returns:
            Thread list resource for the channel.
        """
        params = {}
        if before is not None:
            params['before'] = before
        if limit is not None:
            params['limit'] = limit

        url = self.channels_url / str(self.channel_id)
        url /= 'users/@me/threads/archived/private' % params

        resp = await self._http_client.get(url)
        return ThreadsResponse.model_validate(resp.body)

    async def create_thread_from_message(
        self,
        message_id: SnowflakeInputType,
        thread_data: CreateThreadFromMessageRequest,
        reason: str | None = None,
    ) -> ThreadResponse:
        """Create a thread from a message.

        Args:
            message_id: Message id.
            thread_data: Data to create the thread with.
            reason: Reason for creating the thread.
        """
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}
        url = self.channels_url / str(self.channel_id) / 'messages' / str(message_id) / 'threads'

        payload = thread_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.post(url, payload=payload, headers=headers)
        return ThreadResponse.model_validate(resp.body)

    async def create_thread(self, thread_data: CreateThreadRequest, reason: str | None = None) -> ThreadResponse:
        """Create a thread.

        Args:
            thread_data: Data to create the thread with.
            reason: Reason for creating the thread.
        """
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}
        url = self.threads_url

        payload = thread_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.post(url, payload=payload, headers=headers)
        return ThreadResponse.model_validate(resp.body)

    async def create_media_forum_thread(
        self,
        thread_data: CreateMediaForumThreadRequest,
        reason: str | None = None,
    ) -> ThreadResponse:
        """Create a media/forum thread.

        Args:
            thread_data: Data to create the thread with.
            reason: Reason for creating the thread.
        """
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = thread_data.model_dump(mode='json', exclude_unset=True)
        # fmt: off
        resp = await self._http_client.post(
            url=self.threads_url,
            payload=payload,
            files=[
                (file.filename, file.content_type, file.content)
                for file in thread_data.message.files
            ],
            headers=headers,
        )
        # fmt: on
        return ThreadResponse.model_validate(resp.body)

    async def delete(self, thread_id: SnowflakeInputType, reason: str | None = None) -> None:
        """Delete a thread.

        Args:
            thread_id: Thread id.
            reason: Reason for deleting the channel.
        """
        url = self.channels_url / str(thread_id)

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.delete(url, headers=headers)

    async def join_thread(self, thread_id: SnowflakeInputType) -> None:
        """Join a thread.

        Args:
            thread_id: Thread id.
        """
        url = self.channels_url / str(thread_id) / 'thread-members/@me'
        await self._http_client.put(url, payload=None)

    async def add_member(self, thread_id: SnowflakeInputType, user_id: SnowflakeInputType) -> None:
        """Add a member to a thread.

        Args:
            thread_id: Thread id.
            user_id: User id.
        """
        url = self.channels_url / str(thread_id) / 'thread-members' / str(user_id)
        await self._http_client.put(url, payload=None)

    async def leave_thread(self, thread_id: SnowflakeInputType) -> None:
        """Leave a thread.

        Args:
            thread_id: Thread id.
        """
        url = self.channels_url / str(thread_id) / 'thread-members/@me'
        await self._http_client.delete(url)

    async def remove_member(
        self,
        thread_id: SnowflakeInputType,
        user_id: SnowflakeInputType,
    ) -> None:
        """Remove a member from a thread.

        Args:
            thread_id: Thread id.
            user_id: User id.
        """
        url = self.channels_url / str(thread_id) / 'thread-members' / str(user_id)
        await self._http_client.delete(url)

    async def get_members(
        self,
        thread_id: SnowflakeInputType,
        after: SnowflakeInputType | None = None,
        limit: int | None = None,
    ) -> list[ThreadMemberResponse]:
        """Get the members of a thread.

        Args:
            thread_id: Thread id.
            after: Get members after this id.
            limit: Maximum number of members to return.
                Defaults to 100
        """
        params = {}
        if after is not None:
            params['after'] = after
        if limit is not None:
            params['limit'] = limit

        url = self.channels_url / str(thread_id) / 'thread-members'
        resp = await self._http_client.get(url)
        return list_model(ThreadMemberResponse).validate_python(resp.body)

    async def get_member(
        self,
        thread_id: SnowflakeInputType,
        user_id: SnowflakeInputType,
    ) -> ThreadMemberResponse:
        """Get a thread member.

        Args:
            thread_id: Thread id.
            user_id: User id.
        """
        # It probably default to true in v11 API
        params = {
            'with_member': str(True),
        }

        url = self.channels_url / str(thread_id) / 'thread-members' / str(user_id) % params
        resp = await self._http_client.get(url)
        return ThreadMemberResponse.model_validate(resp.body)

    async def lock(self, thread_id: SnowflakeInputType, reason: str | None = None) -> ThreadResponse:
        """Lock a thread.

        Args:
            thread_id: Thread id.
            reason: Reason for locking the thread.
        """
        return await self.update(
            thread_id=thread_id,
            thread_data=UpdateThreadRequest(locked=True),  # type: ignore
            reason=reason,
        )

    async def unlock(self, thread_id: SnowflakeInputType, reason: str | None = None) -> ThreadResponse:
        """Unlock a thread.

        Args:
            thread_id: Thread id.
            reason: Reason for unlocking the thread.
        """
        return await self.update(
            thread_id=thread_id,
            thread_data=UpdateThreadRequest(locked=False),  # type: ignore
            reason=reason,
        )

    async def archive(self, thread_id: SnowflakeInputType, reason: str | None = None) -> ThreadResponse:
        """Archive a thread.

        Args:
            thread_id: Thread id.
            reason: Reason for archiving the thread.
        """
        return await self.update(
            thread_id=thread_id,
            thread_data=UpdateThreadRequest(archived=True),  # type: ignore
            reason=reason,
        )

    async def unarchive(self, thread_id: SnowflakeInputType, reason: str | None = None) -> ThreadResponse:
        """Unarchive a thread.

        Args:
            thread_id: Thread id.
            reason: Reason for unarchiving the thread.
        """
        return await self.update(
            thread_id=thread_id,
            thread_data=UpdateThreadRequest(archived=False),  # type: ignore
            reason=reason,
        )

    async def update(
        self,
        thread_id: SnowflakeInputType,
        thread_data: UpdateThreadRequest,
        reason: str | None = None,
    ) -> ThreadResponse:
        """Update a thread.

        Args:
            thread_id: Thread id.
            thread_data: Data to update the thread with.
            reason: Reason for updating the thread.
        """
        url = self.channels_url / str(thread_id)

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = thread_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.patch(url, payload=payload, headers=headers)
        return ThreadResponse.model_validate(resp.body)