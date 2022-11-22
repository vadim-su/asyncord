class GatewayError(Exception):
    """Base exception class for all gateway errors."""

    def __init__(self, message: str, code: int | None = None):
        self.message = message
        self.code = code
        fmt_message = f' ({code}) {message}' if code else message
        super().__init__(fmt_message)


class HeartbeatAckTimeoutError(Exception):
    """Raised when the client does not receive a heartbeat ack in time."""

    def __init__(self, period: float):
        super().__init__(
            f'Did not receive a heartbeat ACK within the timeout period {period} s.',
        )


class InvalidSessionError(Exception):
    """Raised when the client receives an invalid session event."""

    def __init__(self, session_id: str):
        super().__init__(f"Session '{session_id}' is invalid")


class NecessaryReconnectError(Exception):
    """Raised when the client receives a reconnect event."""
