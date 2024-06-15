"""This module contains the `Activity` model and related enums and models.

Reference:
https://discord.com/developers/docs/game-sdk/activities#activities
"""

from __future__ import annotations

import datetime
import enum

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel, Field

from asyncord.snowflake import Snowflake

__all__ = (
    'Activity',
    'ActivityAssets',
    'ActivityButton',
    'ActivityEmoji',
    'ActivityFlag',
    'ActivityParty',
    'ActivityResponse',
    'ActivitySecrets',
    'ActivityTimestamps',
    'ActivityType',
)


@enum.unique
class ActivityType(enum.IntEnum):
    """Activity type.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-types
    """

    GAME = 0
    """User is playing a game.

    `Playing {name}`.

    Example:
        `Playing Rocket League`
    """

    STREAMING = 1
    """User is streaming.

    `Streaming {details}`.

    Example:
        `Streaming Rocket League`
    """

    LISTENING = 2
    """User is listening to music.

    `Listening to {name}`.

    Example:
        `Listening to Spotify`
    """
    WATCHING = 3
    """User is watching something.

    `Watching {name}`.

    Example:
        `Watching YouTube Together`
    """

    CUSTOM = 4
    """User is doing something with a custom emoji.

    `{emoji} {text}`.

    Example:
        `:smile: I'm happy`
    """

    COMPETING = 5
    """User is competing in something.

    `Competing in {name}`.

    Example:
        `Competing in Arena World Champions`
    """

    HANG_STATUS = 6
    """User is setting up a new status
    This status isn't documented by Discord, but real.
    """


class ActivityTimestamps(BaseModel):
    """Timestamps for start and/or end of the `Activity`.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-timestamps
    """

    start: int | None = None
    """Unix time (in milliseconds) of when the activity started."""

    end: int | None = None
    """Unix time (in milliseconds) of when the activity ends."""


class ActivityEmoji(BaseModel):
    """Activity emoji.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-emoji
    """

    id: Snowflake | None = None
    """Id of the emoji."""

    name: str
    """Name of the emoji."""

    animated: bool | None = None
    """Whether this emoji is animated."""


class ActivityParty(BaseModel):
    """Activity party.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-party
    """

    id: str | None = None
    """Id of the party."""

    size: tuple[int, int] | None = None
    """Show the party's current and maximum size."""


class ActivityAssets(BaseModel):
    """Activity assets.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-assets
    """

    # FIXME: Posible add support for large_image_text and small_image_text validation
    # https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-asset-image

    large_image: str | None = None
    """Id for a large asset of the activity,

    Usually a snowflake.
    """

    large_text: str | None = None
    """Text displayed when hovering over the large image of the activity."""

    small_image: str | None = None
    """Id for a small asset of the activity.

    Usually a snowflake.
    """

    small_text: str | None = None
    """Text displayed when hovering over the small image of the activity."""


class ActivitySecrets(BaseModel):
    """Activity secrets.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-secrets
    """

    join: str | None = None
    """Secret for joining a party."""

    spectate: str | None = None
    """Secret for spectating a game."""

    match: str | None = None
    """Secret for a specific instanced match."""


class ActivityFlag(enum.IntFlag):
    """Activity flags.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-flags
    """

    INSTANCE = 1 << 0
    """Activity is an instanced game session."""

    JOIN = 1 << 1
    """Activity is joinable."""

    SPECTATE = 1 << 2
    """Activity can be spectated."""

    JOIN_REQUEST = 1 << 3
    """Activity allows asking to join."""

    SYNC = 1 << 4
    """Activity is a spotify track."""

    PLAY = 1 << 5
    """Activity is an embedded youtube video."""

    PARTY_PRIVACY_FRIENDS = 1 << 6
    """Party privacy is set to friends only."""

    PARTY_PRIVACY_VOICE_CHANNEL = 1 << 7
    """Party privacy is set to voice channel only."""

    EMBEDDED = 1 << 8
    """Activity is an embedded something."""


class ActivityButton(BaseModel):
    """Activity button.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-buttons
    """

    label: str = Field(min_length=1, max_length=32)
    """Text shown on the button. Should be between 1-32 characters."""

    url: str = Field(min_length=1, max_length=512)
    """Url for the button. Should be between 1-512 characters."""


class Activity(BaseModel):
    """Represents a Discord activity.

    Bots are only able to send name, state, type, and optionally url.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#activity-object
    """

    name: str
    """Activity's name."""

    type: ActivityType
    """Activity type."""

    url: str | None = None
    """Stream url.

    Is validated when type is `ActivityType.STREAMING`.

    Currently only supports Twitch and YouTube.
    Only https://twitch.tv/ and https://youtube.com/ urls will work.
    """

    created_at: datetime.datetime | None = None
    """Unix timestamp of when the activity was added to the user's session."""

    timestamps: ActivityTimestamps | None = None
    """Unix timestamps for start and/or end of the game."""

    application_id: Snowflake | None = None
    """Application id for the game."""

    details: str | None = None
    """What the player is currently doing."""

    state: str | None = None
    """User's current party status."""

    emoji: ActivityEmoji | None = None
    """Emoji data for custom statuses."""

    party: ActivityParty | None = None
    """Information for the current party of the player."""

    assets: ActivityAssets | None = None
    """Images for the presence and their hover texts."""

    secrets: ActivitySecrets | None = None
    """Secrets for Rich Presence joining and spectating."""

    instance: bool | None = None
    """Whether or not the activity is an instanced game session."""

    flags: ActivityFlag | None = None
    """Activity flags OR d together.

    Describes what the payload includes."""

    buttons: list[ActivityButton] | None = None
    """Custom buttons shown in the Rich Presence.

    Maximum of 2 buttons.
    """


class ActivityResponse(BaseModel):
    """Represents a Discord activity.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#activity-object
    """

    name: str
    """Activity's name."""

    type: FallbackAdapter[ActivityType]
    """Activity type."""

    url: str | None = None
    """Stream url.

    Is validated when type is `ActivityType.STREAMING`.

    Currently only supports Twitch and YouTube.
    Only https://twitch.tv/ and https://youtube.com/ urls will work.
    """

    created_at: datetime.datetime | None = None
    """Unix timestamp of when the activity was added to the user's session."""

    timestamps: ActivityTimestamps | None = None
    """Unix timestamps for start and/or end of the game."""

    application_id: Snowflake | None = None
    """Application id for the game."""

    details: str | None = None
    """What the player is currently doing."""

    state: str | None = None
    """User's current party status."""

    emoji: ActivityEmoji | None = None
    """Emoji data for custom statuses."""

    party: ActivityParty | None = None
    """Information for the current party of the player."""

    assets: ActivityAssets | None = None
    """Images for the presence and their hover texts."""

    secrets: ActivitySecrets | None = None
    """Secrets for Rich Presence joining and spectating."""

    instance: bool | None = None
    """Whether or not the activity is an instanced game session."""

    flags: ActivityFlag | None = None
    """Activity flags OR d together.

    Describes what the payload includes."""

    buttons: list[str] | None = None
    """Custom buttons shown in the Rich Presence.

    Maximum of 2 buttons.
    """
