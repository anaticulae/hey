# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
* Introduction
    * Titlepage
    * Thank you
    * Copyright etc.
    * Erklaerung
* Table-Area
    * Table of content
    * Short cuts
    * Figure table
* Content
    * Chapter
        * Figure
        * Text
        * Headlines
* Table-Area-B
* Appendix
    * Resources
    * Link
    * Literature
"""

from sections.ctor import Sections


# TODO: define interface
def extract_sections() -> Sections:
    result = Sections()

    return result


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
