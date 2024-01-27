from pydantic import AnyUrl, BaseModel


class ConnectionData(BaseModel):
    """Data used to connect or resume to the gateway."""

    token: str
    """Token used to connect to the gateway."""

    resume_url: AnyUrl | None = None
    """URL used to resume a previous session."""

    session_id: str | None = None
    """ID of the previous session."""

    seq: int = 0
    """Sequence number of the previous message."""

    @property
    def should_resume(self) -> bool:
        return all((self.resume_url, self.session_id, self.seq))
