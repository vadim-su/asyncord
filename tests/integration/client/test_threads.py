from pathlib import Path

import pytest

from asyncord.client.channels.models.requests.creation import CreateForumChannelRequest, Tag
from asyncord.client.channels.models.requests.updating import UpdateChannelRequest
from asyncord.client.channels.resources import ChannelResource
from asyncord.client.http import errors
from asyncord.client.messages.models.requests.messages import CreateMessageRequest
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.threads.models.common import ThreadType
from asyncord.client.threads.models.requests import (
    CreateMediaForumThreadRequest,
    CreateThreadFromMessageRequest,
    CreateThreadRequest,
    ThreadMessage,
    UpdateThreadRequest,
)
from asyncord.client.threads.models.responses import ThreadResponse, ThreadsResponse
from asyncord.client.threads.resources import ThreadResource
from tests.conftest import IntegrationTestData

TEST_FILE_NAMES = ['test_image_1.png', 'test_image_2.png']


async def test_get_thread(
    thread_res: ThreadResource,
    thread: ThreadResponse,
) -> None:
    """Test getting a thread."""
    thread = await thread_res.get(thread_id=thread.id)
    assert isinstance(thread, ThreadResponse)


async def test_get_archived_threads(thread_res: ThreadResource) -> None:
    """Test getting archived threads."""
    archived_threads = await thread_res.get_archived_threads()
    assert isinstance(archived_threads, ThreadsResponse)
    assert archived_threads.threads
    assert archived_threads.threads[0].thread_metadata.archived


async def test_get_private_archived_threads(thread_res: ThreadResource) -> None:
    """Test getting private archived threads."""
    archived_threads = await thread_res.get_archived_threads(private=True)
    assert isinstance(archived_threads, ThreadsResponse)
    assert archived_threads.threads
    assert archived_threads.threads[0].thread_metadata.archived


async def test_get_joined_private_archived_threads(thread_res: ThreadResource) -> None:
    """Test getting joined private archived threads."""
    archived_threads = await thread_res.get_joined_private_archive_threads()
    assert isinstance(archived_threads, ThreadsResponse)


@pytest.mark.parametrize(
    'thread_type',
    [
        ThreadType.GUILD_PUBLIC_THREAD,
        ThreadType.GUILD_PRIVATE_THREAD,
    ],
)
async def test_create_delete_thread(
    thread_res: ThreadResource,
    thread_type: ThreadType,
) -> None:
    """Test creating and deleting a thread."""
    thread = await thread_res.create_thread(
        thread_data=CreateThreadRequest(
            name='test',
            type=thread_type,
        ),
    )

    assert isinstance(thread, ThreadResponse)
    assert thread.name == 'test'
    assert thread.type is thread_type
    assert thread.thread_metadata.archived is False

    await thread_res.delete(thread_id=thread.id)


async def test_create_delete_thread_from_message(
    thread_res: ThreadResource,
    message: MessageResponse,
) -> None:
    """Test creating and deleting a thread from a message."""
    thread = await thread_res.create_thread_from_message(
        message_id=message.id,
        thread_data=CreateThreadFromMessageRequest(
            name='test',
        ),
    )

    assert isinstance(thread, ThreadResponse)
    assert thread.name == 'test'
    assert thread.type is ThreadType.GUILD_PUBLIC_THREAD
    assert thread.thread_metadata.archived is False

    await thread_res.delete(thread_id=thread.id)


async def test_leave_rejoin_and_members_thread(thread_res: ThreadResource, thread: ThreadResponse) -> None:
    """Test leaving and rejoining a thread."""
    members = await thread_res.get_members(thread_id=thread.id)
    assert len(members) == thread.member_count

    await thread_res.leave_thread(thread_id=thread.id)

    members = await thread_res.get_members(thread_id=thread.id)
    assert len(members) < thread.member_count

    await thread_res.join_thread(thread_id=thread.id)

    members = await thread_res.get_members(thread_id=thread.id)
    assert len(members) == thread.member_count


async def test_remove_add_and_get_thread_member(thread_res: ThreadResource, thread: ThreadResponse) -> None:
    """Test removing and adding a thread member."""
    member = await thread_res.get_member(
        thread_id=thread.id,
        user_id=thread.owner_id,
    )
    assert member

    await thread_res.remove_member(thread_id=thread.id, user_id=thread.owner_id)

    with pytest.raises(errors.NotFoundError):
        await thread_res.get_member(
            thread_id=thread.id,
            user_id=thread.owner_id,
        )

    await thread_res.add_member(thread_id=thread.id, user_id=thread.owner_id)

    member = await thread_res.get_member(
        thread_id=thread.id,
        user_id=thread.owner_id,
    )
    assert member


@pytest.mark.parametrize('with_files', [True, False])
async def test_post_to_forum_channel(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
    with_files: bool,
) -> None:
    """Test posting to a forum channel."""
    channel = await channel_res.create_channel(
        guild_id=integration_data.guild_id,
        channel_data=CreateForumChannelRequest(
            name='test',
            available_tags=[Tag(name='test', emoji_name='👍')],
        ),
    )

    assert channel.available_tags

    tag_id = channel.available_tags[0].id

    thread_res = channel_res.threads(channel_id=channel.id)
    if with_files:
        files = [Path(f'tests/data/{file_name}') for file_name in TEST_FILE_NAMES]
    else:
        files = []

    try:
        thread = await thread_res.create_media_forum_thread(
            thread_data=CreateMediaForumThreadRequest(
                name='test thread',
                applied_tags=[tag_id],
                message=ThreadMessage(
                    content='test message',
                    attachments=files,
                ),
            ),
        )

    finally:
        await channel_res.delete(channel_id=channel.id)

    assert isinstance(thread, ThreadResponse)
    assert thread.name == 'test thread'
    assert thread.type is ThreadType.GUILD_PUBLIC_THREAD
    assert not thread.thread_metadata.archived
    assert thread.applied_tags
    assert len(thread.applied_tags) == 1
    assert thread.applied_tags[0] == tag_id


async def test_add_tag_to_forum(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test adding a tag to a thread."""
    channel = await channel_res.create_channel(
        guild_id=integration_data.guild_id,
        channel_data=CreateForumChannelRequest(
            name='test',
            available_tags=[],
        ),
    )

    assert not channel.available_tags

    channel = await channel_res.update(
        channel_id=channel.id,
        channel_data=UpdateChannelRequest(
            available_tags=[Tag(name='test')],
        ),
    )

    assert channel.available_tags
    assert len(channel.available_tags) == 1


async def test_add_tag_to_thread(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test adding a tag to a thread."""
    channel = await channel_res.create_channel(
        guild_id=integration_data.guild_id,
        channel_data=CreateForumChannelRequest(
            name='test',
            available_tags=[Tag(name='test')],
        ),
    )

    assert channel.available_tags
    tag_id = channel.available_tags[0].id
    thread_res = channel_res.threads(channel_id=channel.id)

    try:
        thread = await thread_res.create_media_forum_thread(
            thread_data=CreateMediaForumThreadRequest(
                name='test thread',
                message=ThreadMessage(
                    content='test message',
                ),
            ),
        )
        assert not thread.applied_tags

        # Threads are channels, so we should use the channel resource to update the thread.
        await channel_res.update(
            channel_id=thread.id,
            channel_data=UpdateChannelRequest(
                applied_tags=[tag_id],
            ),
        )

        thread = await thread_res.get(thread_id=thread.id)

        assert thread.applied_tags
        assert len(thread.applied_tags) == 1
    finally:
        await channel_res.delete(channel_id=channel.id)


async def test_archive_unarchive_thread(
    thread_res: ThreadResource,
    thread: ThreadResponse,
) -> None:
    """Test archiving and unarchiving a thread."""
    assert not thread.thread_metadata.archived

    thread = await thread_res.archive(thread_id=thread.id)
    assert thread.thread_metadata.archived

    thread = await thread_res.unarchive(thread_id=thread.id)
    assert not thread.thread_metadata.archived


async def test_lock_unlock_thread(thread_res: ThreadResource, thread: ThreadResponse) -> None:
    """Test locking and unlocking a thread."""
    assert not thread.thread_metadata.locked

    thread = await thread_res.lock(thread_id=thread.id)
    assert thread.thread_metadata.locked

    thread = await thread_res.unlock(thread_id=thread.id)
    assert not thread.thread_metadata.locked


async def test_update_thread(thread_res: ThreadResource, thread: ThreadResponse) -> None:
    """Test updating a thread."""
    thread = await thread_res.update(
        thread_id=thread.id,
        thread_data=UpdateThreadRequest(
            name='updated',
            archived=True,
            locked=True,
        ),
    )

    assert thread.name == 'updated'
    assert thread.thread_metadata.archived
    assert thread.thread_metadata.locked


async def test_send_message(thread_res: ThreadResource, thread: ThreadResponse) -> None:
    """Test sending a message to a thread."""
    message_res = thread_res.messages(thread_id=thread.id)
    message = await message_res.create(
        message_data=CreateMessageRequest(
            content='test',
        ),
    )

    assert isinstance(message, MessageResponse)
    assert message.content == 'test'
    assert message.channel_id == thread.id

    updated_thread = await thread_res.get(thread_id=thread.id)
    assert updated_thread.last_message_id == message.id

    await message_res.delete(message_id=message.id)
