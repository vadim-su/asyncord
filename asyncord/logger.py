"""Logging utilities for asyncord."""

import logging
from collections.abc import MutableMapping
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from typing import Any

import pydantic
from rich.logging import RichHandler


def setup_logging(name: str) -> None:
    """Set up logging for the given name.

    Args:
        name: Name of the logger.
    """
    log_queue = Queue()
    queue_handler = QueueHandler(log_queue)

    rich_handler = RichHandler(
        rich_tracebacks=True,
        keywords=[],
        tracebacks_suppress=[pydantic],
    )

    listener = QueueListener(log_queue, rich_handler)
    listener.start()
    base_logger = logging.getLogger(name)

    base_logger.addHandler(queue_handler)
    base_logger.setLevel(logging.INFO)


class NameLoggerAdapter(logging.LoggerAdapter):
    """LoggerAdapter that adds the entity name to the log message."""

    def __init__(self, logger: logging.Logger, name: str) -> None:
        """Initialize the NameLoggerAdapter.

        Args:
            logger: Logger to adapt.
            name: Name of the entity.
        """
        super().__init__(logger, {'entity_name': name, 'markup': True})
        self.entity_name = name

    def process(self, msg: str, kwargs: MutableMapping[str, Any]) -> tuple[str, MutableMapping[str, Any]]:
        """Process the log message and add the entity name to it.

        Args:
            msg: Log message.
            kwargs: Keyword arguments for the log message.

        Returns:
            Tuple containing the formatted log message and the keyword arguments.
        """
        msg, kwargs = super().process(msg, kwargs)
        return f'[bold]<{self.entity_name}>[/] {msg}', kwargs
