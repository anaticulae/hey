# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import itertools

import iamraw
import iamraw.path
import power
import serializeraw
import utila
import utilatest

import groupme.footer.strategy as gfs
import groupme.footer.strategy.fixed as gfsf
import tests.resources


def _restructed():
    horizontals = iamraw.path.horizontals(power.link(power.DOCU27_PDF))
    horizontals = serializeraw.load_horizontals(horizontals)

    sizeandborder = iamraw.path.sizeandborder(power.link(power.DOCU27_PDF))
    sizeandborder = serializeraw.load_pageborders(sizeandborder)

    pageheight = utila.select_page(sizeandborder, 0).size.height

    navigators = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.DOCU27_PDF))
    top, bottom = gfsf.extract_common_footer(
        horizontals=horizontals,
        pageheight=pageheight,
    )
    return horizontals, pageheight, top, bottom, navigators


def test_groupme_footer_fixed_restructed_extract_common_footer():
    _, __, top, bottom, ___ = _restructed()
    assert top  # document has header
    assert bottom  # document has footer
    assert top < bottom


def test_groupme_footer_fixed_restructed_extract_page_footerheader():
    horizontals, pageheight, top, bottom, pagetextnavigators = _restructed()
    top, bottom = top[0], bottom[0]
    extracted = gfsf.extract_page_footerheader(
        horizontals,
        top,
        bottom,
        pageheight,
        pagetextnavigators,
    )
    allfooter = [
        item.footer is not None for item in extracted if item.page >= 2
    ]
    assert all(allfooter), utila.log_raw(allfooter)


def _bachelor111():
    horizontals = iamraw.path.horizontals(power.link(power.BACHELOR111_PDF))
    horizontals = serializeraw.load_horizontals(horizontals)

    sizeandborder = iamraw.path.sizeandborder(power.link(power.BACHELOR111_PDF))
    sizeandborder = serializeraw.load_pageborders(sizeandborder)
    pageheight = utila.select_page(sizeandborder, 0).size.height

    navigators = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.BACHELOR111_PDF),
        prefix='oneline',
    )

    top, bottom = gfsf.extract_common_footer(
        horizontals=horizontals,
        pageheight=pageheight,
    )
    return horizontals, pageheight, top, bottom, navigators


def _bachelor111_footerheader():
    horizontals, pageheight, top, bottom, pagetextnavigators = _bachelor111()

    footerheader = []
    for top, bottom in itertools.zip_longest(top, bottom):
        extracted = gfsf.extract_page_footerheader(
            horizontals,
            top,
            bottom,
            pageheight,
            pagetextnavigators,
        )
        footerheader.extend(extracted)
    footerheader = gfs.remove_duplication(footerheader)
    return footerheader


@utilatest.skip_longrun
def test_groupme_footer_fixed_bachelor111page_extract_common_footer():
    _, __, top, bottom, ___ = _bachelor111()
    assert top  # document has header
    assert bottom  # document has footer
    assert top < bottom


@utilatest.skip_longrun
def test_groupme_footer_fixed_bachelor111page_extract_page_footerheader():
    """Use more than one group to detect all headers. There are ordered
    from biggest to smallest"""

    footerheader = _bachelor111_footerheader()
    msg = 'more footer than pages, remove duplication'
    assert len(footerheader) < tests.resources.BACHELOR111_PAGE_COUNT, msg

    header = [item.header for item in footerheader if item.header]
    assert len(header) == 94, utila.log_raw(header)

    # assert that strategy detect no invalid fixed footer
    footer = [item.footer for item in footerheader if item.footer]
    assert not footer, utila.log_raw(footer)


@utilatest.skip_longrun
def test_groupme_footer_fixed_bachelor111page_extract_page_header():
    footerheader = _bachelor111_footerheader()
    pages = [item.page for item in footerheader]
    assert all(pages)

    title = [
        item.header.title
        for item in footerheader
        if item.header and item.header.title
    ]
    assert len(title) >= 68, 'not enough title'


def test_groupme_footer_dump_and_load_bachelor111():
    footerheader = _bachelor111_footerheader()

    dumped = serializeraw.dump_headerfooter(footerheader)
    loaded = serializeraw.load_headerfooter(dumped)

    assert loaded == footerheader
