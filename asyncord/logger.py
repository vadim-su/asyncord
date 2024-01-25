import logging
from typing import Any, MutableMapping

import pydantic
from rich.logging import RichHandler


def setup_logging(name: str) -> None:
    base_logger = logging.getLogger(name)
    base_logger.addHandler(RichHandler(
        rich_tracebacks=True,
        keywords=[],
        tracebacks_suppress=[pydantic]
    ))
    base_logger.setLevel(logging.INFO)


class NameLoggerAdapter(logging.LoggerAdapter):
    """LoggerAdapter that adds the entity name to the log message."""

    def __init__(self, logger: logging.Logger, name: str) -> None:
        super().__init__(logger, {'entity_name': name, 'markup': True})
        self.entity_name = name

    def process(self, msg: str, kwargs: MutableMapping[str, Any]) -> tuple[str, MutableMapping[str, Any]]:
        msg, kwargs = super().process(msg, kwargs)
        return f'[bold]<{self.entity_name}>[/] {msg}', kwargs
