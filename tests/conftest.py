import os

import pytest


@pytest.fixture(scope='session')
def token():
    bot_token = os.environ.get('TOKEN')
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
