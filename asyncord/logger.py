import logging

import pydantic
from rich.logging import RichHandler


def setup_logging(name: str) -> None:
    base_logger = logging.getLogger(name)
    print(name)
    base_logger.addHandler(RichHandler(
        rich_tracebacks=True,
        keywords=[],
        tracebacks_suppress=[pydantic]
    ))
    base_logger.setLevel(logging.INFO)
