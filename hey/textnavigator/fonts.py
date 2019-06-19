# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from collections import defaultdict
from typing import List
from typing import Tuple

from iamraw import Border
from iamraw import BoundingBox

# TODO: rejoin with newer python
# from hey.textnavigator.navigator import PageTextNavigator

TextBounds = Tuple[int, int, int, int, int]
TextBoundsList = List[Tuple[TextBounds, str]]

FontSize = int
Occurrence = float
FontOccurrence = Tuple[FontSize, Occurrence]
FontOccurrenceList = List[FontOccurrence]


def fontdistance(bounds: List[BoundingBox]) -> List[float]:
    distance = [
        round(first.y_bottom - second.y_top, 2)
        for (first), (second) in zip(bounds[0:], bounds[1:])
    ]
    return distance


def textbounds(
        navigator: 'PageTextNavigator',
        contentborder: Border,
) -> TextBoundsList:
    __x0, __y0, __x1, __y1 = contentborder

    result = []
    for (x0, y0, x1, y1), item in navigator:
        lines = len(item.splitlines())
        xdist, ydist, width, height, fontsize = (
            int(x0 - __x0),
            int(__y1 - y1),
            int(x1 - x0),
            int(y1 - y0),
            int((y1 - y0) / lines) if lines else 0,
            # TODO: Improve font size calculation
        )
        result.append(((xdist, ydist, width, height, fontsize), item))
    return result


def fontsize_from_textbounds(textbound: TextBounds) -> int:
    # TODO: WE NEED THE TEXT DISTANCE OF EVERY LINE
    # xdist
    # ydist
    # width
    # height
    # fontsize
    return textbound[4]


def textfeed(textbounds: TextBounds) -> int:
    """The textfeed describes the distances from left content border to start
    of text.

    Args:
        textbounds(TextBounds):
    Returns:
        distance to content border
    """
    return textbounds[0]


def fontsizes(textbounds: TextBoundsList) -> FontOccurrenceList:
    """Return a list of [fontsize, occurence] of the current page"""
    sizes = defaultdict(int)
    for bounds, text in textbounds:
        fontsize = fontsize_from_textbounds(bounds)
        chars = sum([len(item) for item in text])
        sizes[fontsize] += chars

    # TODO: move to general package
    common = sum(sizes.values())
    result = [(
        size,
        round(occurence / common, 2),
    ) for size, occurence in sizes.items()]
    return result


def textsize(occurrences: FontOccurrenceList) -> int:
    """Compute size of text"""
    mostly = sorted(occurrences, key=lambda item: item[1], reverse=True)
    most_font_item = mostly[0]
    size = most_font_item[0]
    return size


def textsize_from_textbounds(
        navigator: 'PageTextNavigator',
        contentborder: Border,
) -> int:
    text_bounds = textbounds(navigator, contentborder)
    font_sizes = fontsizes(text_bounds)
    return textsize(font_sizes)
