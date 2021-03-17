# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import iamraw


def flatten(pages: iamraw.PageTextPropertiesList) -> iamraw.TextProperties:
    result = []
    for page in pages:
        for length, hashed, size, font, distance, ypos, left, right in zip(
                page.length,
                page.hashed,
                page.sizes,
                page.fonts,
                page.distances,
                page.ypos,
                page.left,
                page.right,
        ):
            result.append(
                iamraw.TextProperty(
                    length=length,
                    hashed=hashed,
                    size=size,
                    font=font,
                    before=distance.top,
                    after=distance.bottom,
                    top=ypos[0],
                    bottom=ypos[1],
                    left=left,
                    right=right,
                    page=page.page,
                ))
    return result


INVALID_CHAPTER = re.compile(
    r'(Kapitel|Chapter|Anhang|Appendix)[ ]{0,5}\d{1,2}$',
    re.IGNORECASE,
)
INVALID_APPENDIX = re.compile(
    r'(Anhang|Appendix)[ ]{0,5}[A-Z]$',
    re.IGNORECASE,
)


def invalid_headline(item: str) -> bool:
    """\
    >>> invalid_headline('KAPITEL  1 ')
    True
    >>> invalid_headline('Chapter 5 ')
    True
    >>> invalid_headline('ANHANG A')
    True
    """
    # TODO: STOLEN FROM WORDS
    item = item.strip()
    if INVALID_CHAPTER.match(item):
        return True
    if INVALID_APPENDIX.match(item):
        return True
    return False
