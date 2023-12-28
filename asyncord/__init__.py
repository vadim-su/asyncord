"""A smart and powerful base for creating discord bots and interactin with the API.

Example:
::

    import asyncord

    if __name__ == '__main__':
        client = asyncord.RestClient('<YOUR_TOKEN_IS_HERE>')
        print(client.ping())
"""
import logging
from importlib import metadata

import pydantic
from rich.logging import RichHandler

package_metadata = metadata.metadata(__package__)
__version__ = package_metadata['version']
__url__ = package_metadata['project-url']
__author__ = package_metadata['author']


base_logger = logging.getLogger('asyncord')
base_logger.addHandler(RichHandler(
    rich_tracebacks=True,
    keywords=[],
    tracebacks_suppress=[pydantic]
))
base_logger.setLevel(logging.INFO)

del metadata, RichHandler, logging, pydantic, base_logger, package_metadata
