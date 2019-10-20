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


@pytest.mark.parametrize('strategy', [
    groupme.footer.moving.MovingFooterStrategy,
    groupme.footer.fixed.FixedFooterStrategy,
    groupme.footer.pages.PageNumberStrategy,
])
def test_groupme_footer_footerheader_detectionstategy(
        strategy,
        restructured_horizontals,  #pylint:disable=W0621
        restructured_sizeandborder,  #pylint:disable=W0621
        restructured_pagenumbers,  #pylint:disable=W0621
        restructured_pagetextnavigators,  # pylint:disable=W0621
):
    """Check that different strategies work proper with given resources"""
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
    assert len(result) >= 1, 'not enough footer and header'
