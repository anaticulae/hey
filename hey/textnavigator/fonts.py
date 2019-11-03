# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import dataclasses
import statistics
import typing

import iamraw
import utila

import hey.textnavigator
import hey.utils


@dataclasses.dataclass
class TextBounds:
    xdist: int
    ydist: int
    width: int
    height: int
    fontsize: int


@dataclasses.dataclass
class TextBoundsInfo:
    text: str
    bounds: TextBounds


TextBoundsList = typing.List[TextBoundsInfo]

FontSize = int
Occurrence = float
FontOccurrence = typing.Tuple[FontSize, Occurrence]
FontOccurrenceList = typing.List[FontOccurrence]


def fontdistance(bounds: typing.List[iamraw.BoundingBox]) -> typing.List[float]:
    """Describes the difference between two content lines"""
    distance = [
        utila.roundme(second.y0 - first.y1)
        for (first), (second) in zip(bounds[0:], bounds[1:])
    ]
    return distance


def feeddistance(bounds: typing.List[iamraw.BoundingBox]) -> typing.List[float]:
    """The text feed describes the distance from the left content border to
    the first content. The feeddistance describes the difference of two
    items"""
    distance = [
        utila.roundme(second.x0 - first.x0)
        for (first), (second) in zip(bounds[0:], bounds[1:])
    ]
    return distance


def fontdistance_textbounds(bounds: typing.List[TextBounds],
                           ) -> typing.List[float]:
    assert isinstance(bounds, list)
    assert all(isinstance(item, TextBounds) for item in bounds)
    distance = [
        utila.roundme(second.ydist - (first.ydist + first.height))
        for (first), (second) in zip(bounds[0:], bounds[1:])
    ]
    if bounds:
        # add distance from first content to page start
        # xdist, ydist(1), width, height, fontsize
        distance.insert(0, bounds[0].ydist)
    distance.append(0)  # TODO: CHECK AGAIN
    return distance


NONE_BORDER = iamraw.Border(None, None, None, None)


def bounds_to_textbounds(
        bounds: iamraw.BoundingBox,
        item: str,
        contentborder: iamraw.Border = None,
) -> TextBounds:
    """Compute distance to page `contentborder` and determine font size

    Args:
        bounds(iamraw.BoundingBox): BoundingBox of item
        item(str): content
        contenborder(Border): the border of page content if None (0,0) is used
    Returns:
        computed `TextBounds`
    """
    assert isinstance(item, str), type(item)
    if contentborder is None:
        contentborder = iamraw.Border(left=0, right=None, top=0, bottom=None)
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
    return TextBounds(xdist, ydist, width, height, fontsize)


def textbounds(
        navigator: 'PageTextNavigator',
        contentborder: iamraw.Border,
) -> TextBoundsList:
    assert hey.textnavigator.is_navigator(navigator), type(navigator)

    # ensure that order of items has no effect
    cb = contentborder  # pylint:disable=C0103
    __x0, __y0, __x1, __y1 = cb.left, cb.top, cb.right, cb.bottom
    if not navigator:
        return []

    result = [
        TextBoundsInfo(
            text=item.text,
            bounds=bounds_to_textbounds(
                item.bounding,
                item.text,
                contentborder,
            ),
        ) for item in navigator
    ]
    return result


def fontsizes(items: TextBoundsList) -> FontOccurrenceList:
    """Return a list of [fontsize, occurence] of the current page"""
    sizes = collections.defaultdict(int)
    for item in items:
        fontsize = item.bounds.fontsize
        chars = sum([len(item) for item in item.text])
        sizes[fontsize] += chars

    # TODO: move to general package
    common = sum(sizes.values())
    result = [(
        size,
        utila.roundme(occurence / common),
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


def textsizes_from_textbounds(
        navigator: 'PageTextNavigator',
        content: iamraw.Border,
) -> int:
    assert hey.textnavigator.is_navigator(navigator), type(navigator)
    text_bounds = textbounds(navigator, content.border)
    font_sizes = fontsizes(text_bounds)
    return font_sizes


def textsize_from_textbounds_common(
        navigator: 'PageTextNavigator',
        content: iamraw.Border,
) -> int:
    assert hey.textnavigator.is_navigator(navigator), type(navigator)
    result = textsizes_from_textbounds(navigator, content)
    return textsize(result)


def document_textsize(navigators, borders: typing.List[iamraw.Border]) -> int:
    """Determine the most common text size"""
    result = []
    for _, (navigator, contentborder) in hey.utils.sync([navigators, borders]):
        size = textsize_from_textbounds_common(navigator, contentborder)
        result.append(size)
    return result


def document_textsize_common(navigators,
                             borders: typing.List[iamraw.Border]) -> int:
    """Determine the most common text size"""
    result = document_textsize(navigators, borders)
    return statistics.mode(result)


def document_textdistance(navigators,
                          borders: typing.List[iamraw.Border]) -> int:
    """Determine the most common text distance"""
    result = []
    for _, (navigator, contentborder) in hey.utils.sync([navigators, borders]):
        bounds = textbounds(navigator, contentborder.border)
        # ignore empty content
        bounds = [item.bounds for item in bounds if len(item.text)]
        ydist = [item.ydist for item in bounds]
        height = [item.height for item in bounds]

        for yfirst, ysecond, firstheight in zip(
                ydist[:-1],
                ydist[1:],
                height[:-1],
        ):
            distance = ysecond - yfirst - firstheight
            result.append(distance)
    # TODO: is that right to have negative distances? see: example
    # howto_argparse.
    result = [item for item in result if item > 0]
    return statistics.mode(result)
