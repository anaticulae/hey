# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import typing


def is_navigator(item):
    import hey.textnavigator.navigator
    result = isinstance(item, (
        hey.textnavigator.navigator.PageTextNavigator,
        hey.textnavigator.navigator.PageTextContentNavigator,
    ))
    return result


@dataclasses.dataclass
class TextBounds:
    xdist: int
    ydist: int
    width: int
    height: int


@dataclasses.dataclass
class TextBoundsInfo:
    text: str
    bounds: TextBounds

    # TODO: Activate me for hunting bugs
    # def __post_init__(self):
    #     assert isinstance(self.bounds, TextBounds)


TextBoundsList = typing.List[TextBoundsInfo]

FontSize = int
Occurrence = float
FontOccurrence = typing.Tuple[FontSize, Occurrence]
FontOccurrences = typing.List[FontOccurrence]
