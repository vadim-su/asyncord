from yarl import URL

from asyncord.client.messages.models.embed_input import (
    EmbedAuthorInput,
    EmbedFooterInput,
    EmbedImageInput,
    EmbedInput,
    EmbedThumbnailInput,
)
from asyncord.client.messages.models.input import (
    AttachmentDataInput,
    CreateMessageInput,
    UpdateMessageInput,
)
from asyncord.client.messages.models.output import MessageOutput
from asyncord.client.messages.resources import MessageResource

TEST_FILE_NAMES = ['test_image_1.png', 'test_image_2.jpg']


async def test_cteate_message_with_files(messages_res: MessageResource):
    message = await messages_res.create(
        CreateMessageInput(
            files=[f'tests/data/{file_name}' for file_name in TEST_FILE_NAMES],
        ),
    )
    assert not message.content
    assert len(message.attachments) == 2

    assert {attach.filename for attach in message.attachments} == set(TEST_FILE_NAMES)

    await messages_res.delete(message.id)


async def test_cteate_message_with_attachments(message: MessageOutput, messages_res: MessageResource):
    message = await messages_res.create(
        CreateMessageInput(
            attachments=[
                AttachmentDataInput(filename=f'new_{file_name}', description=f'test_{i}')
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
    embed = EmbedInput(
        title='Test embed with attachments',
        image=EmbedImageInput(url=f'attachment://{TEST_FILE_NAMES[0]}'),
        thumbnail=EmbedThumbnailInput(url=f'attachment://{TEST_FILE_NAMES[1]}'),
    )

    message = await messages_res.create(
        CreateMessageInput(
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


async def test_update_message_and_add_attachments(message: MessageOutput, messages_res: MessageResource):
    original_message = message
    message = await messages_res.update(
        message.id,
        UpdateMessageInput(
            attachments=[
                AttachmentDataInput(filename=f'new_{file_name}', description=f'test_{i}')
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


async def test_update_message_and_append_attachment(message: MessageOutput, messages_res: MessageResource):
    message = await messages_res.update(
        message.id,
        UpdateMessageInput(
            files=[f'tests/data/{TEST_FILE_NAMES[0]}'],
        ),
    )
    assert len(message.attachments) == 1

    new_attachment_data = [
        AttachmentDataInput(id=attach.id) for attach in message.attachments
    ] + [AttachmentDataInput(id=0)]

    updated_message = await messages_res.update(
        message.id,
        UpdateMessageInput(
            attachments=new_attachment_data,
            files=[f'tests/data/{TEST_FILE_NAMES[1]}'],
        ),
    )

    assert len(updated_message.attachments) == 2
    assert updated_message.attachments[0].id == message.attachments[0].id


async def test_replace_attachment(message: MessageOutput, messages_res: MessageResource):
    test_filename = 'test_image.png'
    embed = EmbedInput(
        title='Test embed with attachments',
        image=EmbedImageInput(url=f'attachment://{test_filename}'),
        author=EmbedAuthorInput(name='test author'),
        footer=EmbedFooterInput(text='test footer'),
    )
    with open(f'tests/data/{TEST_FILE_NAMES[0]}', 'rb') as file:
        message = await messages_res.update(
            message.id,
            UpdateMessageInput(
                embeds=[embed],
                Attachments=[
                    AttachmentDataInput(filename=f'{test_filename}')
                ],
                files=[(f'{TEST_FILE_NAMES[0]}', file.read())],
            ),
        )
    assert len(message.attachments) == 1

    with open(f'tests/data/{TEST_FILE_NAMES[1]}', 'rb') as file:
        updated_message = await messages_res.update(
            message.id,
            UpdateMessageInput(
                attachments=[AttachmentDataInput(id=0)],
                files=[(f'{TEST_FILE_NAMES[1]}', file.read())],
            ),
        )

    assert len(updated_message.attachments) == 1
    assert updated_message.attachments[0].id != message.attachments[0].id
