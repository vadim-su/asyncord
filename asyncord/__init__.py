"""
A smart and powerful base for creating discord bots and interactin with the API.

Example:
::

    import asyncord

    if __name__ == '__main__':
        client = asyncord.RestClient('<YOUR_TOKEN_IS_HERE>')
        print(client.ping())
"""
from importlib import metadata

metadata = metadata.metadata(__package__)
__version__ = metadata['version']
__url__ = metadata['project-url']
__author__ = metadata['author']

del metadata
