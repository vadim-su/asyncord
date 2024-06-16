from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from asyncord.client_hub import ClientHub


async def test_setup_single_client_group(mocker: MockerFixture) -> None:
    """Test setup_single_client_group method."""
    mock_gather = mocker.patch('asyncio.gather', new=mocker.async_stub('gather'))
    mock_client_group_class = mocker.patch('asyncord.client_hub.ClientGroup')

    async with ClientHub.setup_single_client_group(auth='token', session=Mock()) as client_group:
        mock_client_group_class.assert_called_once()
        mock_client_group = mock_client_group_class.return_value
        assert client_group is mock_client_group

    mock_gather.assert_called_once()
    mock_client_group.connect.assert_called_once()


async def test_create_client_group(mocker: MockerFixture) -> None:
    """Test creation of a client group."""
    mock_client_group_class = mocker.patch('asyncord.client_hub.ClientGroup')
    hub = ClientHub(session=Mock())
    hub.create_client_group('group_name', 'token')

    mock_client_group_class.assert_called_once()

    with pytest.raises(ValueError, match=r'Client group group_name already exists'):
        hub.create_client_group('group_name', auth='token')
