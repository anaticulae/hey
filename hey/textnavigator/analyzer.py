# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Text:
    Headline
    TOC
    Description
    Boxed Text
    ?SourceCode?


"""

import enum

import iamraw
import texmex

import words.boxed


class DocumentObjectType(enum.Enum):
    BOXED = enum.auto()
    DESCRIPTION = enum.auto()
    HEADLINE = enum.auto()
    IMAGE = enum.auto()
    INDEX = enum.auto()
    NOTHING = enum.auto()
    TABLE = enum.auto()
    TEXT = enum.auto()
    TOC = enum.auto()
    TEXTBOXED = enum.auto()
    UNDEFINED = enum.auto()


class DocumentObjectTyper:
    """This class enables to detect the `DocumentObjectType` of and
    textobject on a location on a given `page`. It is also possible to
    determine the confedence of this guess."""

    def __init__(
            self,
            textnavigators: texmex.PageTextNavigators,
            boxedchecker: words.boxed.BoxedChecker,
    ):
        self.boxedchecker = boxedchecker
        self.textnavigators = PageTextNavigatorsLookup(textnavigators)

    def what(self, page: int, bounds: iamraw.BoundingBox) -> DocumentObjectType:
        """Determine the underlaying `DocumentObjectType`"""
        is_box = self.boxedchecker.boxid(page, bounds) != words.boxed.NO_BOX
        is_text = self.textnavigators.text(page, bounds) is not None

        if is_text:
            if is_box:
                return DocumentObjectType.TEXTBOXED
            return DocumentObjectType.TEXT

        if is_box:
            return DocumentObjectType.BOXED

        return DocumentObjectType.UNDEFINED

    def confidence(self, page: int, bounds: iamraw.BoundingBox) -> float:
        return 1.0


class PageTextNavigatorsLookup:

    def __init__(self, textnavigators):
        self.data = {item.page: item for item in textnavigators}

    def text(self, page, bounds) -> str:
        try:
            return self.data[page].text(bounds)
        except KeyError:
            return None
