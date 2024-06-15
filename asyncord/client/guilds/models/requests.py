"""Request models for guilds."""

from typing import Self

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel, Field, field_serializer, model_validator

from asyncord.base64_image import Base64ImageInputType
from asyncord.client.channels.models.requests.creation import CreateChannelRequestType
from asyncord.client.guilds.models.common import (
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    OnboardingMode,
    OnboardingPromptType,
)
from asyncord.client.models.automoderation import AutoModerationRuleEventType, RuleAction, TriggerMetadata, TriggerType
from asyncord.client.roles.models.responses import RoleResponse
from asyncord.snowflake import SnowflakeInputType


class CreateGuildRequest(BaseModel):
    """Data for creating a guild.

    Endpoint for which this model is used can only be used by bots
    in less than 10 guilds

    Reference:
    https://discord.com/developers/docs/resources/guild#create-guild
    """

    name: str = Field(min_length=2, max_length=100)
    """Name of the guild (2-100 characters)."""

    icon: Base64ImageInputType | None = None
    """Base64 128x128 image for the guild icon."""

    verification_level: int | None = None
    """Verification level."""

    default_message_notifications: DefaultMessageNotificationLevel | None = None
    """Default message notification level."""

    explicit_content_filter: ExplicitContentFilterLevel | None = None
    """Explicit content filter level."""

    roles: list[RoleResponse] | None = None
    """New guild roles.

    The first member of the array is used to change properties of the guild's
    @everyone role. If you are trying to bootstrap a guild with additional
    roles, keep this in mind.
    The required id field within each role object is an integer placeholder,
    and will be replaced by the API upon consumption. Its purpose is to allow
    youto overwrite a role's permissions in a channel when also passing in
    channels with the channels array.
    """

    channels: list[CreateChannelRequestType] | None = None
    """New guild's channels.

    When using the channels, the position field is ignored, and
    none of the default channels are created.

    The id field within each channel object may be set to an integer
    placeholder, and will be replaced by the API upon consumption.
    Its purpose is to allow you to create `GUILD_CATEGORY` channels by setting
    the parent_id field on any children to the category's id field.

    Category channels must be listed before any children.
    """

    afk_channel_id: SnowflakeInputType | None = None
    """ID for afk channel."""

    afk_timeout: int | None = None
    """Afk timeout in seconds."""

    system_channel_id: SnowflakeInputType | None = None
    """The id of the channel where guild notices.

    Notices such as welcome messages and boost events are posted.
    """

    system_channel_flags: int | None = None
    """System channel flags."""


class WelcomeScreenChannel(BaseModel):
    """Welcome screen channel object.

    Reference:
    https://discord.com/developers/docs/resources/guild#welcome-screen-object-welcome-screen-channel-structure
    """

    channel_id: SnowflakeInputType
    """ID of the channel."""

    description: str
    """Description of the channel."""

    emoji_id: SnowflakeInputType | None
    """Emoji ID, if the emoji is custom."""

    emoji_name: str | None
    """Emoji name if custom, the unicode character if standard, or null if no emoji is set."""


class UpdateWelcomeScreenRequest(BaseModel):
    """Data for updating a welcome screen.

    Reference:
    https://discord.com/developers/docs/resources/guild#modify-guild-welcome-screen
    """

    enabled: bool | None = None
    """Whether the welcome screen is enabled."""

    welcome_channels: list[WelcomeScreenChannel] | None = Field(None, max_length=5)
    """Channels shown in the welcome screen.

    Up to 5 channels can be specified.
    """

    description: str | None = None
    """Server description shown in the welcome screen."""


class CreateAutoModerationRuleRequest(BaseModel):
    """Data for creating an auto moderation rule.

    Reference:
    https://canary.discord.com/developers/docs/resources/auto-moderation#create-auto-moderation-rule-json-params
    """

    name: str
    """Name of the rule."""

    event_type: AutoModerationRuleEventType
    """Rule event type."""

    trigger_type: TriggerType
    """Rule trigger type."""

    trigger_metadata: TriggerMetadata | None = None
    """Rule trigger metadata.

    Required, but can be omited based on trigger type.
    """

    actions: list[RuleAction]
    """Actions which will execute when the rule is triggered."""

    enabled: bool | None = None
    """Whether the rule is enabled.

    False by default.
    """

    exempt_roles: list[SnowflakeInputType] | None = Field(None, max_length=20)
    """Role ids that should not be affected by the rule.

    Maximum of 20.
    """

    exempt_channels: list[SnowflakeInputType] | None = Field(None, max_length=50)
    """Channel ids that should not be affected by the rule.

    Maximum of 50.
    """

    @model_validator(mode='after')
    def validate_trigger_metadata(self) -> Self:
        """Validate trigger metadata based on trigger type."""
        if self.trigger_type is TriggerType.KEYWORD:
            has_filter_or_regex = self.trigger_metadata and (
                self.trigger_metadata.keyword_filter or self.trigger_metadata.regex_patterns
            )
            if not has_filter_or_regex:
                raise ValueError('Keyword filter or regex patterns are required for keyword trigger type.')

        if self.trigger_type is TriggerType.KEYWORD_PRESET:
            has_preset = self.trigger_metadata and self.trigger_metadata.presets
            if not has_preset:
                raise ValueError('Keyword preset is required for keyword preset trigger type.')

        return self


class UpdateAutoModerationRuleRequest(BaseModel):
    """Data for updating an auto moderation rule.

    Reference:
    https://canary.discord.com/developers/docs/resources/auto-moderation#modify-auto-moderation-rule-json-params
    """

    name: str
    """Name of the rule."""

    event_type: FallbackAdapter[AutoModerationRuleEventType]
    """Rule event type."""

    trigger_metadata: TriggerMetadata | None = None
    """Rule trigger metadata.

    Required, but can be omited based on trigger type.
    Reference:
    https://canary.discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-trigger-metadata
    """

    actions: list[RuleAction]
    """Actions which will execute when the rule is triggered."""

    enabled: bool
    """Whether the rule is enabled.

    False by default.
    """

    exempt_roles: list[SnowflakeInputType] = Field(max_length=20)
    """Role ids that should not be affected by the rule.

    Maximum of 20.
    """

    exempt_channels: list[SnowflakeInputType] = Field(max_length=50)
    """Channel ids that should not be affected by the rule.

    Maximum of 50.
    """


class UpdateWidgetSettingsRequest(BaseModel):
    """Data for updating widget settings.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-widget-settings-object-guild-widget-settings-structure
    """

    enabled: bool | None = None
    """Whether the widget is enabled."""

    channel_id: SnowflakeInputType | None = None
    """Widget channel id."""


class OnboardingPromptOption(BaseModel):
    """Onboarding prompt option object.

    Reference:
    https://canary.discord.com/developers/docs/resources/guild#guild-onboarding-object-prompt-option-structure
    """

    id: SnowflakeInputType
    """Id of the prompt option."""

    channel_ids: list[SnowflakeInputType]
    """Id for channels a member is added to when the option is selected."""

    role_ids: list[SnowflakeInputType]
    """Id for roles assigned to a member when the option is selected."""

    emoji_id: SnowflakeInputType | None = None
    """ID for the emoji."""

    emoji_name: str | None = None
    """Emoji name of the option."""

    emoji_animated: bool | None = None
    """Whether the emoji is animated."""

    title: str
    """Title of the option."""

    description: str | None = None
    """Description of the option."""


class OnboardingPrompt(BaseModel):
    """Onboarding prompt object.

    Reference:
    https://canary.discord.com/developers/docs/resources/guild#guild-onboarding-object-onboarding-prompt-structure
    """

    id: SnowflakeInputType
    """ID of the prompt."""

    type: OnboardingPromptType
    """Type of prompt."""

    options: list[OnboardingPromptOption]
    """Options available within the prompt."""

    title: str
    """Title of the prompt."""

    single_select: bool
    """Indicates whether users are limited to selecting one option for the prompt."""

    required: bool
    """Indicates whether the prompt is required.

    Before a user completes the onboarding flow.
    """

    in_boarding: bool
    """Indicates whether the prompt is present in the onboarding flow.

    If false, the prompt will only appear in the Channels & Roles tab.
    """


class UpdateOnboardingRequest(BaseModel):
    """Update onboarding settings.

    Reference:
    https://canary.discord.com/developers/docs/resources/guild#modify-guild-onboarding-json-params
    """

    prompts: list[OnboardingPrompt]
    """Prompts shown during onboarding and in customize community."""

    default_channel_ids: list[SnowflakeInputType]
    """Channel IDs that members get opted into automatically"""

    enabled: bool
    """Whether onboarding is enabled."""

    mode: OnboardingMode
    """Current mode of onboarding."""


class PruneRequest(BaseModel):
    """Data for pruning guild members.

    Reference:
    https://discord.com/developers/docs/resources/guild#begin-guild-prune
    """

    days: int
    """Number of days to prune members for."""

    compute_prune_count: bool | None = None
    """Whether to compute the number of pruned members."""

    include_roles: set[SnowflakeInputType] | None = None
    """Roles to include in the prune."""

    @field_serializer('include_roles', when_used='json-unless-none', return_type=str)
    @classmethod
    def serialize_include_roles_to_str(cls, rolese: set[SnowflakeInputType]) -> str:
        """Serialize include roles to string."""
        return ','.join(map(str, rolese))
