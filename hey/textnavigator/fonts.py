# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from collections import defaultdict
from statistics import mode
from typing import List
from typing import Tuple

from iamraw import Border
from iamraw import BoundingBox
from utila import roundme

from hey.utils import sync

# TODO: rejoin with newer python
# from hey.textnavigator.navigator import PageTextNavigator

# (xdist, ydist, width, height, fontsize)
TextBounds = Tuple[int, int, int, int, int]
TextBoundsList = List[Tuple[TextBounds, str]]

FontSize = int
Occurrence = float
FontOccurrence = Tuple[FontSize, Occurrence]
FontOccurrenceList = List[FontOccurrence]


def fontdistance(bounds: List[BoundingBox]) -> List[float]:
    """Describes the difference between two content lines"""
    distance = [
        roundme(second.y0 - first.y1)
        for (first), (second) in zip(bounds[0:], bounds[1:])
    ]
    return distance


def feeddistance(bounds: List[BoundingBox]) -> List[float]:
    """The text feed describes the distance from the left content border to
    the first content. The feeddistance describes the difference of two
    items"""
    distance = [
        roundme(second.x0 - first.x0)
        for (first), (second) in zip(bounds[0:], bounds[1:])
    ]
    return distance


def fontdistance_textbounds(bounds: TextBoundsList) -> List[float]:
    distance = [
        roundme(second[1] - (first[1] + first[3]))
        for (first), (second) in zip(bounds[0:], bounds[1:])
    ]
    if bounds:
        # add distance from first content to page start
        # xdist, ydist(1), width, height, fontsize
        distance.insert(0, bounds[0][1])
    distance.append(0)  # TODO: CHECK AGAIN
    return distance


NONE_BORDER = Border(None, None, None, None)


def bounds_to_textbounds(
        bounds: BoundingBox,
        item: str,
        contentborder: Border = None,
) -> TextBounds:
    """Compute distance to page `contentborder` and determine font size

    Args:
        bounds(BoundingBox): BoundingBox of item
        item(str): content
        contenborder(Border): the border of page content if None (0,0) is used
    Returns:
        computed `TextBounds`
    """
    assert isinstance(item, str), type(item)
    if contentborder is None:
        contentborder = Border(left=0, right=None, top=0, bottom=None)
    x0, y0, x1, y1 = bounds
    lines = len(item.splitlines())
    xdist, ydist, width, height, fontsize = (
        int(x0 - contentborder.left),
        int(y0 - contentborder.top),
        int(x1 - x0),
        int(y1 - y0),
        int((y1 - y0) / lines) if lines else 0,
        # TODO: Improve font size calculation
    )
    return (xdist, ydist, width, height, fontsize)


def textbounds(
        navigator: 'PageTextNavigator',
        contentborder: Border,
) -> TextBoundsList:
    # ensure that order of items has no effect
    cb = contentborder  # pylint:disable=C0103
    __x0, __y0, __x1, __y1 = cb.left, cb.top, cb.right, cb.bottom
    if not navigator:
        return []
    result = [(bounds_to_textbounds(bounds, item, contentborder), item)
              for (bounds, item) in navigator]
    return result


def fontsize_from_textbounds(textbound: TextBounds) -> int:
    # TODO: WE NEED THE TEXT DISTANCE OF EVERY LINE
    # xdist
    # ydist
    # width
    # height
    # fontsize
    return textbound[4]


def textfeed(item: TextBounds) -> int:
    """The textfeed describes the distances from left content border to start
    of text.

    Args:
        textbounds(TextBounds):
    Returns:
        distance to content border
    """
    return item[0]


def fontsizes(items: TextBoundsList) -> FontOccurrenceList:
    """Return a list of [fontsize, occurence] of the current page"""
    sizes = defaultdict(int)
    for bounds, text in items:
        fontsize = fontsize_from_textbounds(bounds)
        chars = sum([len(item) for item in text])
        sizes[fontsize] += chars

    # TODO: move to general package
    common = sum(sizes.values())
    result = [(
        size,
        roundme(occurence / common),
    ) for size, occurence in sizes.items()]
    return result


def textsize(occurrences: FontOccurrenceList) -> int:
    """Compute size of text"""
    mostly = sorted(occurrences, key=lambda item: item[1], reverse=True)
    if not mostly:
        return None
    most_font_item = mostly[0]
    size = most_font_item[0]
    return size


def textsize_from_textbounds(
        navigator: 'PageTextNavigator',
        content: Border,
) -> int:
    text_bounds = textbounds(navigator, content.border)
    font_sizes = fontsizes(text_bounds)
    return textsize(font_sizes)


def document_textsize(navigators, borders: List[Border]) -> int:
    """Determine the most common text size"""
    result = []
    for _, (navigator, contentborder) in sync([navigators, borders]):
        size = textsize_from_textbounds(navigator, contentborder)
        result.append(size)
    return mode(result)


def document_textdistance(navigators, borders: List[Border]) -> int:
    """Determine the most common text distance"""
    result = []
    for _, (navigator, contentborder) in sync([navigators, borders]):
        bounds = textbounds(navigator, contentborder.border)
        # ignore empty content
        bounds = [item[0] for item in bounds if len(item[1])]
        ydist = [item[1] for item in bounds]
        height = [item[3] for item in bounds]

        for yfirst, ysecond, firstheight in zip(
                ydist[:-1],
                ydist[1:],
                height[:-1],
        ):
            distance = ysecond - yfirst - firstheight
            result.append(distance)
    return mode(result)
