# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import typing

import iamraw
import texmex
import utila

import doctextstyle
import doctextstyle.data

VerticalTextDistance = collections.namedtuple(
    'VerticalTextDistance',
    'top, bottom',
)
VerticalTextDistances = typing.List[VerticalTextDistance]


def parses(navigators: texmex.PageTextNavigators,
          ) -> doctextstyle.data.PageTextPropertiesList:
    result = []
    for navigator in navigators:
        parsed = parse(navigator)
        result.append(parsed)
    return result


def parse(navigator: texmex.PageTextNavigator,
         ) -> doctextstyle.data.PageTextProperties:
    lengths = textlength(navigator)
    hashed = [item.text.strip() for item in navigator]
    distances = textdistances(navigator)
    sizes = textsizes(navigator)
    fonts = textfonts(navigator)
    vertical = vertical_position(navigator)
    left, right = leftright(navigator)

    equal_length = [
        len(item) for item in [
            lengths,
            hashed,
            sizes,
            fonts,
            distances,
            vertical,
            left,
            right,
        ]
    ]
    assert len(set(equal_length)) == 1, f'different iter length {equal_length}'

    result = doctextstyle.data.PageTextProperties(
        lengths,
        hashed,
        sizes,
        fonts,
        distances,
        vertical,
        left,
        right,
    )
    return result


def document_textdistance(navigators) -> float:
    """Determine the most common text distance"""
    result = []
    for navigator in navigators:
        if not navigator:
            # empty page
            continue
        page_textdistances = textdistances(navigator)
        result.extend(page_textdistances)
    mode = utila.modes(result)
    return mode


def textdistances(navigator, digits: int = 1) -> VerticalTextDistances:
    # TODO: MOVE TO TEXMEX
    if not navigator:
        return []
    if len(navigator) == 1:
        # no predecessor and successor
        return [VerticalTextDistance(None, None)]
    ypos = vertical_position(navigator)

    # first
    result = [VerticalTextDistance(None, ypos[0].bottom - ypos[1].bottom)]
    for before, current, after in zip(ypos[0:-2], ypos[1:-1], ypos[2:]):
        # middles
        top_distance = before.bottom - current.bottom
        bottom_distance = current.bottom - after.bottom
        result.append(VerticalTextDistance(top_distance, bottom_distance))
    # last
    result.append(VerticalTextDistance(ypos[-2].bottom - ypos[-1].bottom, None))

    # round to have propper user output/developer handling
    rounded = round_vertical_distances(result, digits=digits)
    return rounded


def round_vertical_distances(items, digits: int = 1):
    """Round list of `VerticalTextDistances`.

    >>> round_vertical_distances([VerticalTextDistance(1.333, None), VerticalTextDistance(5.88, 5.0)])
    [VerticalTextDistance(top=1.3, bottom=None), VerticalTextDistance(top=5.9, bottom=5.0)]
    """
    result = []
    for item in items:
        before = utila.roundme(
            item[0],
            digits=digits,
        ) if item[0] is not None else None
        after = utila.roundme(
            item[1],
            digits=digits,
        ) if item[1] is not None else None
        result.append(VerticalTextDistance(before, after))

    return result


def textlength(navigator) -> utila.Ints:
    return [len(item.text) for item in navigator]


def textsizes(navi: texmex.NavigatorMixin) -> utila.Floats:
    assert issubclass(navi.__class__, texmex.NavigatorMixin), type(navi)
    collected = []
    for line in navi:
        # determine most common text size
        fontsizes = utila.flatten([
            [char.size] * (char.end - char.start) for char in line.style.content
        ])
        collected.append(utila.mode(fontsizes, minimize=True))
    return collected


def textfonts(navi: texmex.NavigatorMixin) -> utila.Ints:
    assert issubclass(navi.__class__, texmex.NavigatorMixin), type(navi)
    collected = []
    for line in navi:
        family = [char.font for char in line.style]
        collected.append(utila.mode(family))
    return collected


def vertical_position(navigator) -> VerticalTextDistances:
    if not navigator:
        return []
    border = iamraw.Border(0, navigator.width, 0, navigator.height)
    bounds = texmex.textbounds(navigator, border)
    # ignore empty content
    bounds = [item.bounds for item in bounds if len(item.text)]
    dist = [
        VerticalTextDistance(
            item.topdist,
            item.bottomdist,
        ) for item in bounds
    ]
    return dist


def leftright(navigator) -> VerticalTextDistances:
    if not navigator:
        return [], []
    # ignore empty content
    border = iamraw.Border(0, navigator.width, 0, navigator.height)
    bounds = texmex.textbounds(navigator, border)
    bounds = [item.bounds for item in bounds if len(item.text)]
    left = [item.leftdist for item in bounds]
    right = [item.rightdist for item in bounds]
    return left, right
