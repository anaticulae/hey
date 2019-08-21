# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from enum import Enum
from enum import auto

import utila

from hey.textnavigator.fonts import bounds_to_textbounds
from hey.textnavigator.fonts import fontsize_from_textbounds
from hey.textnavigator.navigator import PageTextNavigator

# TODO: HOLY VALUE
MIN_TITLE_FONT_SIZE = 20


class TitleParserState(Enum):
    DETECTED_SIZE = auto()
    NOT_ENOUGH_LINES = auto()
    NOT_ENOUGH_DISTANCE = auto()
    TITLE_TO_SMALL = auto()


def parse(textnavigator: PageTextNavigator) -> str:
    """Parse hugest text line as title.

    Requirements for font parsing:
        - require at least 2 lines
        - size(headline) 120% of next line
        - title greater than `MIN_TITLE_FONT_SIZE`

    Args:
        textnavigator(PageTextNavigator):
    Returns:
        parsed title if properties matches to given rules
        If not, return `TitleParserState` to indicate the problem
    """
    sizes = []
    for bounds, text in textnavigator:
        textbounds = bounds_to_textbounds(
            bounds,
            text,
        )
        fontsize = fontsize_from_textbounds(textbounds)
        sizes.append((fontsize, text))

    sizes = sorted(sizes, reverse=True)

    if len(sizes) <= 2:
        return TitleParserState.NOT_ENOUGH_LINES

    detected_size = sizes[0][0]
    next_size = sizes[1][0]

    # Title size must be 20% greater
    if detected_size * 0.8 <= next_size:
        return TitleParserState.NOT_ENOUGH_DISTANCE

    if detected_size < MIN_TITLE_FONT_SIZE:
        return TitleParserState.TITLE_TO_SMALL

    title = sizes[0][1].replace(utila.NEWLINE, ' ')
    title = title.strip()
    return title
