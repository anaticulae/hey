# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
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

BLACK_CHAPTER = re.compile(r'(Kapitel|Chapter|Anhang|Appendix)[ ]{0,5}\d{1,2}$', re.IGNORECASE) # yapf:disable
BLACK_APPENDIX = re.compile(r'(Anhang|Appendix)[ ]{0,5}[A-Z]$', re.IGNORECASE)


def headline_blacklisted(item: str) -> bool:
    """\
    >>> headline_blacklisted('KAPITEL  1 ')
    True
    >>> headline_blacklisted('Chapter 5 ')
    True
    >>> headline_blacklisted('ANHANG A')
    True
    """
    # TODO: STOLEN FROM WORDS
    item = item.strip()
    if BLACK_CHAPTER.match(item):
        return True
    if BLACK_APPENDIX.match(item):
        return True
    return False
