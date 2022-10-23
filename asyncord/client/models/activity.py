from __future__ import annotations

import enum

from pydantic import Field, BaseModel

from asyncord.snowflake import Snowflake


class Activity(BaseModel):
    """https://discord.com/developers/docs/topics/gateway#activity-object

    Bots are only able to send name, type, and optionally url.
    """

    name: str
    """the activity's name"""

    type: ActivityType
    """activity type"""

    url: str | None = None
    """stream url, is validated when type is `ActivityType.STREAMING`

    Currently only supports Twitch and YouTube.
    Only https://twitch.tv/ and https://youtube.com/ urls will work
    """

    created_at: int | None = None
    """unix timestamp of when the activity was added to the user's session"""

    timestamps: ActivityTimestamps | None = None
    """unix timestamps for start and/or end of the game"""

    application_id: Snowflake | None = None
    """application id for the game"""

    details: str | None = None
    """what the player is currently doing"""

    state: str | None = None
    """the user's current party status"""

    emoji: ActivityEmoji | None = None
    """emoji data for custom statuses"""

    party: ActivityParty | None = None
    """information for the current party of the player"""

    assets: ActivityAssets | None = None
    """images for the presence and their hover texts"""

    secrets: ActivitySecrets | None = None
    """secrets for Rich Presence joining and spectating"""

    instance: bool | None = None
    """whether or not the activity is an instanced game session"""

    flags: ActivityFlag | None = None
    """activity flags ORd together, describes what the payload includes"""

    buttons: list[ActivityButton] | None = None


@enum.unique
class ActivityType(enum.IntEnum):
    """https://discord.com/developers/docs/topics/gateway#activity-object-activity-types"""

    GAME = 0
    """Playing {name}

    Example:
        `Playing Rocket League`
    """

    STREAMING = 1
    """Streaming {details}

    Example:
        `Streaming Rocket League`
    """

    LISTENING = 2
    """Listening to {name}

    Example:
        `Listening to Spotify`
    """
    WATCHING = 3
    """Watching {name}

    Example:
        `Watching YouTube Together`
    """

    CUSTOM = 4
    """{emoji} {name}

    Example:
        `:smile: I'm happy`
    """

    COMPETING = 5
    """Competing in {name}

    Example:
        `Competing in Arena World Champions`
    """


class ActivityTimestamps(BaseModel):
    """https://discord.com/developers/docs/topics/gateway#activity-object-activity-timestamps"""

    start: int | None = None
    """unix time (in milliseconds) of when the activity started"""

    end: int | None = None
    """unix time (in milliseconds) of when the activity ends"""


class ActivityEmoji(BaseModel):
    """https://discord.com/developers/docs/topics/gateway#activity-object-activity-emoji"""

    id: Snowflake | None = None
    """the id of the emoji"""

    name: str
    """the name of the emoji"""

    animated: bool | None = None
    """whether this emoji is animated"""


class ActivityParty(BaseModel):
    """https://discord.com/developers/docs/topics/gateway#activity-object-activity-party"""

    id: str | None = None
    """the id of the party"""

    size: tuple[int, int] | None = None
    """used to show the party's current and maximum size"""


class ActivityAssets(BaseModel):
    """https://discord.com/developers/docs/topics/gateway#activity-object-activity-assets"""

    # FIXME: Posible add support for large_image_text and small_image_text validation
    # https://discord.com/developers/docs/topics/gateway#activity-object-activity-asset-image

    large_image: str | None = None
    """the id for a large asset of the activity, usually a snowflake"""

    large_text: str | None = None
    """text displayed when hovering over the large image of the activity"""

    small_image: str | None = None
    """the id for a small asset of the activity, usually a snowflake"""

    small_text: str | None = None
    """text displayed when hovering over the small image of the activity"""


class ActivitySecrets(BaseModel):
    """https://discord.com/developers/docs/topics/gateway#activity-object-activity-secrets"""

    join: str | None = None
    """the secret for joining a party"""

    spectate: str | None = None
    """the secret for spectating a game"""

    match: str | None = None
    """the secret for a specific instanced match"""


class ActivityFlag(enum.IntFlag):
    """https://discord.com/developers/docs/topics/gateway#activity-object-activity-flags"""

    INSTANCE = 1 << 0
    """this activity is an instanced game session"""

    JOIN = 1 << 1
    """this activity is joinable"""

    SPECTATE = 1 << 2
    """this activity can be spectated"""

    JOIN_REQUEST = 1 << 3
    """this activity allows asking to join"""

    SYNC = 1 << 4
    """this activity is a spotify track"""

    PLAY = 1 << 5
    """activity is an embedded youtube video"""

    PARTY_PRIVACY_FRIENDS = 1 << 6
    """party privacy is set to friends only"""

    PARTY_PRIVACY_VOICE_CHANNEL = 1 << 7
    """party privacy is set to voice channel only"""

    EMBEDDED = 1 << 8
    """activity is an embedded something"""


class ActivityButton(BaseModel):
    """https://discord.com/developers/docs/topics/gateway#activity-object-activity-buttons"""

    label: str = Field(min_length=1, max_length=32)
    """the text shown on the button (1-32 characters)"""

    url: str = Field(min_length=1, max_length=512)
    """a url for the button (1-512 characters)"""


Activity.update_forward_refs()
