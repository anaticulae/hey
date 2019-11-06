# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================h

from functools import partial

from iamraw.sections import PERCENT_100
from iamraw.sections import Appendix
from iamraw.sections import Chapter
from iamraw.sections import Index
from iamraw.sections import Introduction
from iamraw.sections import MainPart
from iamraw.sections import Percentage
from iamraw.sections import Position
from iamraw.sections import Sections
from iamraw.sections import Table
from iamraw.sections import TableOfContent
from iamraw.sections import Text
from iamraw.sections import TitlePage
from iamraw.sections import WhitePage


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
add_content = partial(_add_x, constructor=MainPart)
add_appendix = partial(_add_x, constructor=Appendix)

add_title = partial(_add_x, constructor=TitlePage)
add_whitepage = partial(_add_x, constructor=WhitePage)
add_toc = partial(_add_x, constructor=TableOfContent)
add_index = partial(_add_x, constructor=Index)
add_text = partial(_add_x, constructor=Text)


def add_chapter(
        root: MainPart,
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
