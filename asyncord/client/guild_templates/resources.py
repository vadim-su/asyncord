"""This module contains the guilds templates resource endpoints.

Reference: https://discord.com/developers/docs/resources/guild-template
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from asyncord.client.guild_templates.models.responses import GuildTemplateResponse
from asyncord.client.guilds.models.responses import GuildResponse
from asyncord.client.resources import APIResource
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.client.guild_templates.models.requests import (
        CreateGuildFromTemplateRequest,
        CreateGuildTemplateRequest,
        UpdateGuildTemplateRequest,
    )
    from asyncord.client.http.client import HttpClient
    from asyncord.snowflake import SnowflakeInputType


__all__ = ('GuildTemplatesResource',)


class GuildTemplatesResource(APIResource):
    """Representaion of the guild templates resource.

    Attributes:
        guilds_url: Guilds resource URL.
    """

    guilds_url = REST_API_URL / 'guilds'

    def __init__(self, http_client: HttpClient, guild_id: SnowflakeInputType):
        """Initialize the guild templates resource."""
        super().__init__(http_client)
        self.guild_id = guild_id
        self.templates_url = self.guilds_url / str(self.guild_id) / 'templates'

    async def get_template(
        self,
        template_code: str,
    ) -> GuildTemplateResponse:
        """Get a guild template by its code.

        Reference:
        https://discord.com/developers/docs/resources/guild-template#get-guild-template

        Args:
            template_code: The template code.
        """
        url = self.guilds_url / 'templates' / str(template_code)

        resp = await self._http_client.get(url=url)
        return GuildTemplateResponse.model_validate(resp.body)

    async def get_guild_templates(
        self,
    ) -> list[GuildTemplateResponse]:
        """Get the guild's templates.

        Reference:
        https://discord.com/developers/docs/resources/guild-template#get-guild-templates
        """
        resp = await self._http_client.get(url=self.templates_url)
        return list_model(GuildTemplateResponse).validate_python(resp.body)

    async def create_guild_from_template(
        self,
        template_code: str,
        create_data: CreateGuildFromTemplateRequest,
    ) -> GuildResponse:
        """Create a guild from a template.

        This endpoint can be used only by bots in less than 10 guilds.

        Reference:
        https://discord.com/developers/docs/resources/guild-template#create-guild-from-guild-template
        """
        url = self.guilds_url / 'templates' / str(template_code)

        payload = create_data.model_dump(mode='json', exclude_none=True)
        resp = await self._http_client.post(url=url, payload=payload)

        return GuildResponse.model_validate(resp.body)

    async def create_guild_template(
        self,
        template_data: CreateGuildTemplateRequest,
    ) -> GuildTemplateResponse:
        """Create a new guild template.

        Reference:
        https://discord.com/developers/docs/resources/guild-template#create-guild-template

        Args:
            template_data: The template data.
        """
        payload = template_data.model_dump(mode='json', exclude_unset=True)

        resp = await self._http_client.post(url=self.templates_url, payload=payload)
        return GuildTemplateResponse.model_validate(resp.body)

    async def sync_guild_template(
        self,
        template_code: str,
    ) -> GuildTemplateResponse:
        """Sync a guild template.

        Reference:
        https://discord.com/developers/docs/resources/guild-template#sync-guild-template

        Args:
            template_code: The template code.
        """
        url = self.templates_url / str(template_code)

        resp = await self._http_client.put(url=url)
        return GuildTemplateResponse.model_validate(resp.body)

    async def update_guild_template(
        self,
        template_code: str,
        template_data: UpdateGuildTemplateRequest,
    ) -> GuildTemplateResponse:
        """Update a guild template.

        Reference:
        https://discord.com/developers/docs/resources/guild-template#modify-guild-template

        Args:
            template_code: The template code.
            template_data: The template data.
        """
        url = self.templates_url / str(template_code)

        payload = template_data.model_dump(mode='json', exclude_unset=True)

        resp = await self._http_client.patch(url=url, payload=payload)
        return GuildTemplateResponse.model_validate(resp.body)

    async def delete_guild_template(
        self,
        template_code: str,
    ) -> GuildTemplateResponse:
        """Delete a guild template.

        Returns deleted template object on success.

        Reference:
        https://discord.com/developers/docs/resources/guild-template#delete-guild-template

        Args:
            template_code: The template code.
        """
        url = self.templates_url / str(template_code)

        resp = await self._http_client.delete(url=url)
        return GuildTemplateResponse.model_validate(resp.body)
