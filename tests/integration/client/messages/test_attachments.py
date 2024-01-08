from yarl import URL

from asyncord.client.messages.models.requests.embeds import Embed, EmbedAuthor, EmbedFooter, EmbedImage, EmbedThumbnail
from asyncord.client.messages.models.requests.messages import (
    AttachmentData,
    CreateMessageRequest,
    UpdateMessageRequest,
)
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.messages.resources import MessageResource

TEST_FILE_NAMES = ['test_image_1.png', 'test_image_2.jpg']


async def test_cteate_message_with_files(messages_res: MessageResource):
    message = await messages_res.create(
        CreateMessageRequest(
            files=[f'tests/data/{file_name}' for file_name in TEST_FILE_NAMES],
        ),
    )
    assert not message.content
    assert len(message.attachments) == 2

    assert {attach.filename for attach in message.attachments} == set(TEST_FILE_NAMES)

    await messages_res.delete(message.id)


async def test_cteate_message_with_attachments(message: MessageResponse, messages_res: MessageResource):
    message = await messages_res.create(
        CreateMessageRequest(
            attachments=[
                AttachmentData(filename=f'new_{file_name}', description=f'test_{i}')
                for i, file_name in enumerate(TEST_FILE_NAMES)
            ],
            files=[f'tests/data/{file_name}' for file_name in TEST_FILE_NAMES],
        ),
    )
    assert not message.content
    assert len(message.attachments) == 2

    assert {attach.filename for attach in message.attachments} == {
        f'new_{filename}' for filename in TEST_FILE_NAMES}

    assert {attach.description for attach in message.attachments} == {
        f'test_{i}' for i in range(len(TEST_FILE_NAMES))}

    await messages_res.delete(message.id)


async def test_cteate_message_with_attachment_in_embed(messages_res: MessageResource):
    embed = Embed(
        title='Test embed with attachments',
        image=EmbedImage(url=f'attachment://{TEST_FILE_NAMES[0]}'),
        thumbnail=EmbedThumbnail(url=f'attachment://{TEST_FILE_NAMES[1]}'),
    )

    message = await messages_res.create(
        CreateMessageRequest(
            embeds=[embed],
            files=[f'tests/data/{file_name}' for file_name in TEST_FILE_NAMES],
        ),
    )
    assert not message.content

    assert len(message.embeds) == 1
    assert message.embeds[0].title == embed.title
    assert URL(message.embeds[0].image.url).path.endswith(TEST_FILE_NAMES[0])
    assert URL(message.embeds[0].thumbnail.url).path.endswith(TEST_FILE_NAMES[1])

    await messages_res.delete(message.id)


async def test_update_message_and_add_attachments(message: MessageResponse, messages_res: MessageResource):
    original_message = message
    message = await messages_res.update(
        message.id,
        UpdateMessageRequest(
            attachments=[
                AttachmentData(filename=f'new_{file_name}', description=f'test_{i}')
                for i, file_name in enumerate(TEST_FILE_NAMES)
            ],
            files=[f'tests/data/{file_name}' for file_name in TEST_FILE_NAMES],
        ),
    )
    assert message.content == original_message.content
    assert len(message.attachments) == 2

    assert {attach.filename for attach in message.attachments} == {
        f'new_{filename}' for filename in TEST_FILE_NAMES}

    assert {attach.description for attach in message.attachments} == {
        f'test_{i}' for i in range(len(TEST_FILE_NAMES))}


async def test_update_message_and_append_attachment(message: MessageResponse, messages_res: MessageResource):
    message = await messages_res.update(
        message.id,
        UpdateMessageRequest(
            files=[f'tests/data/{TEST_FILE_NAMES[0]}'],
        ),
    )
    assert len(message.attachments) == 1

    new_attachment_data = [
        AttachmentData(id=attach.id) for attach in message.attachments
    ] + [AttachmentData(id=0)]

    updated_message = await messages_res.update(
        message.id,
        UpdateMessageRequest(
            attachments=new_attachment_data,
            files=[f'tests/data/{TEST_FILE_NAMES[1]}'],
        ),
    )

    assert len(updated_message.attachments) == 2
    assert updated_message.attachments[0].id == message.attachments[0].id


async def test_replace_attachment(message: MessageResponse, messages_res: MessageResource):
    test_filename = 'test_image.png'
    embed = Embed(
        title='Test embed with attachments',
        image=EmbedImage(url=f'attachment://{test_filename}'),
        author=EmbedAuthor(name='test author'),
        footer=EmbedFooter(text='test footer'),
    )
    with open(f'tests/data/{TEST_FILE_NAMES[0]}', 'rb') as file:
        message = await messages_res.update(
            message.id,
            UpdateMessageRequest(
                embeds=[embed],
                Attachments=[
                    AttachmentData(filename=f'{test_filename}')
                ],
                files=[(f'{TEST_FILE_NAMES[0]}', file.read())],
            ),
        )
    assert len(message.attachments) == 1

    with open(f'tests/data/{TEST_FILE_NAMES[1]}', 'rb') as file:
        updated_message = await messages_res.update(
            message.id,
            UpdateMessageRequest(
                attachments=[AttachmentData(id=0)],
                files=[(f'{TEST_FILE_NAMES[1]}', file.read())],
            ),
        )

    assert len(updated_message.attachments) == 1
    assert updated_message.attachments[0].id != message.attachments[0].id
