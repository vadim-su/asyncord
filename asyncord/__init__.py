"""A smart and powerful base for creating discord bots and interactin with the API.

Example:
::

    import asyncord

    if __name__ == '__main__':
        client = asyncord.RestClient('<YOUR_TOKEN_IS_HERE>')
        print(client.ping())
"""

from importlib import metadata

from asyncord.logger import setup_logging

# Set package metadata
package_metadata = metadata.metadata(__package__)
__version__ = package_metadata.get('version')
__url__ = package_metadata.get('project-url')
__author__ = package_metadata.get('author')


# Setup logging
setup_logging(__package__)


del metadata, setup_logging, package_metadata
