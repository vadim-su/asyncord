import os
from dataclasses import dataclass

import pytest


@dataclass
class IntegrationData:
    TOKEN = os.environ.get('TOKEN')
    TEST_CHANNEL_ID = os.environ.get('TEST_CHANNEL_ID')
    TEST_VOICE_CHANNEL_ID = os.environ.get('TEST_VOICE_CHANNEL_ID')
    TEST_GUILD_ID = os.environ.get('TEST_GUILD_ID')
    TEST_USER_ID = os.environ.get('TEST_USER_ID')
    TEST_MESSAGE_ID = os.environ.get('TEST_MESSAGE_ID')
    TEST_MEMBER_ID = os.environ.get('TEST_MEMBER_ID')
    TEST_GUILD_NAME = os.environ.get('TEST_GUILD_NAME')
    TEST_APP_ID = os.environ.get('TEST_APP_ID')
    TEST_IMAGE_FILE = os.environ.get('TEST_IMAGE_FILE')
    TEST_ROLE_ID = os.environ.get('TEST_ROLE_ID')
    TEST_USER_TO_BAN = os.environ.get('TEST_USER_TO_BAN')


@pytest.fixture(scope='session')
def integration_data() -> IntegrationData:
    return IntegrationData()


@pytest.fixture(scope='session')
def token(integration_data: IntegrationData):
    bot_token = integration_data.TOKEN
    if not bot_token:
        pytest.skip('TOKEN environment variable is not set')
    return bot_token


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
