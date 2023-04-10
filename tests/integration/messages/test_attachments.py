from asyncord.client.messages import MessageResource
from asyncord.client.models.messages import (
    Embed,
    EmbedImage,
    AttachmentData,
    EmbedThumbnail,
    CreateMessageData,
)

TEST_FILE_NAMES = ['test_image_1.png', 'test_image_2.jpg']


async def test_cteate_message_with_files(messages_res: MessageResource):
    message = await messages_res.create(
        CreateMessageData(
            files=[f'tests/data/{file_name}' for file_name in TEST_FILE_NAMES],
        ),
    )
    assert not message.content
    assert len(message.attachments) == 2

    assert {attach.filename for attach in message.attachments} == set(TEST_FILE_NAMES)

    await messages_res.delete(message.id)


async def test_cteate_message_with_attachments(messages_res: MessageResource):
    message = await messages_res.create(
        CreateMessageData(
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


async def test_cteate_message_attachment_in_embed(messages_res: MessageResource):
    embed = Embed(
        title='Test embed with attachments',
        image=EmbedImage(url=f'attachment://{TEST_FILE_NAMES[0]}'),
        thumbnail=EmbedThumbnail(url=f'attachment://{TEST_FILE_NAMES[1]}'),
    )

    message = await messages_res.create(
        CreateMessageData(
            embeds=[embed],
            files=[f'tests/data/{file_name}' for file_name in TEST_FILE_NAMES],
        ),
    )
    assert not message.content

    assert len(message.embeds) == 1
    assert message.embeds[0].title == embed.title
    assert message.embeds[0].image.url.endswith(TEST_FILE_NAMES[0])
    assert message.embeds[0].thumbnail.url.endswith(TEST_FILE_NAMES[1])

    await messages_res.delete(message.id)
