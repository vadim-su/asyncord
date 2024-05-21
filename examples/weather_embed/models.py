from pydantic import BaseModel  # noqa


class WeatherLocation(BaseModel):
    """Model for the weather location."""

    name: str
    region: str
    country: str
    localtime: str


class WeatherCondition(BaseModel):
    """Model for the weather condition."""

    text: str
    icon: str
    code: int


class WeatherCurrent(BaseModel):
    """Model for the current weather."""

    temp_c: float
    is_day: int
    condition: WeatherCondition
    cloud: int


class WeatherOutput(BaseModel):
    """Model for the weather output."""

    location: WeatherLocation
    current: WeatherCurrent
