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
import tests.resources


@pytest.fixture
def horizontals():
    result = serializeraw.load_horizontals(tests.resources.RESTRUCT_HORIZONTAL)
    return result


def test_groupme_footer_extract(horizontals):  #pylint:disable=W0621
    top, bottom = groupme.footer.fixed.extract_common_footer(horizontals)
    assert top  # document has header
    assert bottom  # document has footer
    assert top < bottom


def test_groupme_footer_work(testdir):  #pylint:disable=W0621
    root = str(testdir)
    dumped = groupme.feature.footer.work(tests.resources.RESTRUCT_HORIZONTAL)
    assert dumped
    assert len(dumped) > 100, str(dumped)  # there is some content

    utila.file_create(os.path.join(root, 'result.yaml'), dumped)


def test_groupme_footer_master72pages(testdir):
    path = tests.resources.horizontals(tests.resources.MASTER_72PAGES)
    result = serializeraw.load_horizontals(path)

    assert len(result) > 10, str(result)


def test_groupme_footer_dump_and_load(horizontals):  #pylint:disable=W0621
    # TODO: use general strategy?
    extracted = groupme.footer.fixed.FixedFooterStrategy(horizontals).result()

    dumped = groupme.footer.dump_headerfooter(extracted)
    loaded = groupme.footer.load_headerfooter(dumped)

    assert loaded == extracted


def test_groupme_footer_footerheader_detectionstategy(horizontals):  #pylint:disable=W0621
    strategy = groupme.footer.FooterHeaderDetectionStrategy(
        horizontals=horizontals,)
    strategy.process()
