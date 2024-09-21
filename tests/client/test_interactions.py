from typing import cast
from unittest.mock import AsyncMock

import pytest

from asyncord.client.http.headers import JSON_CONTENT_TYPE
from asyncord.client.http.models import FormPayload, JsonField, Response
from asyncord.client.interactions.models.common import InteractionResponseType
from asyncord.client.interactions.models.requests import (
    InteractionRespAutocompleteRequest,
    InteractionRespDeferredMessageRequest,
    InteractionRespMessageRequest,
    InteractionRespModalRequest,
    InteractionResponseRequestType,
    InteractionRespUpdateDeferredMessageRequest,
    InteractionRespUpdateMessageRequest,
)
from asyncord.client.interactions.resources import (
    InteractionResource,
)
from asyncord.client.messages.models.requests.components import TextInput
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.models.attachments import Attachment
from asyncord.client.users.models.responses import UserResponse
from asyncord.client.webhooks.models.requests import UpdateWebhookMessageRequest

TEST_ATTACHMENTS = [Attachment(content=b'png:...')]


_MOCK_RESP = Response(
    status=200,
    raw_body=b'{}',
    headers={},
    raw_response=AsyncMock(),
    body=MessageResponse(
        id='1234567890',  # type: ignore
        channel_id='1234567890',  # type: ignore
        author=UserResponse(
            id='1234567890',  # type: ignore
            username='username',
            discriminator='1234',
            global_name='global_name',
            avatar=None,
        ),
        content='Hello, World!',
        timestamp='2021-10-10T10:10:10.000000+00:00',  # type: ignore
        tts=False,
        mention_everyone=False,
        mentions=[],
        mention_roles=[],
        attachments=[],
        embeds=[],
        pinned=False,
        type=0,  # type: ignore
        flags=0,  # type: ignore
    ).model_dump(mode='json'),
)


@pytest.fixture
def interaction_res() -> InteractionResource:
    """Returns an instance of InteractionResource."""
    return InteractionResource(AsyncMock())


@pytest.mark.parametrize(
    'resp',
    [
        InteractionRespMessageRequest(content='Hello, World!'),
        InteractionRespUpdateMessageRequest(content='Hello, World!'),
        InteractionRespDeferredMessageRequest(content='Hello, World!'),
        InteractionRespUpdateDeferredMessageRequest(content='Hello, World!'),
        InteractionRespAutocompleteRequest(choices=[]),
        InteractionRespModalRequest(
            custom_id='1234567890',
            title='Title',
            components=TextInput(custom_id='1234567891', label='Label'),
        ),
    ],
)
async def test_send_not_pong_response(
    resp: InteractionResponseRequestType,
    interaction_res: InteractionResource,
) -> None:
    """Test send_response method of InteractionResource."""
    interaction_id = '1234567890'
    interaction_token = 'token'  # noqa: S105
    await interaction_res.send_response(interaction_id, interaction_token, resp)

    method_caller = cast(AsyncMock, interaction_res._http_client.post)
    method_caller.assert_called_once()

    request_url = method_caller.call_args.kwargs['url']
    payload = method_caller.call_args.kwargs['payload']

    assert str(request_url).endswith(f'/interactions/{interaction_id}/{interaction_token}/callback')
    assert payload['data'] == resp.model_dump(mode='json', exclude_none=True)
    assert payload.get('type')


async def test_send_pong(interaction_res: InteractionResource) -> None:
    """Test send pong response method of InteractionResource."""
    interaction_id = '1234567890'
    interaction_token = 'token'  # noqa: S105

    await interaction_res.send_pong(interaction_id, interaction_token)

    method_caller = cast(AsyncMock, interaction_res._http_client.post)
    method_caller.assert_called_once()

    request_url = method_caller.call_args.kwargs['url']
    payload = method_caller.call_args.kwargs['payload']

    assert str(request_url).endswith(f'/interactions/{interaction_id}/{interaction_token}/callback')
    assert payload == {'type': InteractionResponseType.PONG.value}


async def test_get_original_response(interaction_res: InteractionResource) -> None:
    """Test get original response method of InteractionResource."""
    application_id = '1234567890'
    interaction_token = 'token'  # noqa: S105

    method_caller = cast(AsyncMock, interaction_res._http_client.get)
    method_caller.return_value = _MOCK_RESP

    await interaction_res.get_original_response(application_id, interaction_token)
    method_caller.assert_called_once()

    request_url = method_caller.call_args.kwargs['url']

    assert str(request_url).endswith(f'/webhooks/{application_id}/{interaction_token}/messages/@original')


async def test_get_response(interaction_res: InteractionResource) -> None:
    """Test get response method of InteractionResource."""
    application_id = '1234567890'
    interaction_token = 'token'  # noqa: S105

    method_caller = cast(AsyncMock, interaction_res._http_client.get)
    method_caller.return_value = _MOCK_RESP

    await interaction_res.get_response(application_id, interaction_token, '1234567890')
    method_caller.assert_called_once()

    request_url = method_caller.call_args.kwargs['url']

    assert str(request_url).endswith(f'/webhooks/{application_id}/{interaction_token}/messages/1234567890')


async def test_update_origin_response(interaction_res: InteractionResource) -> None:
    """Test update original response method of InteractionResource."""
    application_id = '1234567890'
    interaction_token = 'token'  # noqa: S105

    method_caller = cast(AsyncMock, interaction_res._http_client.patch)
    method_caller.return_value = _MOCK_RESP

    await interaction_res.update_original_response(
        application_id,
        interaction_token,
        UpdateWebhookMessageRequest(content='Hello, World!'),
    )
    method_caller.assert_called_once()

    request_url = method_caller.call_args.kwargs['url']

    assert str(request_url).endswith(f'/webhooks/{application_id}/{interaction_token}/messages/@original')


async def test_update_response(interaction_res: InteractionResource) -> None:
    """Test update response method of InteractionResource."""
    application_id = '1234567890'
    interaction_token = 'token'  # noqa: S105

    method_caller = cast(AsyncMock, interaction_res._http_client.patch)
    method_caller.return_value = _MOCK_RESP

    await interaction_res.update_response(
        application_id,
        interaction_token,
        '1234567890',
        UpdateWebhookMessageRequest(content='Hello, World!'),
    )
    method_caller.assert_called_once()

    request_url = method_caller.call_args.kwargs['url']

    assert str(request_url).endswith(f'/webhooks/{application_id}/{interaction_token}/messages/1234567890')


async def test_delete_origin_response(interaction_res: InteractionResource) -> None:
    """Test delete original response method of InteractionResource."""
    application_id = '1234567890'
    interaction_token = 'token'  # noqa: S105

    method_caller = cast(AsyncMock, interaction_res._http_client.delete)

    await interaction_res.delete_original_response(application_id, interaction_token)
    method_caller.assert_called_once()

    request_url = method_caller.call_args.kwargs['url']

    assert str(request_url).endswith(f'/webhooks/{application_id}/{interaction_token}/messages/@original')


async def test_delete_response(interaction_res: InteractionResource) -> None:
    """Test delete response method of InteractionResource."""
    application_id = '1234567890'
    interaction_token = 'token'  # noqa: S105

    method_caller = cast(AsyncMock, interaction_res._http_client.delete)

    await interaction_res.delete_response(application_id, interaction_token, '1234567890')
    method_caller.assert_called_once()

    request_url = method_caller.call_args.kwargs['url']

    assert str(request_url).endswith(f'/webhooks/{application_id}/{interaction_token}/messages/1234567890')


@pytest.mark.parametrize(
    'resp',
    [
        InteractionRespMessageRequest(content='Hello, World!', attachments=TEST_ATTACHMENTS),
        InteractionRespUpdateMessageRequest(content='Hello, World!', attachments=TEST_ATTACHMENTS),
        InteractionRespDeferredMessageRequest(content='Hello, World!', attachments=TEST_ATTACHMENTS),
        InteractionRespUpdateDeferredMessageRequest(content='Hello, World!', attachments=TEST_ATTACHMENTS),
    ],
)
async def test_attachments_in_response(
    resp: InteractionResponseRequestType,
    interaction_res: InteractionResource,
) -> None:
    """Test attachments in response."""
    interaction_id = '1234567890'
    interaction_token = 'token'  # noqa: S105
    await interaction_res.send_response(interaction_id, interaction_token, resp)

    method_caller = cast(AsyncMock, interaction_res._http_client.post)
    method_caller.assert_called_once()

    request_url = method_caller.call_args.kwargs['url']
    payload = method_caller.call_args.kwargs['payload']

    assert str(request_url).endswith(f'/interactions/{interaction_id}/{interaction_token}/callback')
    assert isinstance(payload, FormPayload)

    (json_field_name, json_payload), (attachment_field_name, attachment) = payload

    assert isinstance(json_payload, JsonField)
    assert json_field_name == 'payload_json'
    assert json_payload.content_type == JSON_CONTENT_TYPE
    assert not json_payload.filename
    assert isinstance(json_payload.value, dict)
    assert json_payload.value.get('type')
    assert json_payload.value['data'] == resp.model_dump(mode='json', exclude_none=True)

    assert attachment_field_name == 'files[0]'
    assert not attachment.content_type
    assert not attachment.filename
    assert isinstance(attachment.value, bytes)
    assert attachment.value == TEST_ATTACHMENTS[0].content
