# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================h

from functools import partial

from sections.ctor import PERCENT_100
from sections.ctor import Appendix
from sections.ctor import Chapter
from sections.ctor import Content
from sections.ctor import Index
from sections.ctor import Introduction
from sections.ctor import Percentage
from sections.ctor import Position
from sections.ctor import Sections
from sections.ctor import Table
from sections.ctor import TableOfContent
from sections.ctor import Text
from sections.ctor import TitlePage
from sections.ctor import WhitePage


def _add_x(
        root: Sections,  # or DocumentSection
        pstart: Position,
        pend: Position,
        trust: Percentage,
        constructor,
):
    insert = constructor(start=pstart, end=pend, trust=trust)
    root.content.append(insert)
    return insert


#pylint:disable=C0103
add_table = partial(_add_x, constructor=Table)
add_introduction = partial(_add_x, constructor=Introduction)
add_content = partial(_add_x, constructor=Content)
add_appendix = partial(_add_x, constructor=Appendix)

add_title = partial(_add_x, constructor=TitlePage)
add_whitepage = partial(_add_x, constructor=WhitePage)
add_toc = partial(_add_x, constructor=TableOfContent)
add_index = partial(_add_x, constructor=Index)
add_text = partial(_add_x, constructor=Text)


def add_chapter(
        root: Content,
        pstart: float,
        pend: float,
        trust: Percentage = PERCENT_100,
        number: int = 0,
):

    insert = Chapter(
        start=pstart,
        end=pend,
        # start=[pstart, START],
        # end=[pend, END],
        trust=trust,
        number=number,
    )
    root.content.append(insert)
    return insert


def validate(document: Sections) -> bool:
    """Validate page order of `AreaSections`. A ascending order is required

    Args:
        document(Sections): to validate
    Returns:
        True if all page orders are correct, else False
    """
    # test of ascending page order
    start, end = -1, -1
    for section in document:
        if section.end < section.start:
            return False
        if section.start < start:
            return False
        if section.end < end:
            return False
        if not section.start == end + 1:
            return False

        start = section.start
        end = section.end
    return True
