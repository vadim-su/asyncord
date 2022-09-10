from __future__ import annotations

import typing

from yarl import URL

BASE_URL: typing.Final[URL] = URL('https://discord.com')
API_VERSION: typing.Final[int] = 10
REST_API_URL: typing.Final[URL] = URL(f'{BASE_URL}/api/v{API_VERSION}')
GATEWAY_URL: typing.Final[URL] = URL(f'wss://gateway.discord.gg/?v={API_VERSION}&encoding=json')
