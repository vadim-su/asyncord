"""This module contains message models.

Reference:
https://discord.com/developers/docs/resources/channel#message-object
"""

from __future__ import annotations

import datetime
import enum
import io
import mimetypes
from collections.abc import Mapping
from pathlib import Path
from typing import Annotated, Any, BinaryIO, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from asyncord.client.channels.models.common import ChannelType
from asyncord.client.channels.models.output import ChannelOutput
from asyncord.client.members.models import MemberOutput
from asyncord.client.messages.models.components import SELECT_COMPONENT_TYPE_LIST, Component, ComponentType
from asyncord.client.models.emoji import Emoji
from asyncord.client.models.stickers import StickerFormatType
from asyncord.client.users.models import UserOutput
from asyncord.color import Color, ColorInput
from asyncord.snowflake import Snowflake

MAX_EMBED_TEXT_LENGTH = 6000
"""Maximum length of the embed text."""

_OpennedFileType = io.BufferedReader | io.BufferedRandom
_AttachmentContentType = bytes | BinaryIO | _OpennedFileType
_FilePathType = str | Path
_AttachedFileInputType = Annotated[_FilePathType | _AttachmentContentType, _AttachmentContentType]


class ChannelMention(BaseModel):
    """Channel mention object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#channel-mention-object
    """

    id: Snowflake
    """Channel id."""

    guild_id: Snowflake
    """Guild id containing the channel."""

    type: ChannelType
    """Channel type."""

    name: str
    """Channel name."""


class AttachedFile(BaseModel):
    """Attached file.

    Reference:
    https://discord.com/developers/docs/resources/channel#attachment-object-attachment-structure
    """

    filename: str = None  # type: ignore
    """Name of attached file."""

    content_type: str = None  # type: ignore
    """Media type of the file."""

    content: _AttachedFileInputType
    """File content."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    """Pydantic config.# type: ignore
    
    Arbitrary types are allowed because of the `content` field can be BinaryIO
    and other unsupported pydantic types.
    """

    @model_validator(mode='before')
    def validate_file_info(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Fill filename and content type if not provided.

        Args:
            values: Values to validate.

        Returns:
            Validated values.
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


_FilesListType = list[AttachedFile | _FilePathType | _OpennedFileType]
_FileMapType = Mapping[str | Path, _AttachmentContentType]
_FilesType = _FilesListType | _FileMapType


@enum.unique
class EmbedType(enum.StrEnum):
    """Object representing the type of an embed.

    Embed types are "loosely defined" and, for the most part, are not used by clients for rendering.
    Embed attributes power what is rendered.
    Embed types should be considered deprecated and might be removed in a future API version.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-types
    """

    RICH = 'rich'
    """Generic embed rendered from embed attributes."""

    IMAGE = 'image'
    """Image embed."""

    VIDEO = 'video'
    """Video embed."""

    GIFV = 'gifv'
    """Animated gif image embed rendered as a video embed."""

    ARTICLE = 'article'
    """Article embed."""

    LINK = 'link'
    """Link embed."""


class EmbedFooter(BaseModel):
    """Object representing footer of an embed.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-footer-structure
    """

    text: str = Field(max_length=2048)
    """Text of the footer."""

    icon_url: str | None = None
    """URL of the footer icon (only supports http(s) and attachments)."""

    proxy_icon_url: str | None = None
    """Proxied URL of the footer icon."""


class EmbedImage(BaseModel):
    """Object representing image in an embed.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-image-structure
    """

    url: str
    """Source URL of image (only supports http(s) and attachments)."""

    proxy_url: str | None = None
    """Proxied URL of image."""

    height: int | None = None
    """Height of image."""

    width: int | None = None
    """Width of image."""


class EmbedThumbnail(BaseModel):
    """Object representing thumbnail in an embed.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-thumbnail-structure
    """

    url: str
    """Source URL of thumbnail (only supports http(s) and attachments)."""

    proxy_url: str | None = None
    """Proxied URL of thumbnail."""

    height: int | None = None
    """Height of thumbnail."""

    width: int | None = None
    """Width of thumbnail."""


class EmbedVideo(BaseModel):
    """Object representing video in an embed.

    Bots can not send this object.
    Discord API will ignore it if provided.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-video-structure
    """

    url: str | None = None
    """Source URL of the video."""

    proxy_url: str | None = None
    """Proxied URL of the video."""

    height: int | None = None
    """Height of the video."""

    width: int | None = None
    """Width of the video."""


class EmbedProvider(BaseModel):
    """Object representing the provider of an embed.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-provider-structure
    """

    name: str | None = None
    """Name of the provider."""

    url: str | None = None
    """URL of the provider."""


class EmbedAuthor(BaseModel):
    """Object representing the author of an embed.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-author-structure
    """

    name: str = Field(max_length=256)
    """Name of author."""

    url: str | None = None
    """URL of author."""

    icon_url: str | None = None
    """URL of author icon (only supports http(s) and attachments)."""

    proxy_icon_url: str | None = None
    """Proxied URL of author icon."""


class EmbedField(BaseModel):
    """Embed field object.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-field-structure
    """

    name: str = Field(max_length=256)
    """Name of the field."""

    value: str = Field(max_length=1024)
    """Value of the field."""

    inline: bool | None = None
    """Whether or not this field should display inline."""


class Embed(BaseModel):
    """Embed object.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object
    """

    title: str | None = Field(None, max_length=256)
    """Title of the embed."""

    type: EmbedType | None = None
    """Type of the embed.

    Always "rich" for webhook embeds.
    """

    description: str | None = Field(None, max_length=4096)
    """Description of the embed."""

    url: str | None = None
    """URL of the embed."""

    timestamp: datetime.datetime | None = None
    """Timestamp of the embed content."""

    color: ColorInput | None = None
    """Color code of the embed."""

    footer: EmbedFooter | None = None
    """Footer information."""

    image: EmbedImage | None = None
    """Image information."""

    thumbnail: EmbedThumbnail | None = None
    """Thumbnail information."""

    video: EmbedVideo | None = None
    """Video information.
    
    Bots can not use this field.
    Discord API will ignore it if provided
    """

    provider: EmbedProvider | None = None
    """Provider information."""

    author: EmbedAuthor | None = None
    """Author information."""

    fields: list[EmbedField] = Field(default_factory=list, max_length=25)
    """List of fields.

    Maximum of 25 items.
    """


@enum.unique
class MessageFlags(enum.IntFlag):
    """Message flags.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-object-message-flags
    """

    CROSSPOSTED = 1
    """This message has been published to subscribed channels (via Channel Following)."""

    IS_CROSSPOST = 1 << 1
    """This message originated from a message in another channel (via Channel Following)."""

    SUPPRESS_EMBEDS = 1 << 2
    """Do not include any embeds when serializing this message."""

    SOURCE_MESSAGE_DELETED = 1 << 3
    """The source message for this crosspost has been deleted (via Channel Following)."""

    URGENT = 1 << 4
    """This message came from the urgent message system."""

    HAS_THREAD = 1 << 5
    """This message is part of a thread."""

    EPHEMERAL = 1 << 6
    """This message is ephemeral and only visible to the user who invoked the Interaction."""

    LOADING = 1 << 7
    """This message is an Interaction Response and the bot is 'thinking'."""

    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8
    """This message failed to mention some roles and add their members to the thread."""

    SUPPRESS_NOTIFICATIONS = 1 << 12
    """This message will not trigger push and desktop notifications"""

    IS_VOICE_MESSAGE = 1 << 13
    """This message is a voice message"""


@enum.unique
class AttachmentFlags(enum.IntFlag):
    """Attachment flags.

    Reference:
    https://discord.com/developers/docs/resources/channel#attachment-object-attachment-flags
    """

    IS_REMIX = 1 << 2
    """This attachment has been edited using the remix feature on mobile"""


class AttachmentData(BaseModel):
    """Attachment object used for creating and editing messages.

    Reference:
    https://discord.com/developers/docs/resources/channel#attachment-object
    """

    id: Snowflake | int | None = None
    """Attachment ID."""

    filename: str | None = None
    """Name of the attached file."""

    description: str | None = Field(None, max_length=1024)
    """Description for the file (max 1024 characters)."""

    content_type: str | None = None
    """Media type of the file."""

    size: int | None = None
    """Size of the file in bytes."""

    url: str | None = None
    """Source URL of the file."""

    proxy_url: str | None = None
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
    """Duration of the audio file (currently for voice messages)"""

    waveform: str | None = None
    """base64 encoded bytearray representing a sampled waveform.
    
    Currently for voice messages
    """

    flags: AttachmentFlags | None = None
    """Attachment flags combined as a bitfield"""


class BaseMessageData(BaseModel):
    """Base message data class used for message creation and editing.

    Contains axillary validation methods.
    """

    @model_validator(mode='before')
    def has_any_content(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate message content.

        Reference:
        https://discord.com/developers/docs/resources/channel#message-object-message-structure

        Args:
            values: Values to validate.

        Returns:
            Validated values.

        Raises:
            ValueError: If the message has no content or embeds.
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

        Reference:
        https://discord.com/developers/docs/resources/channel#message-object-message-structure

        Args:
            embeds: Values to validate.

        Raises:
            ValueError: If the total embed text length is more than 6000 characters.

        Returns:
            Validated values.
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
    def validate_attached_files(cls, files: _FilesType) -> list[AttachedFile]:
        """Prepare attached files.

        Args:
            files: Files to prepare.

        Returns:
            Prepared files to attach.
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
                case str() | Path() as filename, content if isinstance(content, _AttachmentContentType):
                    if isinstance(filename, Path):
                        filename = filename.name
                    prepared_files.append(
                        AttachedFile(filename=filename, content=content),
                    )

                case _:
                    raise ValueError('Invalid file object type')

        return prepared_files

    @field_validator('attachments', check_fields=False)
    def validate_attachments(cls, attachments: list[AttachmentData] | None) -> list[AttachmentData] | None:
        """Validate attachments.

        Args:
            attachments: Attachments to validate.

        Raises:
            ValueError: If attachments have mixed ids.

        Returns:
            Validated attachments.
        """
        if not attachments:
            return attachments

        attachment_id_exist_list = [attach.id is not None for attach in attachments]

        if all(attachment_id_exist_list):
            # Check is disabled because updated attachments already have id generated by Discord.
            # It means that after creating message with attachments all attachments will have Snowflake id.

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
            components: Components to validate.

        Raises:
            ValueError: If components have more than 5 action rows.

        Returns:
            Validated components.
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

        # allow 5 action rows per message
        if action_row_count > 5:  # noqa: PLR2004
            raise ValueError('ActionRow components must be less than 5')

        return components

    @classmethod
    def _embed_text_length(cls, embed: Embed) -> int:
        """Get the length of the embed text.

        Args:
            embed: Embed to get the length of.

        Returns:
            Length of the embed text.
        """
        embed_text_length = len(embed.title or '')
        embed_text_length += len(embed.description or '')

        if embed.footer:
            embed_text_length += len(embed.footer.text)

        if embed.author:
            embed_text_length += len(embed.author.name)

        for field in embed.fields:
            embed_text_length += len(field.name)
            embed_text_length += len(field.value)

        return embed_text_length


@enum.unique
class AllowedMentionType(enum.Enum):
    """Type of allowed mention.

    Reference:
    https://discord.com/developers/docs/resources/channel#allowed-mentions-object-allowed-mention-types
    """

    ROLES = 'roles'
    """Controls role mentions."""

    USERS = 'users'
    """Controls user mentions."""

    EVERYONE = 'everyone'
    """Controls @everyone and @here mentions."""


class AllowedMentions(BaseModel):
    """Allowed mentions object.

    Reference:
    https://discord.com/developers/docs/resources/channel#allowed-mentions-object
    """

    parse: list[AllowedMentionType] | None = None
    """Array of allowed mention types to parse from the content."""

    roles: list[Snowflake] | None = Field(None, max_length=100)
    """Array of role IDs to mention."""

    users: list[Snowflake] | None = Field(None, max_length=100)
    """Array of user IDs to mention."""

    replied_user: bool | None = None
    """For replies, whether to mention the author of the message being replied to."""


class MessageReference(BaseModel):
    """Message reference object.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-reference-object
    """

    message_id: Snowflake | None = None
    """ID of the originating message."""

    channel_id: Snowflake | None = None
    """ID of the originating message's channel."""

    guild_id: Snowflake | None = None
    """ID of the originating message's guild."""

    fail_if_not_exists: bool | None = None
    """Flag to tell the API to return an error object instead.

    When sending a message that references another message, this field determines
    whether to error if the referenced message doesn't exist instead of sending
    the message as a normal (non-reply) message.

    If None is set, the default serverside value is True.
    """


@enum.unique
class InteractionType(enum.IntEnum):
    """Type of interaction.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-type
    """

    # TODO: #16 move to interactions module (Now it is here because of circular imports)

    PING = 1
    """Ping interaction."""

    APPLICATION_COMMAND = 2
    """Slash command."""

    MESSAGE_COMPONENT = 3
    """Message component."""

    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    """Autocomplete command."""

    MODAL_SUBMIT = 5
    """Modal submit."""


class MessageInteraction(BaseModel):
    """Message interaction object.

    This is sent on the message object when the message is a response to
    an Interaction without an existing message.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#message-interaction-object
    """

    id: Snowflake
    """ID of the interaction."""

    type: InteractionType
    """Type of interaction."""

    name: str
    """Name of the application command, including subcommands and subcommand groups."""

    user: UserOutput
    """User who invoked the interaction."""

    member: MemberOutput | None = None
    """Member who invoked the interaction."""


class CreateMessageData(BaseMessageData):
    """Data to create a message with.

    Reference:
    https://discord.com/developers/docs/resources/channel#create-message
    """

    content: str | None = Field(None, max_length=2000)
    """Message content."""

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

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS, MessageFlags.SUPPRESS_NOTIFICATIONS] | None = None
    """The flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """


class UpdateMessageData(BaseMessageData):
    """The data to update a message with.

    Reference:
    https://discord.com/developers/docs/resources/channel#edit-message
    """

    content: str | None = Field(None, max_length=2000)
    """Message content."""

    embeds: list[Embed] | None = None
    """Embedded rich content."""

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS] | None = None
    """Flags to use when sending the message.

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

    Reference:
    https://discord.com/developers/docs/resources/channel#attachment-object
    """

    id: Snowflake
    """Attachment id."""

    filename: str
    """Name of file attached."""

    description: str | None = Field(None, max_length=1024)
    """Description for the file (max 1024 characters)."""

    content_type: str | None = None
    """Media type of the file."""

    size: int
    """Size of file in bytes."""

    url: str
    """Source url of file"""

    proxy_url: str
    """Proxied url of file."""

    height: int | None = None
    """Height of file (if image)."""

    width: int | None = None
    """Width of file (if image)."""

    ephemeral: bool | None = None
    """Whether this attachment is ephemeral.

    Ephemeral attachments will automatically be removed after a set period of time.
    Ephemeral attachments on messages are guaranteed to be available as long as
    the message itself exists.
    """

    duration_secs: float | None = None
    """Duration of the audio file (currently for voice messages)"""

    waveform: str | None = None
    """base64 encoded bytearray representing a sampled waveform.
    
    Currently for voice messages
    """

    flags: AttachmentFlags | None = None
    """Attachment flags combined as a bitfield"""


class ReactionCountDetails(BaseModel):
    """Reaction Count Details object.

    The reaction count details object contains
    a breakdown of normal and super reaction counts for the associated emoji.
    """
    burst: int
    """Count of super reactions"""

    normal: int
    """Count of normal reactions"""


class Reaction(BaseModel):
    """Reaction object.

    Reference:
    https://discord.com/developers/docs/resources/channel#reaction-object
    """

    count: int
    """Times this emoji has been used to react."""

    count_details: ReactionCountDetails

    me: bool
    """Whether the current user reacted using this emoji."""

    me_burst: bool
    """Whether the current user super-reacted using this emoji"""

    emoji: Emoji
    """Emoji information."""

    burst_colors: list[Color]
    """HEX colors used for super reaction"""


@enum.unique
class MessageType(enum.IntEnum):
    """Type of message.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-object-message-types
    """

    DEFAULT = 0
    """Default message."""

    RECIPIENT_ADD = 1
    """Recipient was added to a group DM."""

    RECIPIENT_REMOVE = 2
    """Recipient was removed from a group DM."""

    CALL = 3
    """Call was started in the channel."""

    CHANNEL_NAME_CHANGE = 4
    """Channel name was changed."""

    CHANNEL_ICON_CHANGE = 5
    """Channel icon was changed."""

    CHANNEL_PINNED_MESSAGE = 6
    """Message was pinned."""

    USER_JOIN = 7
    """User joined the guild."""

    GUILD_BOOST = 8
    """User started boosting the guild."""

    GUILD_BOOST_TIER_1 = 9
    """User boosted the guild to tier 1."""

    GUILD_BOOST_TIER_2 = 10
    """User boosted the guild to tier 2."""

    GUILD_BOOST_TIER_3 = 11
    """User boosted the guild to tier 3."""

    CHANNEL_FOLLOW_ADD = 12
    """Channel was followed into a news channel."""

    GUILD_DISCOVERY_DISQUALIFIED = 14
    """Guild discovery disqualification occurred."""

    GUILD_DISCOVERY_REQUALIFIED = 15
    """Guild discovery requalification occurred."""

    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    """Guild discovery grace period initial warning occurred."""

    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    """Guild discovery grace period final warning occurred."""

    THREAD_CREATED = 18
    """Thread was created."""

    REPLY = 19
    """Reply to another message."""

    CHAT_INPUT_COMMAND = 20
    """Message sent in response to an Interaction."""

    THREAD_STARTER_MESSAGE = 21
    """Message in a thread was published to the parent channel."""

    GUILD_INVITE_REMINDER = 22
    """Thread was created from an announcement message with the `HAS_THREAD` flag."""

    CONTEXT_MENU_COMMAND = 23
    """Context menu command was used."""

    AUTO_MODERATION_ACTION = 24
    """Auto moderation action was taken."""

    ROLE_SUBSCRIPTION_PURCHASE = 25
    """User purchased a Nitro subscription."""

    INTERACTION_PREMIUM_UPSELL = 26
    """User has upgraded their guild subscription."""

    STAGE_START = 27
    """Represents start of a stage in a voice channel."""

    STAGE_END = 28
    """Represents end of a stage in a voice channel."""

    STAGE_SPEAKER = 29
    """Represents speaker in a stage in a voice channel."""

    STAGE_TOPIC = 31
    """Represents topic change in a stage in a voice channel."""

    GUILD_APPLICATION_PREMIUM_SUBSCRIPTION = 32
    """Guild application premium subscription."""


class MessageActivityType(enum.IntEnum):
    """Type of activity.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-object-message-activity-types
    """

    JOIN = 1
    """Join a party."""

    SPECTATE = 2
    """Spectate a game."""

    LISTEN = 3
    """Listen along to a song."""

    JOIN_REQUEST = 5
    """Join a request to play a game."""


class MessageActivity(BaseModel):
    """Message activity object.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-object-message-activity-structure
    """

    type: MessageActivityType
    """Type of message activity."""

    party_id: str | None = None
    """Party ID from a Rich Presence event."""


# FIXME: It's AI guess, need to be tested
class MessageApplication(BaseModel):
    """Message application object."""

    id: Snowflake
    """ID of the application"""

    cover_image: str | None = None
    """ID of the embed's image asset"""

    description: str
    """Application's description"""

    icon: str | None = None
    """ID of the application's icon"""

    name: str
    """Name of the application"""


class MessageStickerItem(BaseModel):
    """Smallest amount of data required to render a sticker.

    Partial sticker object.

    Reference:
    https://discord.com/developers/docs/resources/sticker#sticker-item-object
    """

    id: Snowflake
    """id of the sticker."""

    name: str
    """Name of the sticker."""

    format_type: StickerFormatType
    """type of sticker format"""


class RoleSubscriptionData(BaseModel):
    """Role Subscription Data Object

    Reference:
    https://discord.com/developers/docs/resources/channel#role-subscription-data-object
    """

    role_subscription_listing_id: Snowflake
    """the id of the sku and listing that the user is subscribed to"""

    tier_name: str
    """name of the tier that the user is subscribed to."""

    total_months_subscribed: int
    """cumulative number of months that the user has been subscribed for."""

    is_renewal: bool
    """whether this notification is for a renewal rather than a new purchase"""


class Message(BaseModel):
    """Message object.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-object
    """

    id: Snowflake
    """ID of the message."""

    channel_id: Snowflake
    """ID of the channel the message was sent in."""

    author: UserOutput
    """Author of the message."""

    content: str
    """Contents of the message."""

    timestamp: datetime.datetime
    """When this message was sent."""

    edited_timestamp: datetime.datetime | None = None
    """When this message was edited (or null if never)."""

    tts: bool
    """Whether this was a TTS message."""

    mention_everyone: bool
    """Whether this message mentions everyone."""

    mentions: list[UserOutput]
    """Users specifically mentioned in the message."""

    mention_roles: list[Snowflake]
    """Roles specifically mentioned in this message."""

    mention_channels: list[ChannelMention] | None = None
    """Channels specifically mentioned in this message."""

    attachments: list[Attachment]
    """Any attached files."""

    embeds: list[Embed]
    """Any embedded content."""

    reactions: list[Reaction] | None = None
    """Any reactions to the message."""

    nonce: int | str | None = None
    """Used for validating a message was sent."""

    pinned: bool
    """Whether this message is pinned."""

    webhook_id: Snowflake | None = None
    """If the message is generated by a webhook, this is the webhook's id."""

    type: MessageType
    """Type of message."""

    activity: MessageActivity | None = None
    """Sent with Rich Presence-related chat embeds."""

    application: MessageApplication | None = None
    """Sent with Rich Presence-related chat embeds."""

    application_id: Snowflake | None = None
    """If the message is an Interaction or application-owned webhook.

    This is the id of the application.
    """

    message_reference: MessageReference | None = None
    """Reference data sent with crossposted messages."""

    flags: MessageFlags
    """Message flags combined as a bitfield."""

    referenced_message: Message | None = None
    """The message this message references, if the message is a reply."""

    interaction: MessageInteraction | None = None
    """Sent if the message is a response to an Interaction."""

    thread: ChannelOutput | None = None
    """The thread that was started from this message, includes thread member object."""

    components: list[Component] | None = None
    """Sent if the message is a response to an Interaction."""

    sticker_items: list[MessageStickerItem] | None = None
    """Sent if the message contains stickers"""

    position: int | None = None
    """Generally increasing integer (there may be gaps or duplicates)
     
    Represents the approximate position of the message in a thread,
    it can be used to estimate the relative position of the message in a thread
    in company with total_message_sent on parent thread
    """

    role_subscription_data: RoleSubscriptionData | None = None
    """Data of the role subscription purchase or renewal.
    
    that prompted this ROLE_SUBSCRIPTION_PURCHASE message
    """

    # TODO: resolved needs a model
    # https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-resolved-data-structure
    resolved: dict[str, Any] | None = None
    """data for users, members, channels, and roles.
     
    In the message's auto-populated select menus.
    """
