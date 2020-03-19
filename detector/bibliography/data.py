# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""BibliographyReference
=====================

Sorting
-------

We sort by family name and as tybreaker by year. If no name is given, we
use `o. V. = ohne Verfasser` instead. If no year is given, we sort it
after the items with year.

# TODO: ADD OTHER SORTING AS THEISSEN recommends
"""

import contextlib
import dataclasses
import typing

import texmex.alpha
import utila
import yaml


@dataclasses.dataclass(unsafe_hash=True)
class BibliographyReference:

    reference: str = None
    data: str = None

    title: str = None
    year: int = None
    authors: typing.List[str] = dataclasses.field(default_factory=list)

    def __lt__(self, value):  # pylint:disable=too-many-return-statements
        """See rules in module doc `sorting`."""
        author = self.author if self.author else 'o. V.'
        value_author = value.author if value.author else 'o. V.'
        author = texmex.alpha.replace(author).lower()
        value_author = texmex.alpha.replace(value_author).lower()
        if author == value_author:
            if self.year is None:
                return False
            if value.year is None:
                return True
            return self.year < value.year
        return author < value_author

    @classmethod
    def create(cls, author: str, title: str = '', year: int = 2000):
        author = tuple(author.split(' ', maxsplit=1))
        with contextlib.suppress(TypeError):
            year = int(year)
        return cls(authors=[author], title=title, year=year)

    @property
    def author(self) -> str:
        """Return family of first author."""
        with contextlib.suppress(IndexError):
            return self.authors[0][0]  # pylint:disable=E1136
        return None


BibliographyReferences = typing.List[BibliographyReference]


def dump_bibliography_reference(references: BibliographyReferences) -> str:
    dumped = yaml.dump(references)
    return dumped


def load_bibliography_reference(content: str) -> BibliographyReferences:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)
    return loaded
