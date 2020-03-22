# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation
============

Examples:

* homework/page_50_math.pdf:page6
* master/page_116_images_toc_formular.pdf:95

TODO: Abbreviation creation tool
TODO: Symbol collector
"""

import abc
import contextlib
import dataclasses
import typing

import texmex
import texmex.alpha
import utila


# TODO: MOVE TO IAMRAW
@dataclasses.dataclass
class AbbreviationPosition:
    page: int = None
    sentence: int = None
    word: int = None


@dataclasses.dataclass
class Abbreviation:
    short: str = None
    description: str = None
    position: AbbreviationPosition = None

    def __lt__(self, item):
        return (texmex.alpha.replace(self.short).lower() <=
                texmex.alpha.replace(item.short).lower())


Abbreviations = typing.List[Abbreviation]


@dataclasses.dataclass
class AbbreviationData:
    normal: texmex.PageTextNavigators = None
    oneline: texmex.PageTextNavigators = None


@dataclasses.dataclass
class AbbreviationResult:

    abbreviations: Abbreviations = dataclasses.field(default_factory=list)

    def append(self, item):
        self.abbreviations.append(item)  # pylint:disable=E1101

    def __getitem__(self, index):
        return self.abbreviations[index]  # pylint:disable=E1136

    def __len__(self):
        return len(self.abbreviations)


class AbbreviationExtractorStrategy(abc.ABC):

    def __init__(self, loaded: AbbreviationData):
        self.loaded = loaded

    @abc.abstractmethod
    def result(self) -> AbbreviationResult:
        pass


def _dump_abbreviation(item) -> dict:
    assert isinstance(item, Abbreviation), type(item)
    position = item.position
    raw = {
        'short': item.short,
    }
    if item.description:
        raw['description'] = item.description
    if position:
        raw['position'] = f'{position.page} {position.sentence} {position.word}'
    return raw


def _load_abbreviation(raw: dict) -> Abbreviation:
    assert isinstance(raw, dict), type(raw)
    result = Abbreviation(short=raw['short'])
    with contextlib.suppress(KeyError):
        result.description = raw['description']
    with contextlib.suppress(KeyError):
        # TODO: REPLACE WITH UTILA>PARSE_TUPLE AFTER UPGRADING
        page, sentence, word = [int(item) for item in raw['position'].split()]
        result.position = AbbreviationPosition(
            page=page,
            sentence=sentence,
            word=word,
        )
    return result
