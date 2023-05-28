"""This module contains message models."""
from __future__ import annotations

import datetime
import enum
import io
import mimetypes
from collections.abc import Mapping
from pathlib import Path
from typing import Annotated, Any, BinaryIO, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, root_validator

from asyncord.client.models.channels import Channel, ChannelMention
from asyncord.client.models.components import SELECT_COMPONENT_TYPE_LIST, Component, ComponentType
from asyncord.client.models.emoji import Emoji
from asyncord.client.models.members import Member
from asyncord.client.models.stickers import Sticker
from asyncord.client.models.users import User
from asyncord.snowflake import Snowflake

MAX_EMBED_TEXT_LENGTH = 6000

_OpennedFileType = io.BufferedReader | io.BufferedRandom

AttachmentContentType = bytes | BinaryIO | _OpennedFileType
FilePathType = str | Path


class AttachedFile(BaseModel):
    """Attached file.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#attachment-object-attachment-structure
    """

    filename: str
    """Name of attached file."""

    content_type: str
    """Media type of the file."""

    content: AttachmentContentType
    """File content."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    """Pydantic config."""

    def __init__(  # noqa: D107
        self, *, content: FilePathType | AttachmentContentType, **kwargs: dict[str, Any],
    ) -> None:
        super().__init__(content=content, **kwargs)

    @root_validator(pre=True)
    def validate_file_info(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Fill filename and content type if not provided.

        Args:
            values (dict): The values to validate.

        Returns:
            dict: The validated values.
        """
        content = values.get('content')
        if not content:
            return values

        if isinstance(content, str):
            content = Path(content)

        # if file informaton is provided, skip
        if values.get('filename') and values.get('content_type'):
            return values

        if isinstance(content, Path):
            content = content.open('rb')
            values['content'] = content
            if not values.get('filename'):
                values['filename'] = Path(content.name).name

        elif isinstance(content, BinaryIO | io.BufferedReader | io.BufferedRandom):
            if not values.get('filename'):
                values['filename'] = Path(content.name).name

        elif isinstance(content, bytes):
            if not values.get('filename'):
                raise ValueError("'filename' is required for bytes file")

        else:
            raise ValueError(f'Unsupported file object type: {type(content).__name__}')

        if not values.get('content_type'):
            content_type = mimetypes.guess_type(values['filename'])[0]
            if not content_type:
                raise ValueError(f"Unable to guess content type for {values['filename']}")

            values['content_type'] = content_type

        return values


_FilesListType = list[AttachedFile | FilePathType | _OpennedFileType]
_FileMapType = Mapping[str | Path, 'AttachmentContentType']
FilesType = _FilesListType | _FileMapType


@enum.unique
class EmbedType(enum.StrEnum):
    """Embed type.

    Embed types are "loosely defined" and, for the most part, are not used by our
    clients for rendering. Embed attributes power what is rendered.
    Embed types should be considered deprecated and might be removed in
    a future API version.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-types
    """

    RICH = 'rich'
    """generic embed rendered from embed attributes"""

    IMAGE = 'image'
    """image embed"""

    VIDEO = 'video'
    """video embed"""

    GIFV = 'gifv'
    """animated gif image embed rendered as a video embed"""

    ARTICLE = 'article'
    """article embed"""

    LINK = 'link'
    """link embed"""


class EmbedFooter(BaseModel):
    """Embed footer object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-footer-structure
    """

    # WPS432: Found magic number
    text: str = Field(max_length=2048)
    """footer text"""

    icon_url: str | None = None
    """url of footer icon (only supports http(s) and attachments)"""

    proxy_icon_url: str | None = None
    """a proxied url of footer icon"""


class EmbedImage(BaseModel):
    """Embed image object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-image-structure
    """

    url: str
    """source url of image (only supports http(s) and attachments)"""

    proxy_url: str | None = None
    """a proxied url of the image"""

    height: int | None = None
    """height of image"""

    width: int | None = None
    """width of image"""


class EmbedThumbnail(BaseModel):
    """Embed thumbnail object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-thumbnail-structure
    """

    url: str
    """source url of thumbnail (only supports http(s) and attachments)"""

    proxy_url: str | None = None
    """a proxied url of the thumbnail"""

    height: int | None = None
    """height of thumbnail"""

    width: int | None = None
    """width of thumbnail"""


class EmbedVideo(BaseModel):
    """Embed video object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-video-structure
    """

    url: str | None = None
    """source url of video"""

    proxy_url: str | None = None
    """a proxied url of the video"""

    height: int | None = None
    """height of video"""

    width: int | None = None
    """width of video"""


class EmbedProvider(BaseModel):
    """Embed provider object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-provider-structure
    """

    name: str | None = None
    """name of provider"""

    url: str | None = None
    """url of provider"""


class EmbedAuthor(BaseModel):
    """Embed author object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-author-structure
    """

    name: str = Field(max_length=256)
    """name of author"""

    url: str | None = None
    """url of author"""

    icon_url: str | None = None
    """url of author icon (only supports http(s) and attachments)"""

    proxy_icon_url: str | None = None
    """a proxied url of author icon"""


class EmbedField(BaseModel):
    """Embed field object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-field-structure
    """

    name: str = Field(max_length=256)  # - Found magic number
    """name of the field"""

    # WPS110: Found wrong variable name
    # WPS432: Found magic number
    value: str = Field(max_length=1024)
    """value of the field"""

    inline: bool | None = None
    """whether or not this field should display inline"""


class Embed(BaseModel):
    """Embed object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#embed-object
    """

    title: str | None = Field(None, max_length=256)
    """title of embed"""

    type: EmbedType | None = None
    """type of embed (always "rich" for webhook embeds)"""

    description: str | None = Field(None, max_length=4096)
    """description of embed"""

    url: str | None = None
    """url of embed"""

    timestamp: datetime.datetime | None = None
    """timestamp of embed content"""

    color: int | None = None
    """color code of the embed"""

    footer: EmbedFooter | None = None
    """footer information"""

    image: EmbedImage | None = None
    """image information"""

    thumbnail: EmbedThumbnail | None = None
    """thumbnail information"""

    video: EmbedVideo | None = None
    """video information"""

    provider: EmbedProvider | None = None
    """provider information"""

    author: EmbedAuthor | None = None
    """author information"""

    # FIXME: Field(None, max_items=25) doesn't work On field "fields"
    # the following field constraints are set but not enforced: max_items.
    fields: list[EmbedField] | None = None
    """fields information"""


@enum.unique
class MessageFlags(enum.IntFlag):
    """Message flags.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#message-object-message-flags
    """

    CROSSPOSTED = 1
    """this message has been published to subscribed channels (via Channel Following)"""

    IS_CROSSPOST = 1 << 1
    """this message originated from a message in another channel (via Channel Following)"""

    SUPPRESS_EMBEDS = 1 << 2
    """do not include any embeds when serializing this message"""

    SOURCE_MESSAGE_DELETED = 1 << 3
    """the source message for this crosspost has been deleted (via Channel Following)"""

    URGENT = 1 << 4
    """this message came from the urgent message system"""

    HAS_THREAD = 1 << 5
    """this message is only visible to the user who invoked the Interaction"""

    EPHEMERAL = 1 << 6
    """this message is only visible to the user who invoked the Interaction"""

    LOADING = 1 << 7
    """this message is an Interaction Response and the bot is 'thinking'"""

    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8
    """this message failed to mention some roles and add their members to the thread"""


class AttachmentData(BaseModel):
    """Attachment object using for creating messages and editing messages.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#attachment-object
    """

    id: Snowflake | int | None = None
    """Attachment id"""

    filename: str | None = None
    """Name of file attached"""

    description: str | None = Field(None, max_length=1024)
    """Description for the file (max 1024 characters)"""

    content_type: str | None = None
    """Media type of the file"""

    size: int | None = None
    """Size of file in bytes"""

    url: str | None = None
    """Source url of file"""

    proxy_url: str | None = None
    """Proxied url of file"""

    height: int | None = None
    """Height of file (if image)"""

    width: int | None = None
    """Width of file (if image)"""

    ephemeral: bool | None = None
    """Whether this attachment is ephemeral

    Ephemeral attachments will automatically be removed after a set period of time.
    Ephemeral attachments on messages are guaranteed to be available as long as
    the message itself exists.
    """


class _MessageData(BaseModel):
    """Base message data class used for message creation and editing.

    Contains axillary validation methods and general fields.
    """

    @root_validator(skip_on_failure=True)
    def has_any_content(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate message content.

        Read more info at:
        https://discord.com/developers/docs/resources/channel#message-object-message-structure

        Args:
            values (dict[str, Any]): The values to validate.

        Raises:
            ValueError: If the message has no content or embeds.

        Returns:
            dict: The validated values.
        """
        has_any_content = bool(
            values.get('content', False)
            or values.get('embeds', False)
            or values.get('sticker_ids', False)
            or values.get('components', False)
            or values.get('files', False),
        )

        if not has_any_content:
            raise ValueError(
                'Message must have content, embeds, stickers, components or files.',
            )

        return values

    @field_validator('embeds', check_fields=False)
    def validate_embeds(cls, embeds: list[Embed] | None) -> list[Embed] | None:
        """Check total embed text length.

        Read more info at:
        https://discord.com/developers/docs/resources/channel#message-object-message-structure

        Args:
            embeds (list[Embed] | None): The values to validate.

        Raises:
            ValueError: If the total embed text length is more than 6000 characters.

        Returns:
            list[Embed] | None: The validated values.
        """
        if not embeds:
            return embeds

        total_embed_text_length = 0
        for embed in embeds:
            total_embed_text_length += cls._embed_text_length(embed)

            if total_embed_text_length > MAX_EMBED_TEXT_LENGTH:
                raise ValueError(
                    'Total embed text length must be less than 6000 characters.',
                )

        return embeds

    @field_validator('files', mode='before', check_fields=False)
    def validate_attached_files(cls, files: FilesType) -> list[AttachedFile]:
        """Prepare attached files.

        Args:
            files (FilesType): Files to prepare.

        Returns:
            list[AttachedFile: Prepared files to attach.
        """
        if not files:
            return []

        attached_files = files.items() if isinstance(files, Mapping) else files

        prepared_files = []

        for content in attached_files:
            match content:
                case AttachedFile():
                    prepared_files.append(content)

                # if list item - file_path or BinaryIO
                case str() | Path() | io.BufferedReader() | io.BufferedRandom() | BinaryIO():
                    prepared_files.append(AttachedFile(content=content))

                # if mapping item - filename, file
                case str() | Path() as filename, content if isinstance(content, AttachmentContentType):
                    if isinstance(filename, Path):
                        filename = filename.name
                    prepared_files.append(
                        AttachedFile(filename=filename, content=content),  # type: ignore
                    )

                case _:
                    raise ValueError('Invalid file object type')

        return prepared_files

    @field_validator('attachments', check_fields=False)
    def validate_attachments(cls, attachments: list[AttachmentData] | None) -> list[AttachmentData] | None:
        """Validate attachments.

        Args:
            attachments (list[AttachmentData] | None): Attachments to validate.

        Raises:
            ValueError: If attachments have mixed ids.

        Returns:
            list[AttachmentData] | None: Validated attachments.
        """
        if not attachments:
            return attachments

        attachment_id_exist_list = [attach.id is not None for attach in attachments]

        if all(attachment_id_exist_list):
            # Check is disabled because updated attachments already have id generated by Discord.

            # for attachment in attachments:
            #     if attachment.id >= len(files):

            return attachments

        if any(attachment_id_exist_list):
            raise ValueError('Attachments must have all ids or none of them')

        for index, attachment in enumerate(attachments):
            attachment.id = index

        return attachments

    @field_validator('components', check_fields=False)
    def validate_components(cls, components: list[Component] | None) -> list[Component] | None:
        """Validate components.

        Args:
            components (list[Component] | None): Components to validate.

        Raises:
            ValueError: If components have more than 5 action rows.

        Returns:
            list[Component] | None: Validated components.
        """
        if not components:
            return components

        action_row_count = 0

        for component in components:
            match component.type:
                case ComponentType.ACTION_ROW:
                    action_row_count += 1
                case ComponentType.BUTTON:
                    raise ValueError('Button components must be inside ActionRow')
                case _ if component.type in SELECT_COMPONENT_TYPE_LIST:
                    raise ValueError('Select components must be inside ActionRow')

        if action_row_count > 5:
            raise ValueError('ActionRow components must be less than 5')

        return components

    @classmethod
    def _embed_text_length(cls, embed: Embed) -> int:
        """Get the length of the embed text.

        Args:
            embed (Embed): Embed to get the length of.

        Returns:
            int: length of the embed text.
        """
        embed_text_length = len(embed.title or '')
        embed_text_length += len(embed.description or '')

        if embed.footer:
            embed_text_length += len(embed.footer.text or '')

        if embed.author:
            embed_text_length += len(embed.author.name or '')

        for field in embed.fields or []:
            embed_text_length += len(field.name or '')
            embed_text_length += len(field.value or '')

        return embed_text_length


@enum.unique
class AllowedMentionType(enum.Enum):
    """Type of allowed mention.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#allowed-mentions-object-allowed-mention-types
    """

    ROLES = 'roles'
    """Controls role mentions."""

    USERS = 'users'
    """Controls user mentions."""

    EVERYONE = 'everyone'
    """Controls @everyone and @here mentions"""


class AllowedMentions(BaseModel):
    """Allowed mentions object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#allowed-mentions-object
    """

    parse: list[AllowedMentionType] | None = None
    """array of allowed mention types to parse from the content"""

    roles: list[Snowflake] | None = Field(None, max_items=100)
    """array of role_ids to mention"""

    users: list[Snowflake] | None = Field(None, max_items=100)
    """array of user_ids to mention"""

    replied_user: bool | None = None
    """for replies, whether to mention the author of the message being replied to"""


class MessageReference(BaseModel):
    """Message reference object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#message-reference-object
    """

    message_id: Snowflake | None = None
    """id of the originating message"""

    channel_id: Snowflake | None = None
    """id of the originating message's channel"""

    guild_id: Snowflake | None = None
    """id of the originating message's guild"""

    fail_if_not_exists: bool | None = None
    """when sending, whether to error if the referenced message doesn't exist
    instead of sending as a normal (non-reply) message, default true"""


@enum.unique
class InteractionType(enum.IntEnum):
    """Type of interaction.

    Read more info at:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-type
    """

    PING = 1
    """ping interaction"""

    APPLICATION_COMMAND = 2
    """slash command"""

    MESSAGE_COMPONENT = 3
    """message component"""

    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    """autocomplete command"""

    MODAL_SUBMIT = 5
    """modal submit"""


class MessageInteraction(BaseModel):
    """Message interaction object.

    This is sent on the message object when the message is a response to
    an Interaction without an existing message.

    Read more info at:
    https://discord.com/developers/docs/interactions/receiving-and-responding#message-interaction-object
    """

    id: Snowflake
    """id of the interaction"""

    type: InteractionType
    """type of interaction"""

    name: str
    """Name of the application command, including subcommands and subcommand groups"""

    user: User
    """User who invoked the interaction"""

    member: Member | None = None
    """Member who invoked the interaction"""


class CreateMessageData(_MessageData):
    """The data to create a message with.

    More info at:
    https://discord.com/developers/docs/resources/channel#create-message
    """

    content: str | None = Field(None, max_length=2000)
    """The message content."""

    nonce: Annotated[str, Field(max_length=25)] | int | None = None
    """Can be used to verify a message was sent.

    Value will appear in the Message Create event.
    """

    tts: bool | None = None
    """True if this is a TTS message."""

    embeds: list[Embed] | None = None
    """Embedded rich content."""

    allowed_mentions: AllowedMentions | None = None
    """Allowed mentions for the message."""

    message_reference: MessageReference | None = None
    """Reference data sent with crossposted messages."""

    components: list[Component] | None = None
    """Components to include with the message."""

    sticker_ids: list[Snowflake] | None = None
    """Sticker ids to include with the message."""

    files: list[AttachedFile] = Field(default_factory=list, exclude=True)
    """Contents of the file being sent.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """

    attachments: list[AttachmentData] | None = None
    """Attachment objects with filename and description.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS] | None = None
    """The flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """


class UpdateMessageData(_MessageData):
    """The data to update a message with.

    More info at:
    https://discord.com/developers/docs/resources/channel#edit-message
    """

    content: str | None = Field(None, max_length=2000)
    """The message content."""

    embeds: list[Embed] | None = None
    """Embedded rich content."""

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS] | None = None
    """The flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    allowed_mentions: AllowedMentions | None = None
    """Allowed mentions for the message."""

    components: list[Component] | None = None
    """Components to include with the message."""

    files: list[AttachedFile] = Field(default_factory=list, exclude=True)
    """Contents of the file being sent.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """

    attachments: list[AttachmentData] | None = None
    """Attachment objects with filename and description.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """


class Attachment(BaseModel):
    """Attachment object.

    ATTENTION: This is not the same as the `AttachmentData` object.
    If you want to send an attachment, use the `AttachmentData` object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#attachment-object
    """

    id: Snowflake
    """Attachment id"""

    filename: str
    """Name of file attached"""

    description: str | None = Field(None, max_length=1024)
    """Description for the file (max 1024 characters)"""

    content_type: str | None = None
    """Media type of the file"""

    size: int
    """Size of file in bytes"""

    url: str
    """Source url of file"""

    proxy_url: str
    """Proxied url of file"""

    height: int | None = None
    """Height of file (if image)"""

    width: int | None = None
    """Width of file (if image)"""

    ephemeral: bool | None = None
    """Whether this attachment is ephemeral

    Ephemeral attachments will automatically be removed after a set period of time.
    Ephemeral attachments on messages are guaranteed to be available as long as
    the message itself exists.
    """


class Reaction(BaseModel):
    """Reaction object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#reaction-object
    """

    count: int
    """times this emoji has been used to react"""

    me: bool
    """whether the current user reacted using this emoji"""

    # FIXME: emoji is partial emoji object. I didn't find any info about it.
    emoji: Emoji
    """emoji information"""


@enum.unique
class MessageType(enum.IntEnum):
    """Type of message.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#message-object-message-types
    """

    DEFAULT = 0
    """a default message"""

    RECIPIENT_ADD = 1
    """a recipient was added to a group DM"""

    RECIPIENT_REMOVE = 2
    """a recipient was removed from a group DM"""

    CALL = 3
    """a call was started in the channel"""

    CHANNEL_NAME_CHANGE = 4
    """a channel name was changed"""

    CHANNEL_ICON_CHANGE = 5
    """a channel icon was changed"""

    CHANNEL_PINNED_MESSAGE = 6
    """a message was pinned"""

    USER_JOIN = 7
    """a user joined the guild"""

    GUILD_BOOST = 8
    """a user started boosting the guild"""

    GUILD_BOOST_TIER_1 = 9
    """a user boosted the guild to tier 1"""

    GUILD_BOOST_TIER_2 = 10
    """a user boosted the guild to tier 2"""

    GUILD_BOOST_TIER_3 = 11
    """a user boosted the guild to tier 3"""

    CHANNEL_FOLLOW_ADD = 12
    """a channel was followed into a news channel"""

    GUILD_DISCOVERY_DISQUALIFIED = 14
    """a guild discovery disqualification occurred"""

    GUILD_DISCOVERY_REQUALIFIED = 15
    """a guild discovery requalification occurred"""

    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    """a guild discovery grace period initial warning occurred"""

    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    """a guild discovery grace period final warning occurred"""

    THREAD_CREATED = 18
    """a thread was created"""

    REPLY = 19
    """a reply to another message"""

    CHAT_INPUT_COMMAND = 20
    """a message sent in response to an Interaction"""

    THREAD_STARTER_MESSAGE = 21
    """a message in a thread was published to the parent channel"""

    GUILD_INVITE_REMINDER = 22
    """a thread was created from an announcement message with the `HAS_THREAD` flag"""

    CONTEXT_MENU_COMMAND = 23
    """a context menu command was used"""

    AUTO_MODERATION_ACTION = 24
    """an auto moderation action was taken"""


class MessageActivityType(enum.IntEnum):
    """Type of activity.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#message-object-message-activity-types
    """

    JOIN = 1
    """join a party"""

    SPECTATE = 2
    """spectate a game"""

    LISTEN = 3
    """listen along to a song"""

    JOIN_REQUEST = 5
    """join a request to play a game"""


class MessageActivity(BaseModel):
    """Message activity object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#message-object-message-activity-structure
    """

    type: MessageActivityType
    """type of message activity"""

    party_id: str | None = None
    """party_id from a Rich Presence event"""


# FIXME: It's AI guess, need to be tested
class MessageApplication(BaseModel):
    """Message application object."""

    id: Snowflake
    """id of the application"""

    cover_image: str | None = None
    """id of the embed's image asset"""

    description: str
    """application's description"""

    icon: str | None = None
    """id of the application's icon"""

    name: str
    """name of the application"""


class Message(BaseModel):
    """Message object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#message-object
    """

    id: Snowflake
    """id of the message"""

    channel_id: Snowflake
    """id of the channel the message was sent in"""

    author: User
    """author of the message"""

    content: str
    """contents of the message"""

    timestamp: datetime.datetime
    """when this message was sent"""

    edited_timestamp: datetime.datetime | None = None
    """when this message was edited (or null if never)"""

    tts: bool
    """whether this was a TTS message"""

    mention_everyone: bool
    """whether this message mentions everyone"""

    mentions: list[User]
    """users specifically mentioned in the message"""

    mention_roles: list[Snowflake]
    """roles specifically mentioned in this message"""

    mention_channels: list[ChannelMention] | None = None
    """channels specifically mentioned in this message"""

    attachments: list[Attachment]
    """any attached files"""

    embeds: list[Embed]
    """any embedded content"""

    reactions: list[Reaction] | None = None
    """any reactions to the message"""

    nonce: int | str | None = None
    """used for validating a message was sent"""

    pinned: bool
    """whether this message is pinned"""

    webhook_id: Snowflake | None = None
    """if the message is generated by a webhook, this is the webhook's id"""

    type: MessageType
    """type of message"""

    activity: MessageActivity | None = None
    """sent with Rich Presence-related chat embeds"""

    application: MessageApplication | None = None
    """sent with Rich Presence-related chat embeds"""

    application_id: Snowflake | None = None
    """if the message is an Interaction or application-owned webhook,
    this is the id of the application
    """

    message_reference: MessageReference | None = None
    """reference data sent with crossposted messages"""

    flags: MessageFlags
    """message flags combined as a bitfield"""

    stickers: list[Sticker] | None = None
    """message stickers"""

    referenced_message: Message | None = None
    """the message this message references, if the message is a reply"""

    thread: Channel | None = None
    """the thread that was started from this message, includes thread member object"""

    components: list[Component] | None = None
    """sent if the message is a response to an Interaction"""

    interaction: MessageInteraction | None = None
    """sent if the message is a response to an Interaction"""

    message: str | None = None
    """error message"""
