# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex
import utila

import textstyle


def parses(navigators: texmex.PageTextNavigators
          ) -> textstyle.PageTextPropertiesList:
    result = []
    for navigator in navigators:
        parsed = parse(navigator)
        result.append(parsed)
    return result


def parse(navigator: texmex.PageTextNavigator) -> textstyle.PageTextProperties:
    lengths = textlength(navigator)
    distances = textdistances(navigator)
    sizes = textsizes(navigator)
    fonts = textfonts(navigator)

    equal_length = [len(item) for item in [lengths, sizes, fonts, distances]]
    assert len(set(equal_length)) == 1, f'different iterator length {equal_length}' # yapf:disable

    return textstyle.PageTextProperties(lengths, sizes, fonts, distances)


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


def textdistances(navigator) -> utila.Floats:
    """Determine the most common text distance"""
    if not navigator:
        return []
    border = iamraw.Border(0, navigator.width, 0, navigator.height)
    bounds = texmex.textbounds(navigator, border)
    # ignore empty content
    bounds = [item.bounds for item in bounds if len(item.text)]
    ydist = [item.bottomdist for item in bounds]
    result = []
    for yfirst, ysecond in zip(ydist[:-1], ydist[1:]):
        distance = yfirst - ysecond
        result.append(distance)
    result.append(None)
    return result


def textlength(navigator) -> utila.Ints:
    return [len(item.text) for item in navigator]


def textsizes(navigator: texmex.PageTextNavigator) -> utila.Floats:
    assert isinstance(navigator, texmex.PageTextNavigator), type(navigator)
    collected = []
    for line in navigator:
        fontsizes = texmex.TextStyle.textsizes(
            line.style,
            method=lambda x: x,  # do not filter anything
        )
        collected.append(utila.mode(fontsizes, minimize=True))
    return collected


def textfonts(navigator: texmex.PageTextNavigator) -> utila.Ints:
    assert isinstance(navigator, texmex.PageTextNavigator), type(navigator)
    collected = []
    for line in navigator:
        family = [char.font for char in line.style]
        collected.append(utila.mode(family))
    return collected
