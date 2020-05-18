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

    equal_length = [
        len(item) for item in [
            lengths,
            hashed,
            sizes,
            fonts,
            distances,
            vertical,
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
        top_distance = utila.roundme(top_distance, digits=digits)
        bottom_distance = utila.roundme(bottom_distance, digits=digits)
        result.append(VerticalTextDistance(top_distance, bottom_distance))
    # last
    result.append(VerticalTextDistance(ypos[-2].bottom - ypos[-1].bottom, None))
    return result


def textlength(navigator) -> utila.Ints:
    return [len(item.text) for item in navigator]


def textsizes(navigator: texmex.PageTextNavigator) -> utila.Floats:
    assert isinstance(navigator, texmex.PageTextNavigator), type(navigator)
    collected = []
    for line in navigator:
        # determine most common text size
        fontsizes = utila.flatten([
            [char.size] * (char.end - char.start) for char in line.style.content
        ])
        collected.append(utila.mode(fontsizes, minimize=True))
    return collected


def textfonts(navigator: texmex.PageTextNavigator) -> utila.Ints:
    assert isinstance(navigator, texmex.PageTextNavigator), type(navigator)
    collected = []
    for line in navigator:
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
