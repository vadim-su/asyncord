import logging

import pydantic
from rich.logging import RichHandler

_base_logger = logging.getLogger('asyncord')
_base_logger.addHandler(RichHandler(
    rich_tracebacks=True,
    keywords=[],
    tracebacks_suppress=[pydantic]
))
