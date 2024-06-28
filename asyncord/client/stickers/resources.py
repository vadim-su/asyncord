"""Sticker Resource.

Contains endpoints to Sticker resource.

Reference:
https://discord.com/developers/docs/resources/sticker
"""

from __future__ import annotations

from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.http.models import FormField, FormPayload
from asyncord.client.models.stickers import Sticker
from asyncord.client.resources import APIResource
from asyncord.client.stickers.models.requests import (
    CreateGuildStickerRequest,
    UpdateGuildStickerRequest,
)
from asyncord.client.stickers.models.responses import StickerPackListResponse
from asyncord.snowflake import SnowflakeInputType
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL


class StickersResource(APIResource):
    """Stickers Resource.

    These endpoints are for managing Stickers.

    Reference:
    https://discord.com/developers/docs/resources/sticker
    """

    stickers_url = REST_API_URL / 'stickers'
    sticker_packs_url = REST_API_URL / 'sticker-packs'
    guild_url = REST_API_URL / 'guilds'

    async def get_sticker(
        self,
        sticker_id: SnowflakeInputType,
    ) -> Sticker:
        """Returns a sticker object for the given sticker ID.

        Reference:
        https://discord.com/developers/docs/resources/sticker#get-sticker

        Args:
            sticker_id: The ID of the sticker.
        """
        url = self.stickers_url / str(sticker_id)

        resp = await self._http_client.get(url=url)

        return Sticker.model_validate(resp.body)

    async def get_sticker_pack_list(self) -> StickerPackListResponse:
        """Returns a list of available sticker packs.

        Reference:
        https://discord.com/developers/docs/resources/sticker#list-sticker-packs
        """
        url = self.sticker_packs_url

        resp = await self._http_client.get(url=url)

        return StickerPackListResponse.model_validate(resp.body)

    async def get_guild_stickers_list(self, guild_id: SnowflakeInputType) -> list[Sticker]:
        """Returns array of sticker objects foriven guild.

        Reference:
        https://discord.com/developers/docs/resources/sticker#list-guild-stickers

        Args:
            guild_id: ID of guild.
        """
        url = self.guild_url / str(guild_id) / 'stickers'

        resp = await self._http_client.get(url=url)

        return list_model(Sticker).validate_python(resp.body)

    async def get_guild_sticker(
        self,
        guild_id: SnowflakeInputType,
        sticker_id: SnowflakeInputType,
    ) -> Sticker:
        """Returns sticker object for given guild and sticker IDs.

        Reference:
        https://discord.com/developers/docs/resources/sticker#get-guild-sticker

        Args:
            guild_id: ID of guild.
            sticker_id: ID of sticker.
        """
        url = self.guild_url / str(guild_id) / 'stickers' / str(sticker_id)

        resp = await self._http_client.get(url=url)

        return Sticker.model_validate(resp.body)

    async def create_guild_sticker(
        self,
        guild_id: SnowflakeInputType,
        sticker_data: CreateGuildStickerRequest,
        reason: str | None = None,
    ) -> Sticker:
        """Create new sticker for guild.

        Lottie stickers can only be uploaded on guilds that have either the VERIFIED and/or the PARTNERED guild feature.
        Uploaded stickers are constrained to 5 seconds in length for animated stickers, and 320 x 320 pixels.

        Reference:
        https://discord.com/developers/docs/resources/sticker#create-guild-sticker

        Args:
            guild_id: ID of guild.
            sticker_data: Data for new sticker.
            reason: Reason for creation.

        Returns:
            The created sticker.
        """
        url = self.guild_url / str(guild_id) / 'stickers'

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload_dict = sticker_data.model_dump(
            mode='python',
            by_alias=True,
            exclude_unset=True,
        )

        form_fields = {}
        for field_name, value in payload_dict.items():
            form_fields[field_name] = FormField(value)

        payload = FormPayload(form_fields)
        resp = await self._http_client.post(
            url=url,
            payload=payload,
            headers=headers,
        )
        return Sticker.model_validate(resp.body)

    async def update_guild_sticker(
        self,
        guild_id: SnowflakeInputType,
        sticker_id: SnowflakeInputType,
        sticker_data: UpdateGuildStickerRequest,
        reason: str | None = None,
    ) -> Sticker:
        """Modify the given sticker.

        Reference:
        https://discord.com/developers/docs/resources/sticker#modify-guild-sticker

        Args:
            guild_id: The ID of the guild.
            sticker_id: The ID of the sticker.
            sticker_data: The data to update the sticker with.
            reason: The reason for the update.
        """
        url = self.guild_url / str(guild_id) / 'stickers' / str(sticker_id)

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = sticker_data.model_dump(mode='json', exclude_unset=True)

        resp = await self._http_client.patch(url=url, payload=payload, headers=headers)

        return Sticker.model_validate(resp.body)

    async def delete_guild_sticker(
        self,
        guild_id: SnowflakeInputType,
        sticker_id: SnowflakeInputType,
        reason: str | None = None,
    ) -> None:
        """Delete the given sticker.

        Reference:
        https://discord.com/developers/docs/resources/sticker#delete-guild-sticker

        Args:
            guild_id: The ID of the guild.
            sticker_id: The ID of the sticker.
            reason: The reason for the deletion.
        """
        url = self.guild_url / str(guild_id) / 'stickers' / str(sticker_id)

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.delete(url=url, headers=headers)
