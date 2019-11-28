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
import groupme.path
import hey.path
import hey.textnavigator.navigator as htn
import tests.fixtures.restruct
import tests.resources
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_horizontals
from tests.fixtures.restruct import restructured_pagenumbers
from tests.fixtures.restruct import restructured_pagetextnavigators
from tests.fixtures.restruct import restructured_sizeandborder


def test_groupme_footer_work(testdir):  #pylint:disable=W0621
    root = str(testdir)
    dumped = groupme.feature.footer.work(
        tests.resources.text(tests.resources.RESTRUCT),
        tests.resources.text_positions(tests.resources.RESTRUCT),
        tests.resources.horizontals(tests.resources.RESTRUCT),
        tests.resources.sizeandborder(tests.resources.RESTRUCT),
        tests.resources.pagenumbers(tests.resources.RESTRUCT),
    )
    assert dumped
    assert len(dumped) > 100, str(dumped)  # there is some content

    utila.file_create(os.path.join(root, 'result.yaml'), dumped)


def test_groupme_footer_dump_and_load(
        restructured_horizontals,  #pylint:disable=W0621
        restructured_sizeandborder,  #pylint:disable=W0621
        restructured_pagenumbers,  #pylint:disable=W0621
        restructured_pagetextnavigators,  #pylint:disable=W0621
):
    horizontals = restructured_horizontals
    pagenumbers = restructured_pagenumbers
    sizeandborders = restructured_sizeandborder
    pagetextnavigators = restructured_pagetextnavigators
    # TODO: use general strategy?
    extracted = groupme.footer.fixed.FixedFooterStrategy(
        horizontals,
        sizeandborders,
        pagenumbers,
        pagetextnavigators,
    )
    extracted = extracted.result()

    dumped = serializeraw.dump_headerfooter(extracted)
    loaded = serializeraw.load_headerfooter(dumped)

    assert loaded == extracted


@pytest.mark.parametrize(
    'strategy, expected_results',
    [
        (groupme.footer.moving.MovingFooterStrategy, 0),
        (groupme.footer.fixed.FixedFooterStrategy, 26),  # TODO: CHECK 26
        (groupme.footer.pages.PageNumberStrategy, 0),
    ])
def test_groupme_footer_footerheader_detectionstategy(
        strategy,
        expected_results,
        restructured_horizontals,  #pylint:disable=W0621
        restructured_sizeandborder,  #pylint:disable=W0621
        restructured_pagenumbers,  #pylint:disable=W0621
        restructured_pagetextnavigators,  # pylint:disable=W0621
):
    """Check that different strategies work proper with given resources

    TODO: SEE DUPLICATION test_footer_judgement_strategy_quality"""
    horizontals = restructured_horizontals
    sizeandborders = restructured_sizeandborder
    pagenumbers = restructured_pagenumbers
    pagetextnavigators = restructured_pagetextnavigators

    process = strategy(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        pagenumbers=pagenumbers,
        pagetextnavigators=pagetextnavigators,
    )
    result = process.result()
    assert len(result) == expected_results, 'not enough footer and header'


@pytest.mark.parametrize('root, expected', [
    pytest.param(
        tests.resources.TECHNICAL_24PAGES,
        list(range(1, 24)),
        id='technical24',
    ),
    pytest.param(
        tests.resources.MASTER_72PAGES,
        [],
        id='master72',
    ),
])
def test_groupme_footer_extract_footerheader_technical(root, expected):
    pages = None
    pagetextnavigators = htn.create_pagetextnavigators_frompath(
        root,
        pages=pages,
    )

    horizontals = serializeraw.load_horizontals(
        hey.path.horizontals(root),
        pages=pages,
    )

    sizeandborders = serializeraw.load_pageborders(
        hey.path.sizeandborder(root),
        pages=pages,
    )

    pagenumbers = serializeraw.load_pagenumbers(
        groupme.path.pagenumbers(root),
        pages=pages,
    )

    result = groupme.feature.footer.extract_footerheader(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        pagenumbers=pagenumbers,
        pagetextnavigators=pagetextnavigators,
    )

    header = [item.page for item in result if item.header is not None]
    assert header == expected
