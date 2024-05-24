from asyncord.client.channels.resources import ChannelResource
from asyncord.client.invites.resources import InvitesResource
from tests.conftest import IntegrationTestData

CHANNEL_NAME = 'test'


async def test_create_get_delete_channel_invite(
    channel_res: ChannelResource,
    invite_res: InvitesResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test creating channel invite, get invite, delete invite."""
    invite = await channel_res.create_channel_invite(integration_data.channel_id)
    assert invite.code

    invite_response = await invite_res.get_invite(invite.code)

    assert invite_response.code == invite.code

    deleted_invite = await invite_res.delete_invite(invite.code)

    assert deleted_invite.code == invite.code
