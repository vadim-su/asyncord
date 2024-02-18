class BaseGatewayError(Exception):
    """Base class for all gateway errors."""


class ConnectionClosed(BaseGatewayError):
    """Connection was closed."""

    def __init__(self):
        super().__init__('Connection was closed')
