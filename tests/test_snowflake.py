import datetime
import random

import pytest
from pydantic import BaseModel

from asyncord.snowflake import Snowflake


@pytest.fixture
def raw_snowflake() -> int:
    """Return a raw snowflake value."""
    return 175928847299117063


@pytest.fixture
def snowflake(raw_snowflake: int) -> Snowflake:
    """Return a snowflake instance."""
    return Snowflake(raw_snowflake)


def test_timestamp(snowflake: Snowflake) -> None:
    """Test that the timestamp is correct."""
    assert snowflake.timestamp == datetime.datetime(2016, 4, 30, 11, 18, 25, 796000, tzinfo=datetime.UTC)


def test_internal_worker_id(snowflake: Snowflake) -> None:
    """Test that the internal worker id is correct."""
    assert snowflake.internal_worker_id == 1


def test_internal_process_id(snowflake: Snowflake) -> None:
    """Test that the internal process id is correct."""
    assert snowflake.internal_process_id == 0


def test_incriment(snowflake: Snowflake) -> None:
    """Test that the increment is correct."""
    assert snowflake.increment == 7


@pytest.mark.parametrize('snowflake_type', [Snowflake, int, str])
def test_equality(snowflake: Snowflake, raw_snowflake: int, snowflake_type: type) -> None:
    """Test that snowflakes are equal."""
    assert snowflake == snowflake_type(raw_snowflake)
    assert snowflake != snowflake_type(raw_snowflake + random.randint(1, 100))


def test_int_convertation(snowflake: Snowflake, raw_snowflake: int) -> None:
    """Test that snowflake can be converted to int."""
    assert int(snowflake) == raw_snowflake


def test_str_convertation(snowflake: Snowflake, raw_snowflake: int) -> None:
    """Test that snowflake can be converted to str."""
    assert str(snowflake) == str(raw_snowflake)


def test_build_from_raw_values() -> None:
    """Test that snowflake can be built from raw values."""
    timestamp = datetime.datetime.now(tz=datetime.UTC)
    snowflake = Snowflake.build(
        timestamp=timestamp,
        internal_worker_id=4,
        internal_process_id=2,
        increment=55,
    )
    assert abs(snowflake.timestamp - timestamp) < datetime.timedelta(seconds=1)
    assert snowflake.internal_worker_id == 4
    assert snowflake.internal_process_id == 2
    assert snowflake.increment == 55


@pytest.mark.parametrize('snowflake_type', [Snowflake, int, str])
def test_snowflake_as_part_of_model(raw_snowflake: int, snowflake_type: type) -> None:
    """Test that snowflake can be used as part of pydantic model."""

    class Model(BaseModel):
        id: Snowflake

    model = Model(id=snowflake_type(raw_snowflake))
    assert model.id == raw_snowflake
    assert model.id.timestamp == datetime.datetime(2016, 4, 30, 11, 18, 25, 796000, tzinfo=datetime.UTC)
    assert model.id.internal_worker_id == 1
    assert model.id.internal_process_id == 0
    assert model.id.increment == 7

    assert model.model_dump() == {'id': Snowflake(raw_snowflake)}
    assert model.model_dump(mode='json') == {'id': str(raw_snowflake)}
