from __future__ import annotations

import enum
import datetime
from typing import Literal

from pydantic import Field, BaseModel, root_validator

from asyncord.snowflake import Snowflake
from asyncord.client.models.emoji import Emoji
from asyncord.client.models.users import User
from asyncord.client.models.members import Member
from asyncord.client.models.channels import Channel, ChannelMention
from asyncord.client.models.stickers import Sticker


@enum.unique
class MessageFlags(enum.IntFlag):
    """Message flags.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#message-object-message-flags
    """
    CROSSPOSTED = 1 << 0
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


class _MessageData(BaseModel):
    @root_validator
    def check_total_embed_text_length(cls, values):
        """Check total embed text length.

        Read more info at:
        https://discord.com/developers/docs/resources/channel#message-object-message-structure
        """
        embeds: list[Embed] = values.get('embeds') or []

        total_embed_text_length = 0
        for embed in embeds:
            total_embed_text_length += len(embed.title or '')
            total_embed_text_length += len(embed.description or '')

            if embed.footer:
                total_embed_text_length += len(embed.footer.text or '')

            if embed.author:
                total_embed_text_length += len(embed.author.name or '')

            if embed.fields:
                for field in embed.fields:
                    total_embed_text_length += len(field.name or '')
                    total_embed_text_length += len(field.value or '')

            if total_embed_text_length > 6000:
                raise ValueError('Total embed text length must be less than 6000 characters.')

        return values

    @root_validator
    def has_content_or_embeds(cls, values):
        """Check if the message has content or embeds.

        Read more info at:
        https://discord.com/developers/docs/resources/channel#message-object-message-structure
        """
        has_any_content = bool(
            values.get('content', False)
            or values.get('embeds', False)
            or values.get('sticker_ids', False)
            or values.get('components', False)
            # or values.get('files[n]', False) # FIXME: activate when attachments are implemented
        )

        if not has_any_content:
            raise ValueError('Message must have content, embeds, stickers or components.')

        return values


class CreateMessageData(_MessageData):
    """The data to create a message with.

    More info at: https://discord.com/developers/docs/resources/channel#create-message
    """

    content: str | None = Field(None, max_length=2000)
    """The message content."""

    nonce: str | int | None = Field(None, max_length=25)
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

    components: list[MessageComponent] | None = None
    """Components to include with the message."""

    sticker_ids: list[Snowflake] | None = None
    """Sticker ids to include with the message."""

    # FIXME: add attachments

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS] | None = None
    """The flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """


class UpdateMessageData(_MessageData):
    """The data to update a message with.

    More info at: https://discord.com/developers/docs/resources/channel#edit-message-json-params
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

    # FIXME: add attachments
    components: list[MessageComponent] | None = None
    """Components to include with the message."""

    sticker_ids: list[Snowflake] | None = None
    """Sticker ids to include with the message."""


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

    components: list[MessageComponent] | None = None
    """sent if the message is a response to an Interaction"""

    interaction: MessageInteraction | None = None
    """sent if the message is a response to an Interaction"""

    message: str | None = None
    """error message"""


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


class Attachment(BaseModel):
    """Attachment object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#attachment-object
    """
    id: Snowflake
    """attachment id"""

    filename: str
    """name of file attached"""

    description: str | None = Field(None, max_length=1024)
    """description for the file (max 1024 characters)"""

    content_type: str | None = None
    """the media type of the file"""

    size: int
    """size of file in bytes"""

    url: str
    """source url of file"""

    proxy_url: str
    """a proxied url of file"""

    height: int | None = None
    """height of file (if image)"""

    width: int | None = None
    """width of file (if image)"""

    ephemeral: bool | None = None
    """whether this attachment is ephemeral

    Ephemeral attachments will automatically be removed after a set period of time.
    Ephemeral attachments on messages are guaranteed to be available as long as
    the message itself exists.
    """


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

    # FIXME= Field(None, max_items=25) doesn't work On field "fields"
    # the following field constraints are set but not enforced: max_items.
    fields: list[EmbedField] | None = None
    """fields information"""


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

    RICH = "rich"
    """generic embed rendered from embed attributes"""

    IMAGE = "image"
    """image embed"""

    VIDEO = "video"
    """video embed"""

    GIFV = "gifv"
    """animated gif image embed rendered as a video embed"""

    ARTICLE = "article"
    """article embed"""

    LINK = "link"
    """link embed"""


class EmbedFooter(BaseModel):
    """Embed footer object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-footer-structure
    """
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
    name: str = Field(max_length=256)
    """name of the field"""

    value: str = Field(max_length=1024)
    """value of the field"""

    inline: bool | None = None
    """whether or not this field should display inline"""


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


class MessageActivity(BaseModel):
    """Message activity object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#message-object-message-activity-structure
    """
    type: MessageActivityType
    """type of message activity"""

    party_id: str | None = None
    """party_id from a Rich Presence event"""


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


@enum.unique
class AllowedMentionType(enum.Enum):
    """Type of allowed mention.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#allowed-mentions-object-allowed-mention-types
    """
    ROLES = "roles"
    """Controls role mentions."""

    USERS = "users"
    """Controls user mentions."""

    EVERYONE = "everyone"
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


class MessageComponent(BaseModel):
    """Message component object.

    Read more info at:
    https://discord.com/developers/docs/interactions/message-components#component-object
    """
    type: ComponentType
    """type of component"""

    style: ComponentStyle | None = None
    """style of the button"""

    label: str | None = None
    """text that appears on the button, max 80 characters"""

    emoji: PartialEmoji | None = None
    """emoji to display on the button"""

    custom_id: str | None = None
    """a developer-defined identifier for the button, max 100 characters"""

    url: str | None = None
    """a url for link-style buttons"""

    disabled: bool | None = None
    """whether the button is disabled"""

    components: list[MessageComponent] | None = None
    """a list of child components"""

    placeholder: str | None = None
    """custom placeholder text if nothing is selected, max 100 characters"""

    min_values: int | None = None
    """the minimum number of items that must be chosen; default 1, min 0, max 25"""

    max_values: int | None = None
    """the maximum number of items that can be chosen; default 1, max 25"""

    options: list[SelectOption] | None = None
    """the options in the select, max 25"""

    channel_id: Snowflake | None = None
    """the id of the channel to send the message to"""

    message_id: Snowflake | None = None
    """the id of the message to send the message to"""

    message: str | None = None
    """the message to send"""

    target: str | None = None
    """the target to send the message to"""


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


Message.update_forward_refs()
Embed.update_forward_refs()
MessageInteraction.update_forward_refs()
