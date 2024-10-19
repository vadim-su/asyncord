#!/usr/bin/env python
"""Get the version of the package using git describe."""

import re
from argparse import ArgumentParser
from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal

from git import Repo

VERSION_REGEX = re.compile(
    r'v(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?P<suffix_name>((?:\.)?(dev|b|a|rc))(?P<suffix_value>\d+)?)?',
)
"""Regex to match the version."""


SUFFIX_RANK = MappingProxyType({
    'dev': 1,
    'a': 2,
    'b': 3,
    'rc': 4,
    None: 0,
})


ALLOWED_SUFFIX = MappingProxyType({
    'dev': 'dev',
    'a': 'a',
    'alpha': 'a',
    'b': 'b',
    'beta': 'b',
    'rc': 'rc',
})


@dataclass
class Version:
    """Dataclass to represent a version."""

    major: int
    minor: int
    patch: int
    suffix_name: Literal['dev', 'a', 'b', 'rc'] | None = None
    suffix_value: int = 0

    def __str__(self) -> str:
        """Return the version as a string."""
        version = f'v{self.major}.{self.minor}.{self.patch}'
        if not self.suffix_name:
            return version

        # If the suffix is dev, then add it to the version (e.g. v1.0.0.dev1)
        # Otherwise, add the suffix to the version (e.g. v1.0.0a1)
        # https://peps.python.org/pep-0440/#examples-of-compliant-version-schemes
        if self.suffix_name == 'dev':
            return f'{version}.{self.suffix_name}{self.suffix_value}'
        return f'{version}{self.suffix_name}{self.suffix_value}'


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


def bump_version(
    part_to_bump: Literal['major', 'minor', 'patch'] | None,
    suffix: Literal['dev', 'alpha', 'beta', 'rc'] | None,
) -> Version:
    """Bump the version of the package.

    Args:
        part_to_bump: The part of the version to bump.
        suffix: The suffix of the version.

    Returns:
        The new version of the package.
    """
    repo = Repo(search_parent_directories=True)
    version = _get_splite_version(repo)

    if suffix:
        if suffix not in ALLOWED_SUFFIX:
            raise ValueError(f'Invalid suffix: {suffix}')
        prep_suffix = ALLOWED_SUFFIX[suffix]
    else:
        prep_suffix = None

    if part_to_bump is None and prep_suffix:
        _validate_suffix_bump(version, prep_suffix)

    if part_to_bump:
        version = _get_new_version(version, part_to_bump)

    if prep_suffix:
        version.suffix_name = prep_suffix  # type: ignore
        version.suffix_value += 1

    repo.create_tag(str(version))
    return version


def _validate_suffix_bump(version: Version, suffix: str) -> None:
    """Validate if the suffix bump is allowed."""
    if not version.suffix_name:
        raise ValueError(
            'Cannot bump suffix without bumping main version part when current version has no suffix.',
        )
    if SUFFIX_RANK.get(suffix, -1) < SUFFIX_RANK.get(version.suffix_name, -1):
        raise ValueError(
            f'Cannot bump to a lower rank suffix: {suffix} from {version.suffix_name}',
        )


def _get_new_version(version: Version, part: str) -> Version:
    """Get the new version based on the part to bump."""
    increments = {
        'major': (version.major + 1, 0, 0),
        'minor': (version.major, version.minor + 1, 0),
        'patch': (version.major, version.minor, version.patch + 1),
    }
    if part not in increments:
        raise ValueError(f'Invalid part: {part}')
    return Version(*increments[part])


def _get_splite_version(repo: Repo) -> Version:
    """Get the version of the package using git describe.

    Returns:
        The version of the package.
    """
    current_tag = get_current_tag(repo)
    if current_tag:
        return _extract_version(current_tag)

    try:
        tag_version = repo.git.describe(tags=True, abbrev=0, match=r'v[0-9]*')
    except Exception:
        return Version(0, 0, 0)

    return _extract_version(tag_version)


def _extract_version(version: str) -> Version:
    """Extract the major, minor and patch version from the version.

    Args:
        version: The version to split.

    Returns:
        The version as a Version object.
    """
    match = VERSION_REGEX.match(version)
    if not match:
        raise ValueError(f'Invalid version: {version}')

    groups = match.groupdict()
    version_obj = Version(
        major=int(groups['major']),
        minor=int(groups['minor']),
        patch=int(groups['patch']),
    )
    if groups['suffix_name']:
        version_obj.suffix_name = groups['suffix_name']  # type: ignore
        version_obj.suffix_value = int(groups['suffix_value'])

    return version_obj


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
    parser.add_argument(
        '-s',
        '--suffix',
        type=str,
        choices=['dev', 'alpha', 'beta', 'rc'],
        help='Add or bump the suffix',
    )
    args = parser.parse_args()

    if args.bump or args.suffix:
        version = bump_version(args.bump, args.suffix)
    else:
        version = get_version()

    print(version)  # noqa: T201


if __name__ == '__main__':
    cli()
