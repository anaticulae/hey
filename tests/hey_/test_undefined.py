# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from hey.undefined import extract_undefined
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_contentborder
from tests.fixtures.restruct import restructured_headerfooter
from tests.fixtures.restruct import restructured_headlines
from tests.fixtures.restruct import restructured_horizontals
from tests.fixtures.restruct import restructured_pagenumbers
from tests.fixtures.restruct import restructured_sizeandborder
from tests.fixtures.restruct import restructured_text
from tests.fixtures.restruct import restructured_textexample
from tests.fixtures.restruct import restructured_textpositions

# collected by reading the pdf file
RESTRUCTURED_NON_TEXTUAL_PAGE = 10


# pylint:disable=W0621
def test_extract_undefined(
        restructured_textexample,
        restructured_text,
        restructured_textpositions,
        restructured_contentborder,
):
    """Text replacing the undefined items with content"""
    # TODO: Move to hey
    extracted = extract_undefined(
        restructured_textexample,
        restructured_text,
        restructured_textpositions,
        restructured_contentborder,
    )
    assert extracted
    non_empty_pages = [item for item in extracted if item]

    assert len(non_empty_pages) == RESTRUCTURED_NON_TEXTUAL_PAGE
