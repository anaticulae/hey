# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Title page parser
=================

TODO: Introduce multiple extraction strategies
"""
import enum
import math

import texmex
import utila

# TODO: HOLY VALUE
MIN_TITLE_FONT_SIZE = 20


class TitleParserState(enum.Enum):
    DETECTED_SIZE = enum.auto()
    NOT_ENOUGH_LINES = enum.auto()
    NOT_ENOUGH_DISTANCE = enum.auto()
    TITLE_TO_SMALL = enum.auto()
    TITLE_BLACKLIST = enum.auto()


TITLE_BLACKLIST = {
    'STUDIENARBEIT',
    'BACHELORARBEIT',
    'MASTERARBEIT',
}


def parse(textnavigator: texmex.PageTextNavigator) -> str:
    """Parse hugest text line as title.

    Args:
        textnavigator(PageTextNavigator): given page to analyze text content
    Returns:
        parsed title if properties matches to given rules
        If not, return `TitleParserState` to indicate the problem

    Requirements for font parsing:
        - require at least 2 lines
        - size(headline) 120% of next line
        - title greater than `MIN_TITLE_FONT_SIZE`
    """
    merged = merge(textnavigator)
    sizes = determine_sizes(merged)

    if len(sizes) <= 2:
        return TitleParserState.NOT_ENOUGH_LINES

    sizes = sorted(sizes, reverse=True)

    detected_size = sizes[0][0]
    next_size = sizes[1][0]
    # Title size must be 20% greater
    if detected_size * 0.8 <= next_size:
        msg = ('title-detector: next following text font is to close: '
               f'detected({detected_size}) next({next_size})')
        utila.info(msg)
        return TitleParserState.NOT_ENOUGH_DISTANCE

    if detected_size < MIN_TITLE_FONT_SIZE:
        return TitleParserState.TITLE_TO_SMALL

    title = sizes[0][1].replace(utila.NEWLINE, ' ')
    title = title.strip()
    if title.upper() in TITLE_BLACKLIST:
        # bachelor
        return TitleParserState.TITLE_BLACKLIST
    return title


def merge(items):
    if not items:
        return []
    max_distance = 20  # TODO HOLY VALUE
    max_font_distance = 0.5  # TODO HOLY VALUE
    merged = [[items[0]]]
    for item in items[1:]:
        last = merged[-1][-1]
        distance = item.bounding[1] - last.bounding[3]
        split = any([
            distance > max_distance,
            fontdistance(last, item) > max_font_distance
        ])
        if split:
            merged.append([item])
        else:
            merged[-1].append(item)
    return merged


def determine_sizes(merged):
    result = []
    for group in merged:
        size = texmex.TextStyle.textsizes(group[0].style)
        text = '\n'.join([item.text for item in group])
        result.append((size, text))
    return result


def fontdistance(first, second) -> float:
    first = texmex.TextStyle.textsizes(first.style)
    second = texmex.TextStyle.textsizes(second.style)
    return math.fabs(first - second)
