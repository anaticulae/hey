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
import dataclasses
import typing

import hey.textnavigator.navigator


@dataclasses.dataclass
class Abbreviation:
    short: str = None
    description: str = None


Abbreviations = typing.List[Abbreviation]


@dataclasses.dataclass
class AbbreviationData:
    content: hey.textnavigator.navigator.PageTextNavigators = None

    def __getitem__(self, index):
        return self.content[index]  # pylint:disable=E1136


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
