import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import pytest

INTEGRATION_TEST_DIR: Final[Path] = Path(__file__).parent / 'integration'


@dataclass
class IntegrationTestData:
    """Data to perform integration tests."""

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
    stage_id: str


@pytest.fixture(scope='session')
def integration_data() -> IntegrationTestData:
    """Get data to perform integration tests."""
    token = os.environ.get('ASYNCORD_TEST_TOKEN')
    if token is None:
        raise RuntimeError('ASYNCORD_TEST_TOKEN env variable is not set')
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
        stage_id=os.environ['ASYNCORD_TEST_STAGE_ID'],
    )


@pytest.fixture(scope='session')
def token(integration_data: IntegrationTestData) -> str:
    """Get token to perform integration tests."""
    return integration_data.token


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom options to pytest."""
    parser.addoption(
        '--run-limited',
        action='store_true',
        default=False,
        help='run limited tests',
    )
    parser.addoption(
        '--disable-integration',
        action='store_true',
        default=False,
        help='disable integration tests',
    )


def pytest_configure(config: pytest.Config) -> None:
    """Add custom markers to some tests."""
    config.addinivalue_line('markers', 'limited: mark test as api limited')
    config.addinivalue_line('markers', 'integration: mark test as integration')


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Mark integration tests and skip others if needed."""
    # Mark integration tests first
    for item in items:
        if item.path.is_relative_to(INTEGRATION_TEST_DIR):
            item.add_marker(pytest.mark.integration)

    # Skip tests if needed
    run_limited = config.getoption('--run-limited')
    disable_integration = config.getoption('--disable-integration')

    skip_limited = pytest.mark.skip(
        reason='This test has api limitations. Can be run with --run-limited option',
    )

    skip_integration = pytest.mark.skip(
        reason='This test is integration test. Can be run with --run-integration option',
    )

    for item in items:
        if not run_limited and 'limited' in item.keywords:
            item.add_marker(skip_limited)

        if disable_integration and 'integration' in item.keywords:
            item.add_marker(skip_integration)
