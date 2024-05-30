#!/usr/bin/env python
"""Get the version of the package using git describe."""

import re
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Literal

from git import Repo


@dataclass
class Version:
    """Dataclass to represent a version."""

    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        """Return the version as a string."""
        return f'v{self.major}.{self.minor}.{self.patch}'


def get_version() -> str:
    """Get the version of the package using git describe.

    This method is used to get the version of the package.

    Returns:
        The version of the package.
    """
    repo = Repo(search_parent_directories=True)
    current_tag = get_current_tag(repo)
    if current_tag:
        return current_tag

    try:
        description = repo.git.describe(tags=True, long=True, match=r'v[0-9]*')
    except Exception as err:
        raise RuntimeError('No tags found. Please create a tag to get the version') from err

    tag, commit_count, commit_hash = description.rsplit('-', 2)
    return f'{tag}.dev{commit_count}+{commit_hash}'


def bump_version(part: Literal['major', 'minor', 'patch']) -> Version:
    """Bump the version of the package.

    Args:
        version: The current version of the package.
        part: The part of the version to bump.

    Returns:
        The new version of the package.
    """
    repo = Repo(search_parent_directories=True)
    version = _get_splite_version(repo)
    match part:
        case 'major':
            version = Version(version.major + 1, 0, 0)
        case 'minor':
            version = Version(version.major, version.minor + 1, 0)
        case 'patch':
            version = Version(version.major, version.minor, version.patch + 1)
        case _:
            raise ValueError(f'Invalid part: {part}')

    repo.create_tag(str(version))
    return version


def _get_splite_version(repo: Repo) -> Version:
    """Get the version of the package using git describe.

    Returns:
        The version of the package.
    """
    current_tag = get_current_tag(repo)
    if current_tag:
        return current_tag

    try:
        tag_version = repo.git.describe(tags=True, abbrev=0, match=r'v[0-9]*')
    except Exception:
        return Version(0, 0, 0)

    regex = r'v(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'
    match = re.match(regex, tag_version)

    return Version(
        major=int(match.group('major')),
        minor=int(match.group('minor')),
        patch=int(match.group('patch')),
    )


def get_current_tag(repo: Repo) -> str | None:
    """Get the current tag of the repository.

    Args:
        repo: The repository object.

    Returns:
        The current tag of the repository.
    """
    head = repo.head.commit
    for tag in repo.tags:
        if tag.commit == head:
            return tag.name
    return None


def cli() -> None:
    """CLI to get the version of the package."""
    parser = ArgumentParser(description='Get the version of the package')
    parser.add_argument('-b', '--bump', type=str, choices=['major', 'minor', 'patch'], help='Bump the version')
    args = parser.parse_args()

    if args.bump:
        version = bump_version(args.bump)
    else:
        version = get_version()

    print(version)  # noqa: T201


if __name__ == '__main__':
    cli()
