import os
from dataclasses import dataclass

import pytest


@dataclass
class IntegrationTestData:
    token: str
    channel_id: str
    voice_channel_id: str
    guild_id: str
    user_id: str
    message_id: str
    member_id: str
    custom_emoji: str
    guild_prefix_to_delete: str
    app_id: str
    role_id: str
    user_to_ban: str


@pytest.fixture(scope='session')
def integration_data() -> IntegrationTestData:
    token = os.environ.get('ASYNCORD_TEST_TOKEN')
    if not token:
        pytest.skip('ASYNCORD_TEST_TOKEN environment variable is not set')
    try:
        return IntegrationTestData(
            token=token,
            channel_id=os.environ['ASYNCORD_TEST_CHANNEL_ID'],
            voice_channel_id=os.environ['ASYNCORD_TEST_VOICE_CHANNEL_ID'],
            guild_id=os.environ['ASYNCORD_TEST_GUILD_ID'],
            user_id=os.environ['ASYNCORD_TEST_USER_ID'],
            message_id=os.environ['ASYNCORD_TEST_MESSAGE_ID'],
            member_id=os.environ['ASYNCORD_TEST_MEMBER_ID'],
            custom_emoji=os.environ['ASYNCORD_TEST_CUSTOM_EMOJI'],
            guild_prefix_to_delete=os.environ['ASYNCORD_TEST_GUILD_PREFIX_TO_DELETE'],
            app_id=os.environ['ASYNCORD_TEST_APP_ID'],
            role_id=os.environ['ASYNCORD_TEST_ROLE_ID'],
            user_to_ban=os.environ['ASYNCORD_TEST_USER_TO_BAN'],
        )
    except KeyError as err:
        pytest.skip(f"'{err.args[0]}' environment variable is not set")


@pytest.fixture(scope='session')
def token(integration_data: IntegrationTestData):
    return integration_data.token


def pytest_addoption(parser):
    parser.addoption(
        '--run-limited', action='store_true', default=False, help='run limited tests',
    )


def pytest_configure(config):
    config.addinivalue_line('markers', 'limited: mark test as api limited')


def pytest_collection_modifyitems(config, items):
    if config.getoption('--run-limited'):
        return
    skip_limited = pytest.mark.skip(
        reason='This test has api limitations. Can be run with --run-limited option',
    )
    for item in items:
        if 'limited' in item.keywords:
            item.add_marker(skip_limited)
