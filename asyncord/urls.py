"""This module contains the base URLs for the Discord API and Gateway."""

from __future__ import annotations

from typing import Final

from yarl import URL

BASE_URL: Final[URL] = URL('https://discord.com')
API_VERSION: Final[int] = 10
REST_API_URL: Final[URL] = URL(f'{BASE_URL}/api/v{API_VERSION}')
GATEWAY_URL: Final[URL] = URL(f'wss://gateway.discord.gg/?v={API_VERSION}&encoding=json')
INVITE_BASE_URL: Final[URL] = URL('https://discord.gg')
