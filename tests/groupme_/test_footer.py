# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import serializeraw
import utila

import groupme.feature.footer
import groupme.footer
import groupme.footer.moving
import hey.utils
import tests.fixtures.restruct
import tests.resources
from tests.fixtures.restruct import restructured_horizontals
from tests.fixtures.restruct import restructured_pagenumbers
from tests.fixtures.restruct import restructured_sizeandborder


def test_groupme_footer_extract(restructured_horizontals):  #pylint:disable=W0621
    horizontals = restructured_horizontals
    top, bottom = groupme.footer.fixed.extract_common_footer(horizontals)
    assert top  # document has header
    assert bottom  # document has footer
    assert top < bottom


def test_groupme_footer_work(testdir):  #pylint:disable=W0621
    root = str(testdir)
    dumped = groupme.feature.footer.work(
        tests.resources.RESTRUCT_HORIZONTAL,
        tests.resources.RESTRUCT_PAGESIZE,
        tests.resources.RESTRUCT_PAGENUMBERS,
    )
    assert dumped
    assert len(dumped) > 100, str(dumped)  # there is some content

    utila.file_create(os.path.join(root, 'result.yaml'), dumped)


def test_groupme_footer_master72pages(testdir):
    path = tests.resources.horizontals(tests.resources.MASTER_72PAGES)
    result = serializeraw.load_horizontals(path)

    assert len(result) > 10, str(result)


def test_groupme_footer_dump_and_load(
        restructured_horizontals,  #pylint:disable=W0621
        restructured_sizeandborder,  #pylint:disable=W0621
        restructured_pagenumbers,  #pylint:disable=W0621
):
    horizontals = restructured_horizontals
    pagenumbers = restructured_pagenumbers
    sizeandborders = restructured_sizeandborder
    # TODO: use general strategy?
    extracted = groupme.footer.fixed.FixedFooterStrategy(
        horizontals,
        sizeandborders,
        pagenumbers,
    ).result()

    dumped = groupme.footer.dump_headerfooter(extracted)
    loaded = groupme.footer.load_headerfooter(dumped)

    assert loaded == extracted


def test_groupme_footer_footerheader_detectionstategy(
        restructured_horizontals,  #pylint:disable=W0621
        restructured_sizeandborder,  #pylint:disable=W0621
        restructured_pagenumbers,  #pylint:disable=W0621
):
    horizontals = restructured_horizontals
    sizeandborders = restructured_sizeandborder
    pagenumbers = restructured_pagenumbers
    strategy = groupme.footer.FooterHeaderDetectionStrategy(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        pagenumbers=pagenumbers,
    )
    strategy.process()


@pytest.mark.parametrize('document, pages', [
    (tests.resources.MASTER_72PAGES, tuple(range(20))),
])
def test_groupme_footer_moving(document, pages):
    horizontallines = serializeraw.load_horizontals(
        tests.resources.horizontals(document),
        pages,
    )
    sizeandborder = serializeraw.load_pageborders(
        tests.resources.sizeandborder(document),
        pages,
    )

    pagenumbers = serializeraw.load_pagenumbers(
        tests.resources.pagenumbers(document),
        pages,
    )

    strategy = groupme.footer.moving.MovingFooterStrategy(
        horizontallines,
        sizeandborder,
        pagenumbers,
    )
    result = strategy.result()

    expected = [3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert len(result) == len(expected), result

    for footer in expected:
        extracted_footer = hey.utils.select_page(result, footer)
        assert extracted_footer[1], f'{footer}'
