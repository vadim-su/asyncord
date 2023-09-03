"""Gateway exceptions."""


class GatewayError(Exception):
    """Base exception class for all gateway errors."""

    def __init__(self, message: str, code: int | None = None) -> None:
        """Initialize base gateway error.

        Args:
            message: Message of error.
            code: Code of error.
        """
        self.message = message
        self.code = code
        fmt_message = f' ({code}) {message}' if code else message
        super().__init__(fmt_message)


class HeartbeatAckTimeoutError(Exception):
    """Raised when the client does not receive a heartbeat ack in time."""


class InvalidSessionError(Exception):
    """Raised when the client receives an invalid session event."""

    def __init__(self, session_id: str):
        """Initialize invalid session error.

        Args:
            session_id: Session ID that is invalid.
        """
        super().__init__(f"Session '{session_id}' is invalid")


class NecessaryReconnectError(Exception):
    """Raised when the client receives a reconnect event."""
