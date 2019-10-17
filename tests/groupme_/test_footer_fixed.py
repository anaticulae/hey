# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw
import utila

import groupme.footer.fixed
import tests.resources


def _restructed():
    horizontals = tests.resources.horizontals(tests.resources.RESTRUCT)
    horizontals = serializeraw.load_horizontals(horizontals)

    sizeandborder = tests.resources.sizeandborder(tests.resources.RESTRUCT)
    sizeandborder = serializeraw.load_pageborders(sizeandborder)

    pageheight = utila.select_page(sizeandborder, 0).size.height

    top, bottom = groupme.footer.fixed.extract_common_footer(
        horizontals=horizontals,
        pageheight=pageheight,
    )
    return horizontals, pageheight, top, bottom


def test_groupme_footer_fixed_restructed_extract_common_footer():
    _, __, top, bottom = _restructed()
    assert top  # document has header
    assert bottom  # document has footer
    assert top < bottom


def test_groupme_footer_fixed_restructed_extract_page_footerheader():
    horizontals, pageheight, top, bottom = _restructed()

    extracted = groupme.footer.fixed.extract_page_footerheader(
        horizontals,
        top,
        bottom,
        pageheight,
    )
    allfooter = [
        item.footer is not None for item in extracted if item.page >= 2
    ]
    assert all(allfooter), utila.log_raw(allfooter)


def _bachelor111():
    horizontals = tests.resources.horizontals(tests.resources.BACHELOR_111PAGES)
    horizontals = serializeraw.load_horizontals(horizontals)

    sizeandborder = tests.resources.sizeandborder(tests.resources.BACHELOR_111PAGES)  #yapf:disable
    sizeandborder = serializeraw.load_pageborders(sizeandborder)
    pageheight = utila.select_page(sizeandborder, 0).size.height

    top, bottom = groupme.footer.fixed.extract_common_footer(
        horizontals=horizontals,
        pageheight=pageheight,
    )
    return horizontals, pageheight, top, bottom


def test_groupme_footer_fixed_bachelor111page_extract_common_footer():
    _, __, top, bottom = _bachelor111()
    assert top  # document has header
    assert bottom  # document has footer
    assert top < bottom


@pytest.mark.xfail(reason='header collector is not good enough')
def test_groupme_footer_fixed_bachelor111page_extract_page_footerheader():
    horizontals, pageheight, top, bottom = _bachelor111()

    extracted = groupme.footer.fixed.extract_page_footerheader(
        horizontals,
        top,
        bottom,
        pageheight,
    )
    header = [item.header for item in extracted if item.header]
    assert len(header) == 94, utila.log_raw(header)
