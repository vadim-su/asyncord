"""Emojis resource for the client."""

from __future__ import annotations

from typing import TYPE_CHECKING

from asyncord.client.emojis.models.responses import EmojiResponse
from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.resources import APIResource
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.client.emojis.models.requests import CreateEmojiRequest, UpdateEmojiRequest
    from asyncord.client.http.client import HttpClient
    from asyncord.snowflake import SnowflakeInputType

__all__ = ('EmojiResource',)


class EmojiResource(APIResource):
    """Resource to perform actions on guild emojis.

    Attributes:
        guilds_url: URL for the guilds resource.
    """

    guilds_url = REST_API_URL / 'guilds'

    def __init__(
        self,
        http_client: HttpClient,
        guild_id: SnowflakeInputType,
    ):
        """Create a new emojis resource."""
        super().__init__(http_client)
        self.guild_id = guild_id
        self.emojis_url = self.guilds_url / str(self.guild_id) / 'emojis'

    async def get_guild_emoji(
        self,
        emoji_id: SnowflakeInputType,
    ) -> EmojiResponse:
        """Returns an emoji object for the given guild.

        Args:
            emoji_id: ID of the emoji to get.

        Reference:
        https://discord.com/developers/docs/resources/emoji#get-guild-emoji
        """
        url = self.emojis_url / str(emoji_id)
        resp = await self._http_client.get(url=url)
        return EmojiResponse.model_validate(resp.body)

    async def get_guild_emojis(self) -> list[EmojiResponse]:
        """Returns a list of emoji objects for the given guild.

        Reference:
        https://discord.com/developers/docs/resources/emoji#list-guild-emojis
        """
        resp = await self._http_client.get(url=self.emojis_url)
        return list_model(EmojiResponse).validate_python(resp.body)

    async def create_guild_emoji(
        self,
        emoji_data: CreateEmojiRequest,
        reason: str | None = None,
    ) -> EmojiResponse:
        """Create a new emoji for the guild.

        Args:
            emoji_data: Data for the new emoji.
            reason: Reason for creating the emoji.

        Reference:
        https://discord.com/developers/docs/resources/emoji#create-guild-emoji
        """
        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = emoji_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.post(url=self.emojis_url, payload=payload, headers=headers)
        return EmojiResponse.model_validate(resp.body)

    async def update_guild_emoji(
        self,
        emoji_id: SnowflakeInputType,
        emoji_data: UpdateEmojiRequest,
        reason: str | None = None,
    ) -> EmojiResponse:
        """Update the given emoji.

        Args:
            emoji_id: ID of the emoji to update.
            emoji_data: New data for the emoji.
            reason: Reason for updating the emoji.

        Reference:
        https://discord.com/developers/docs/resources/emoji#modify-guild-emoji
        """
        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = emoji_data.model_dump(mode='json', exclude_unset=True)
        url = self.emojis_url / str(emoji_id)
        resp = await self._http_client.patch(url=url, payload=payload, headers=headers)
        return EmojiResponse.model_validate(resp.body)

    async def delete_guild_emoji(
        self,
        emoji_id: SnowflakeInputType,
        reason: str | None = None,
    ) -> None:
        """Delete the given emoji.

        Args:
            emoji_id: ID of the emoji to delete.
            reason: Reason for deleting the emoji.

        Reference:
        https://discord.com/developers/docs/resources/emoji#delete-guild-emoji
        """
        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        url = self.emojis_url / str(emoji_id)

        await self._http_client.delete(url=url, headers=headers)
