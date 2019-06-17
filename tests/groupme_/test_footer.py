# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import fixture
from serializeraw import load_horizontals

from groupme.feature.footer import dump_headerfooter
from groupme.feature.footer import extract_common_footer
from groupme.feature.footer import extract_pages
from groupme.feature.footer import load_headerfooter
from groupme.feature.footer import work
from tests.resources import RESTRUCT_HORIZONTAL as HORIZONTALS


@fixture
def horizontals():
    result = load_horizontals(HORIZONTALS)
    return result


def test_footer_extract(horizontals):  #pylint:disable=W0621
    top, bottom = extract_common_footer(horizontals)
    assert top  # document has header
    assert bottom  # document has footer
    assert top > bottom


def test_footer_work():  #pylint:disable=W0621
    dumped = work(HORIZONTALS)
    assert dumped
    assert len(dumped) > 100, str(dumped)  # there is some content


def test_footer_dump_and_load(horizontals):  #pylint:disable=W0621
    extracted = extract_pages(horizontals)

    dumped = dump_headerfooter(extracted)
    loaded = load_headerfooter(dumped)

    assert loaded == extracted
