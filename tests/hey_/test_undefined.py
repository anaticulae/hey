# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from hey.undefined import extract_undefined
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_headlines
from tests.fixtures.restruct import restructured_sizeandborder
from tests.fixtures.restruct import restructured_text
from tests.fixtures.restruct import restructured_text_positions
from tests.fixtures.restruct import restructured_textexample

# collected by reading the pdf file
RESTRUCTURED_NON_TEXTUAL_PAGE = 10


# pylint:disable=W0621
def test_extract_undefined(
        restructured_sizeandborder,
        restructured_text,
        restructured_text_positions,
        restructured_textexample,
):
    """Text replacing the undefined items with content"""
    _, border = restructured_sizeandborder
    # TODO: Move to hey
    extracted = extract_undefined(
        restructured_textexample,
        restructured_text,
        restructured_text_positions,
        border,
    )
    assert extracted
    non_empty_pages = [item for item in extracted if item]
    assert len(non_empty_pages) == RESTRUCTURED_NON_TEXTUAL_PAGE, str(extracted)
