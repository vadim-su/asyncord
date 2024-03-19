"""This module contains the `Locale` enum and `LocaleInputType` type."""

import enum
from typing import Annotated

from pydantic import Field


@enum.unique
class Locale(enum.StrEnum):
    """Represents a locale for a language.

    Reference:
    https://discord.com/developers/docs/reference#locales
    """

    ID = 'id'
    DA = 'da'
    DE = 'de'
    EN_GB = 'en-GB'
    EN_US = 'en-US'
    ES_ES = 'es-ES'
    FR = 'fr'
    HR = 'hr'
    IT = 'it'
    LT = 'lt'
    HU = 'hu'
    NL = 'nl'
    NO = 'no'
    PL = 'pl'
    PT_BR = 'pt-BR'
    RO = 'ro'
    FI = 'fi'
    SV_SE = 'sv-SE'
    VI = 'vi'
    TR = 'tr'
    CS = 'cs'
    EL = 'el'
    BG = 'bg'
    RU = 'ru'
    UK = 'uk'
    HI = 'hi'
    TH = 'th'
    ZH_CN = 'zh-CN'
    JA = 'ja'
    ZH_TW = 'zh-TW'
    KO = 'ko'


type LocaleInputType = Annotated[str | Locale, Annotated[Locale, Field(min_length=2)]]
"""Type of locale input."""
