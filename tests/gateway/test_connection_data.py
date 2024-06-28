import pytest
from yarl import URL

from asyncord.gateway.client.client import ConnectionData
from asyncord.urls import GATEWAY_URL


@pytest.mark.parametrize('token', ['token', ''])
@pytest.mark.parametrize('resume_url', ['ws://localhost', ''])
@pytest.mark.parametrize('session_id', ['session_id', None])
@pytest.mark.parametrize('seq', [1, 0])
def test_can_resume(token: str, resume_url: str, session_id: str | None, seq: int) -> None:
    """Test checking if the connection can be resumed."""
    conn_data = ConnectionData(
        token=token,
        resume_url=URL(resume_url),
        session_id=session_id,
        seq=seq,
    )
    assert conn_data.can_resume is bool(resume_url and session_id and seq)


def test_reset() -> None:
    """Test resetting connection data."""
    conn_data = ConnectionData(
        token='token',  # noqa: S106
        resume_url=URL('ws://localhost'),
        session_id='session_id',
        seq=1,
    )
    conn_data.reset()

    assert conn_data.resume_url == GATEWAY_URL
    assert conn_data.session_id is None
    assert conn_data.seq == 0
