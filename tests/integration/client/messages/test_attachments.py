from pathlib import Path

from yarl import URL

from asyncord.client.messages.models.requests.embeds import (
    Embed,
    EmbedAuthor,
    EmbedFooter,
    EmbedImage,
)
from asyncord.client.messages.models.requests.messages import (
    CreateMessageRequest,
    UpdateMessageRequest,
)
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.messages.resources import MessageResource
from asyncord.client.models.attachments import Attachment

TEST_FILE_NAMES = ['test_image_1.png', 'test_image_2.png']


async def test_cteate_message_with_files(messages_res: MessageResource) -> None:
    """Test creating a message with files."""
    # fmt: off
    message = await messages_res.create(
        CreateMessageRequest(
            attachments=[
                Attachment(
                    content=Path(f'tests/data/{file_name}'),
                    do_not_attach=True,
                )
                for file_name in TEST_FILE_NAMES],
        ),
    )
    # fmt: on
    assert not message.content
    assert len(message.attachments) == len(TEST_FILE_NAMES)

    assert {attach.filename for attach in message.attachments} == set(TEST_FILE_NAMES)

    await messages_res.delete(message.id)


async def test_cteate_message_with_attachments(
    message: MessageResponse,
    messages_res: MessageResource,
) -> None:
    """Test creating a message with attachments."""
    message = await messages_res.create(
        CreateMessageRequest(
            attachments=[
                Attachment(
                    filename=f'new_{file_name}',
                    description=f'test_{i}',
                    content=Path(f'tests/data/{file_name}'),
                )
                for i, file_name in enumerate(TEST_FILE_NAMES)
            ],
        ),
    )
    assert not message.content
    assert len(message.attachments) == 2
    assert {attach.filename for attach in message.attachments} == {f'new_{filename}' for filename in TEST_FILE_NAMES}
    assert {attach.description for attach in message.attachments} == {f'test_{i}' for i in range(len(TEST_FILE_NAMES))}

    await messages_res.delete(message.id)


async def test_attachment_and_embeds(
    messages_res: MessageResource,
) -> None:
    """Test creating a message with attachments in an embed."""
    embed = Embed(
        title='Test embed with attachments',
        image=EmbedImage(url=f'attachment://{TEST_FILE_NAMES[0]}'),
        thumbnail=EmbedImage(url=f'attachment://{TEST_FILE_NAMES[1]}'),
    )

    message = await messages_res.create(
        CreateMessageRequest(
            embeds=[embed],
            attachments=[Path(f'tests/data/{file_name}') for file_name in TEST_FILE_NAMES],
        ),
    )
    assert not message.content

    assert len(message.embeds) == 1
    assert message.embeds[0].title == embed.title
    assert message.embeds[0].image
    assert URL(message.embeds[0].image.url).path.endswith(TEST_FILE_NAMES[0])
    assert message.embeds[0].thumbnail
    assert URL(message.embeds[0].thumbnail.url).path.endswith(TEST_FILE_NAMES[1])

    await messages_res.delete(message.id)


async def test_embed_attachment(
    messages_res: MessageResource,
) -> None:
    """Test creating a message with an attachment in an embed."""
    embed = Embed(
        title='Test embed with attachments',
        image=Path(f'tests/data/{TEST_FILE_NAMES[0]}'),
    )

    message = await messages_res.create(
        CreateMessageRequest(
            embeds=[embed],
        ),
    )
    assert not message.content

    assert len(message.embeds) == 1
    assert message.embeds[0].title == embed.title
    assert message.embeds[0].image
    assert URL(message.embeds[0].image.url).path.endswith('image_0.png')

    await messages_res.delete(message.id)


async def test_single_embed_attachment(
    messages_res: MessageResource,
) -> None:
    """Test creating a message with a single attachment in an embed."""
    embed = Embed(
        title='Test embed with attachments',
        image=Path(f'tests/data/{TEST_FILE_NAMES[0]}'),
    )

    message = await messages_res.create(
        CreateMessageRequest(
            embeds=embed,
        ),
    )
    assert not message.content

    assert len(message.embeds) == 1
    assert message.embeds[0].title == embed.title
    assert message.embeds[0].image
    assert URL(message.embeds[0].image.url).path.endswith('image_0.png')

    await messages_res.delete(message.id)


async def test_update_message_and_add_attachments(
    message: MessageResponse,
    messages_res: MessageResource,
) -> None:
    """Test updating a message and adding attachments."""
    original_message = message
    message = await messages_res.update(
        message.id,
        UpdateMessageRequest(
            attachments=[
                Attachment(
                    filename=f'new_{file_name}',
                    description=f'test_{i}',
                    content=Path(f'tests/data/{file_name}'),
                )
                for i, file_name in enumerate(TEST_FILE_NAMES)
            ],
        ),
    )
    assert message.content == original_message.content
    assert len(message.attachments) == 2

    assert {attach.filename for attach in message.attachments} == {f'new_{filename}' for filename in TEST_FILE_NAMES}

    assert {attach.description for attach in message.attachments} == {f'test_{i}' for i in range(len(TEST_FILE_NAMES))}


async def test_update_message_and_append_attachment(
    message: MessageResponse,
    messages_res: MessageResource,
) -> None:
    """Test updating a message and appending an attachment."""
    message = await messages_res.update(
        message.id,
        UpdateMessageRequest(
            attachments=[Path(f'tests/data/{TEST_FILE_NAMES[0]}')],
        ),
    )
    assert len(message.attachments) == 1

    new_attachment_data = [Attachment(id=attach.id) for attach in message.attachments]
    new_attachment_data.append(
        Attachment(
            id=0,
            content=Path(f'tests/data/{TEST_FILE_NAMES[1]}'),
        ),
    )

    updated_message = await messages_res.update(
        message.id,
        UpdateMessageRequest(
            attachments=new_attachment_data,
        ),
    )

    assert len(updated_message.attachments) == 2
    assert updated_message.attachments[0].id == message.attachments[0].id


async def test_replace_attachment(message: MessageResponse, messages_res: MessageResource) -> None:
    """Test replacing an attachment."""
    test_filename = 'test_image.png'
    embed = Embed(
        title='Test embed with attachments',
        image=EmbedImage(url=f'attachment://{test_filename}'),
        author=EmbedAuthor(name='test author'),
        footer=EmbedFooter(text='test footer'),
    )
    with Path(f'tests/data/{TEST_FILE_NAMES[0]}').open('rb') as file:
        message = await messages_res.update(
            message.id,
            UpdateMessageRequest(
                embeds=[embed],
                attachments=[
                    Attachment(
                        filename=f'{TEST_FILE_NAMES[0]}',
                        content=file.read(),
                    ),
                ],
            ),
        )
    assert len(message.attachments) == 1

    with Path(f'tests/data/{TEST_FILE_NAMES[1]}').open('rb') as file:
        updated_message = await messages_res.update(
            message.id,
            UpdateMessageRequest(
                attachments=[
                    Attachment(
                        id=0,
                        description='test description',
                        filename=f'{TEST_FILE_NAMES[1]}',
                        content=file.read(),
                    ),
                ],
            ),
        )

    assert len(updated_message.attachments) == 1
    assert updated_message.attachments[0].id != message.attachments[0].id
    assert updated_message.attachments[0].description == 'test description'
