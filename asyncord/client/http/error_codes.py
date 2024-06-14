"""List of error codes returned by Discord API."""

import enum

from fbenum.enum import FallbackEnum


@enum.unique
class ErrorCode(enum.IntEnum, FallbackEnum):
    """Error codes returned by Discord API.

    Reference:
    https://discord.com/developers/docs/topics/opcodes-and-status-codes#json-json-error-codes
    """

    GENERAL_ERROR = 0
    """General error (such as a malformed request body, amongst other things)."""

    UNKNOWN_ACCOUNT = 10001
    """Unknown account."""

    UNKNOWN_APPLICATION = 10002
    """Unknown application."""

    UNKNOWN_CHANNEL = 10003
    """Unknown channel."""

    UNKNOWN_GUILD = 10004
    """Unknown guild."""

    UNKNOWN_INTEGRATION = 10005
    """Unknown integration."""

    UNKNOWN_INVITE = 10006
    """Unknown invite."""

    UNKNOWN_MEMBER = 10007
    """Unknown member."""

    UNKNOWN_MESSAGE = 10008
    """Unknown message."""

    UNKNOWN_PERMISSION_OVERWRITE = 10009
    """Unknown permission overwrite."""

    UNKNOWN_PROVIDER = 10010
    """Unknown provider."""

    UNKNOWN_ROLE = 10011
    """Unknown role."""

    UNKNOWN_TOKEN = 10012
    """Unknown token."""

    UNKNOWN_USER = 10013
    """Unknown user."""

    UNKNOWN_EMOJI = 10014
    """Unknown emoji."""

    UNKNOWN_WEBHOOK = 10015
    """Unknown webhook."""

    UNKNOWN_WEBHOOK_SERVICE = 10016
    """Unknown webhook service."""

    UNKNOWN_SESSION = 10020
    """Unknown session."""

    UNKNOWN_BAN = 10026
    """Unknown ban."""

    UNKNOWN_SKU = 10027
    """Unknown SKU."""

    UNKNOWN_STORE_LISTING = 10028
    """Unknown Store Listing."""

    UNKNOWN_ENTITLEMENT = 10029
    """Unknown entitlement."""

    UNKNOWN_BUILD = 10030
    """Unknown build."""

    UNKNOWN_LOBBY = 10031
    """Unknown lobby."""

    UNKNOWN_BRANCH = 10032
    """Unknown branch."""

    UNKNOWN_STORE_DIRECTORY_LAYOUT = 10033
    """Unknown store directory layout."""

    UNKNOWN_REDISTRIBUTABLE = 10036
    """Unknown redistributable."""

    UNKNOWN_GIFT_CODE = 10038
    """Unknown gift code."""

    UNKNOWN_STREAM = 10049
    """Unknown stream."""

    UNKNOWN_PREMIUM_SERVER_SUBSCRIBE_COOLDOWN = 10050
    """Unknown premium server subscribe cooldown."""

    UNKNOWN_GUILD_TEMPLATE = 10057
    """Unknown guild template."""

    UNKNOWN_DISCOVERABLE_SERVER_CATEGORY = 10059
    """Unknown discoverable server category."""

    UNKNOWN_STICKER = 10060
    """Unknown sticker."""

    UNKNOWN_INTERACTION = 10062
    """Unknown interaction."""

    UNKNOWN_APPLICATION_COMMAND = 10063
    """Unknown application command."""

    UNKNOWN_VOICE_STATE = 10065
    """Unknown voice state."""

    UNKNOWN_APPLICATION_COMMAND_PERMISSIONS = 10066
    """Unknown application command permissions."""

    UNKNOWN_STAGE_INSTANCE = 10067
    """Unknown Stage Instance."""

    UNKNOWN_GUILD_MEMBER_VERIFICATION_FORM = 10068
    """Unknown Guild Member Verification Form."""

    UNKNOWN_GUILD_WELCOME_SCREEN = 10069
    """Unknown Guild Welcome Screen."""

    UNKNOWN_GUILD_SCHEDULED_EVENT = 10070
    """Unknown Guild Scheduled Event."""

    UNKNOWN_GUILD_SCHEDULED_EVENT_USER = 10071
    """Unknown Guild Scheduled Event User."""

    UNKNOWN_TAG = 10087
    """Unknown Tag."""

    BOTS_CANNOT_USE_THIS_ENDPOINT = 20001
    """Bots cannot use this endpoint."""

    ONLY_BOTS_CAN_USE_THIS_ENDPOINT = 20002
    """Only bots can use this endpoint."""

    EXPLICIT_CONTENT_CANNOT_BE_SENT = 20009
    """Explicit content cannot be sent to the desired recipient(s)."""

    ACTION_NOT_AUTHORIZED = 20012
    """You are not authorized to perform this action on this application."""

    ACTION_RATE_LIMITED_SLOWMODE = 20016
    """This action cannot be performed due to slowmode rate limit."""

    ACTION_OWNER_ONLY = 20018
    """Only the owner of this account can perform this action."""

    ACTION_ANNOUNCEMENT_RATE_LIMIT = 20022
    """This message cannot be edited due to announcement rate limits."""

    UNDER_MINIMUM_AGE = 20024
    """Under minimum age."""

    WRITE_RATE_LIMIT_CHANNEL = 20028
    """The channel you are writing has hit the write rate limit."""

    WRITE_RATE_LIMIT_SERVER = 20029
    """The write action you are performing on the server has hit the write rate limit."""

    INVALID_WORDS_IN_STAGE_TOPIC = 20031
    """Your Stage topic, server name, server description, or channel names contain words that are not allowed."""

    GUILD_PREMIUM_SUBSCRIPTION_LEVEL_TOO_LOW = 20035
    """Guild premium subscription level too low."""

    MAX_GUILDS_REACHED = 30001
    """Maximum number of guilds reached (100)."""

    MAX_FRIENDS_REACHED = 30002
    """Maximum number of friends reached (1000)."""

    MAX_PINS_REACHED_FOR_CHANNEL = 30003
    """Maximum number of pins reached for the channel (50)."""

    MAX_RECIPIENTS_REACHED = 30004
    """Maximum number of recipients reached (10)."""

    MAX_GUILD_ROLES_REACHED = 30005
    """Maximum number of guild roles reached (250)."""

    MAX_WEBHOOKS_REACHED = 30007
    """Maximum number of webhooks reached (15)."""

    MAX_EMOJIS_REACHED = 30008
    """Maximum number of emojis reached."""

    MAX_REACTIONS_REACHED = 30010
    """Maximum number of reactions reached (20)."""

    MAX_GROUP_DMS_REACHED = 30011
    """Maximum number of group DMs reached (10)."""

    MAX_GUILD_CHANNELS_REACHED = 30013
    """Maximum number of guild channels reached (500)."""

    MAX_ATTACHMENTS_IN_MESSAGE_REACHED = 30015
    """Maximum number of attachments in a message reached (10)."""

    MAX_INVITES_REACHED = 30016
    """Maximum number of invites reached (1000)."""

    MAX_ANIMATED_EMOJIS_REACHED = 30018
    """Maximum number of animated emojis reached."""

    MAX_SERVER_MEMBERS_REACHED = 30019
    """Maximum number of server members reached."""

    MAX_SERVER_CATEGORIES_REACHED = 30030
    """Maximum number of server categories has been reached (5)."""

    GUILD_ALREADY_HAS_A_TEMPLATE = 30031
    """Guild already has a template."""

    MAX_APPLICATION_COMMANDS_REACHED = 30032
    """Maximum number of application commands reached."""

    MAX_THREAD_PARTICIPANTS_REACHED = 30033
    """Maximum number of thread participants has been reached (1000)."""

    MAX_DAILY_APPLICATION_COMMAND_CREATES_REACHED = 30034
    """Maximum number of daily application command creates has been reached (200)."""

    MAX_BANS_FOR_NON_GUILD_MEMBERS_EXCEEDED = 30035
    """Maximum number of bans for non-guild members have been exceeded."""

    MAX_BANS_FETCHES_REACHED = 30037
    """Maximum number of bans fetches has been reached."""

    MAX_UNCOMPLETED_GUILD_SCHEDULED_EVENTS_REACHED = 30038
    """Maximum number of uncompleted guild scheduled events reached (100)."""

    MAX_STICKERS_REACHED = 30039
    """Maximum number of stickers reached."""

    MAX_PRUNE_REQUESTS_REACHED = 30040
    """Maximum number of prune requests has been reached. Try again later."""

    MAX_GUILD_WIDGET_SETTINGS_UPDATES_REACHED = 30042
    """Maximum number of guild widget settings updates has been reached. Try again later."""

    MAX_EDITS_TO_MESSAGES_OLDER_THAN_1_HOUR_REACHED = 30046
    """Maximum number of edits to messages older than 1 hour reached. Try again later."""

    MAX_PINNED_THREADS_IN_A_FORUM_CHANNEL_REACHED = 30047
    """Maximum number of pinned threads in a forum channel has been reached."""

    MAX_TAGS_IN_A_FORUM_CHANNEL_REACHED = 30048
    """Maximum number of tags in a forum channel has been reached."""

    BITRATE_IS_TOO_HIGH_FOR_CHANNEL_OF_THIS_TYPE = 30052
    """Bitrate is too high for channel of this type."""

    MAX_PREMIUM_EMOJIS_REACHED = 30056
    """Maximum number of premium emojis reached (25)."""

    MAX_WEBHOOKS_PER_GUILD_REACHED = 30058
    """Maximum number of webhooks per guild reached (1000)."""

    MAX_CHANNEL_PERMISSION_OVERWRITES_REACHED = 30060
    """Maximum number of channel permission overwrites reached (1000)."""

    CHANNELS_FOR_GUILD_TOO_LARGE = 30061
    """The channels for this guild are too large."""

    UNAUTHORIZED = 40001
    """Unauthorized. Provide a valid token and try again."""

    ACCOUNT_VERIFICATION_REQUIRED = 40002
    """You need to verify your account in order to perform this action."""

    OPENING_DIRECT_MESSAGES_TOO_FAST = 40003
    """You are opening direct messages too fast."""

    SEND_MESSAGES_TEMPORARILY_DISABLED = 40004
    """Send messages has been temporarily disabled."""

    REQUEST_ENTITY_TOO_LARGE = 40005
    """Request entity too large. Try sending something smaller in size."""

    FEATURE_TEMPORARILY_DISABLED_SERVER_SIDE = 40006
    """This feature has been temporarily disabled server-side."""

    USER_BANNED_FROM_GUILD = 40007
    """The user is banned from this guild."""

    CONNECTION_REVOKED = 40012
    """Connection has been revoked."""

    TARGET_USER_NOT_CONNECTED_TO_VOICE = 40032
    """Target user is not connected to voice."""

    MESSAGE_ALREADY_CROSSPOSTED = 40033
    """This message has already been crossposted."""

    APPLICATION_COMMAND_ALREADY_EXISTS = 40041
    """An application command with that name already exists."""

    APPLICATION_INTERACTION_FAILED_TO_SEND = 40043
    """Application interaction failed to send."""

    CANNOT_SEND_MESSAGE_IN_FORUM_CHANNEL = 40058
    """Cannot send a message in a forum channel."""

    INTERACTION_ALREADY_ACKNOWLEDGED = 40060
    """Interaction has already been acknowledged."""

    TAG_NAMES_MUST_BE_UNIQUE = 40061
    """Tag names must be unique."""

    SERVICE_RESOURCE_RATE_LIMITED = 40062
    """Service resource is being rate limited."""

    NO_TAGS_AVAILABLE_FOR_NON_MODERATORS = 40066
    """There are no tags available that can be set by non-moderators."""

    TAG_REQUIRED_TO_CREATE_FORUM_POST = 40067
    """A tag is required to create a forum post in this channel."""

    ENTITLEMENT_ALREADY_GRANTED = 40074
    """An entitlement has already been granted for this resource."""

    MISSING_ACCESS = 50001
    """Missing access."""

    INVALID_ACCOUNT_TYPE = 50002
    """Invalid account type."""

    CANNOT_EXECUTE_ACTION_ON_DM_CHANNEL = 50003
    """Cannot execute action on a DM channel."""

    GUILD_WIDGET_DISABLED = 50004
    """Guild widget disabled."""

    CANNOT_EDIT_MESSAGE_AUTHORED_BY_ANOTHER_USER = 50005
    """Cannot edit a message authored by another user."""

    CANNOT_SEND_EMPTY_MESSAGE = 50006
    """Cannot send an empty message."""

    CANNOT_SEND_MESSAGES_TO_THIS_USER = 50007
    """Cannot send messages to this user."""

    CANNOT_SEND_MESSAGES_IN_NON_TEXT_CHANNEL = 50008
    """Cannot send messages in a non-text channel."""

    CHANNEL_VERIFICATION_LEVEL_TOO_HIGH = 50009
    """Channel verification level is too high for you to gain access."""

    OAUTH2_APPLICATION_DOES_NOT_HAVE_A_BOT = 50010
    """OAuth2 application does not have a bot."""

    OAUTH2_APPLICATION_LIMIT_REACHED = 50011
    """OAuth2 application limit reached."""

    INVALID_OAUTH2_STATE = 50012
    """Invalid OAuth2 state."""

    LACK_PERMISSIONS_TO_PERFORM_ACTION = 50013
    """You lack permissions to perform that action."""

    INVALID_AUTHENTICATION_TOKEN_PROVIDED = 50014
    """Invalid authentication token provided."""

    NOTE_TOO_LONG = 50015
    """Note was too long."""

    INVALID_MESSAGES_TO_DELETE = 50016
    """Provided too few or too many messages to delete.

    Must provide at least 2 and fewer than 100 messages to delete.
    """

    INVALID_MFA_LEVEL = 50017
    """Invalid MFA Level."""

    MESSAGE_CAN_ONLY_BE_PINNED_TO_CHANNEL_IT_WAS_SENT_IN = 50019
    """A message can only be pinned to the channel it was sent in."""

    INVALID_INVITE_CODE = 50020
    """Invite code was either invalid or take."""

    CANNOT_EXECUTE_ACTION_ON_SYSTEM_MESSAGE = 50021
    """Cannot execute action on a system message."""

    CANNOT_EXECUTE_ACTION_ON_THIS_CHANNEL_TYPE = 50024
    """Cannot execute action on this channel type."""

    INVALID_OAUTH2_ACCESS_TOKEN_PROVIDED = 50025
    """Invalid OAuth2 access token provided."""

    MISSING_REQUIRED_OAUTH2_SCOPE = 50026
    """Missing required OAuth2 scope."""

    INVALID_WEBHOOK_TOKEN_PROVIDED = 50027
    """Invalid webhook token provided."""

    INVALID_ROLE = 50028
    """Invalid role."""

    INVALID_RECIPIENTS = 50033
    """Invalid Recipient(s)."""

    MESSAGE_TOO_OLD_TO_BULK_DELETE = 50034
    """A message provided was too old to bulk delete."""

    INVALID_FORM_BODY = 50035
    """Invalid form body.

    Returned for both application/json and multipart/form-data bodies), or invalid Content-Type provided.
    """

    INVITE_ACCEPTED_TO_GUILD_BOT_NOT_IN = 50036
    """An invite was accepted to a guild the application's bot is not in."""

    INVALID_ACTIVITY_ACTION = 50039
    """Invalid Activity Action."""

    INVALID_API_VERSION_PROVIDED = 50041
    """Invalid API version provided."""

    FILE_UPLOADED_EXCEEDS_MAXIMUM_SIZE = 50045
    """File uploaded exceeds the maximum size."""

    INVALID_FILE_UPLOADED = 50046
    """Invalid file uploade."""

    CANNOT_SELF_REDEEM_GIFT = 50054
    """Cannot self-redeem this gift."""

    INVALID_GUILD = 50055
    """Invalid Guild."""

    INVALID_SKU = 50057
    """Invalid SKU."""

    INVALID_REQUEST_ORIGIN = 50067
    """Invalid request origin."""

    INVALID_MESSAGE_TYPE = 50068
    """Invalid message type."""

    PAYMENT_SOURCE_REQUIRED_TO_REDEEM_GIFT = 50070
    """Payment source required to redeem gift."""

    CANNOT_MODIFY_SYSTEM_WEBHOOK = 50073
    """Cannot modify a system webhook."""

    CANNOT_DELETE_CHANNEL_REQUIRED_FOR_COMMUNITY_GUILDS = 50074
    """Cannot delete a channel required for Community guilds."""

    CANNOT_EDIT_STICKERS_WITHIN_MESSAGE = 50080
    """Cannot edit stickers within a message."""

    INVALID_STICKER_SENT = 50081
    """Invalid sticker sent."""

    CANNOT_PERFORM_OPERATION_ON_ARCHIVED_THREAD = 50083
    """Tried to perform an operation on an archived thread.

    Such as editing a message or adding a user to the thread.
    """

    INVALID_THREAD_NOTIFICATION_SETTINGS = 50084
    """Invalid thread notification settings."""

    BEFORE_VALUE_EARLIER_THAN_THREAD_CREATION_DATE = 50085
    """before value is earlier than the thread creation date."""

    COMMUNITY_SERVER_CHANNELS_MUST_BE_TEXT_CHANNELS = 50086
    """Community server channels must be text channels."""

    ENTITY_TYPE_OF_EVENT_DIFFERENT_FROM_ENTITY = 50091
    """The entity type of the event is different from the entity you are trying to start the event for."""

    SERVER_NOT_AVAILABLE_IN_LOCATION = 50095
    """This server is not available in your location."""

    MONETIZATION_REQUIRED_TO_PERFORM_ACTION = 50097
    """This server needs monetization enabled in order to perform this action."""

    MORE_BOOSTS_REQUIRED_TO_PERFORM_ACTION = 50101
    """This server needs more boosts to perform this action."""

    INVALID_JSON_REQUEST_BODY = 50109
    """The request body contains invalid JSON."""

    OWNER_CANNOT_BE_PENDING_MEMBER = 50131
    """Owner cannot be pending member."""

    OWNERSHIP_CANNOT_BE_TRANSFERRED_TO_BOT_USER = 50132
    """Ownership cannot be transferred to a bot user."""

    FAILED_TO_RESIZE_ASSET_BELOW_MAXIMUM_SIZE = 50138
    """Failed to resize asset below the maximum size 262144."""

    CANNOT_MIX_SUBSCRIPTION_AND_NON_SUBSCRIPTION_ROLES_FOR_EMOJI = 50144
    """Cannot mix subscription and non subscription roles for an emoji."""

    CANNOT_CONVERT_BETWEEN_PREMIUM_AND_NORMAL_EMOJI = 50145
    """Cannot convert between premium emoji and normal emoji."""

    UPLOADED_FILE_NOT_FOUND = 50146
    """Uploaded file not found."""

    VOICE_MESSAGES_DO_NOT_SUPPORT_ADDITIONAL_CONTENT = 50159
    """Voice messages do not support additional content."""

    VOICE_MESSAGES_MUST_HAVE_SINGLE_AUDIO_ATTACHMENT = 50160
    """Voice messages must have a single audio attachment."""

    VOICE_MESSAGES_MUST_HAVE_SUPPORTING_METADATA = 50161
    """Voice messages must have supporting metadata."""

    VOICE_MESSAGES_CANNOT_BE_EDITED = 50162
    """Voice messages cannot be edited."""

    CANNOT_DELETE_GUILD_SUBSCRIPTION_INTEGRATION = 50163
    """Cannot delete guild subscription integration"""

    CANNOT_SEND_VOICE_MESSAGES_IN_CHANNEL = 50173
    """You cannot send voice messages in this channel."""

    USER_ACCOUNT_MUST_BE_VERIFIED = 50178
    """The user account must first be verified"""

    YOU_DO_NOT_HAVE_PERMISSION_TO_SEND_THIS_STICKER = 50600
    """You do not have permission to send this sticker."""
