import random
from datetime import datetime, timedelta

import pytest

from asyncord.snowflake import Snowflake


class TestSnowflake:
    def setup_method(self) -> None:
        self.raw_snowflake = 175928847299117063
        self.snowflake = Snowflake(self.raw_snowflake)

    def test_timestamp(self):
        assert self.snowflake.timestamp == datetime(2016, 4, 30, 11, 18, 25, 796000)

    def test_internal_worker_id(self):
        assert self.snowflake.internal_worker_id == 1

    def test_internal_process_id(self):
        assert self.snowflake.internal_process_id == 0

    def test_incriment(self):
        assert self.snowflake.increment == 7

    @pytest.mark.parametrize('snowflake_type', [Snowflake, int, str])
    def test_equality(self, snowflake_type):
        # check Snowflake and Snowflake equality
        assert self.snowflake == snowflake_type(self.raw_snowflake)
        assert self.snowflake != snowflake_type(self.raw_snowflake + random.randint(1, 100))

    def test_int(self):
        assert int(self.snowflake) == self.raw_snowflake

    def test_str(self):
        assert str(self.snowflake) == str(self.raw_snowflake)

    def test_build(self):
        timestamp = datetime.now()
        snowflake = Snowflake.build(
            timestamp=timestamp,
            internal_worker_id=4,
            internal_process_id=2,
            increment=55,
        )
        assert abs(snowflake.timestamp - timestamp) < timedelta(seconds=1)
        assert snowflake.internal_worker_id == 4
        assert snowflake.internal_process_id == 2
        assert snowflake.increment == 55
