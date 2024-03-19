"""Gateway client errors."""


class BaseGatewayError(Exception):
    """Base class for all gateway errors."""


class ConnectionClosedError(BaseGatewayError):
    """Connection was closed."""

    def __init__(self) -> None:
        """Initialize the error."""
        super().__init__('Connection was closed')
