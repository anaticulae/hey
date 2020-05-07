# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import serializeraw
import texmex

import tests
import tests.fixtures
import tests.resources

SIMPLE_PAGESIZE = iamraw.path.sizeandborder(tests.resources.HOWTO_PYPORTING)
SIMPLE_HORIZONTAL = iamraw.path.horizontals(tests.resources.HOWTO_PYPORTING)
SIMPLE_TEXT_POSITION = iamraw.path.textposition(tests.resources.HOWTO_PYPORTING)
SIMPLE_TEXT = iamraw.path.text(tests.resources.HOWTO_PYPORTING)
SIMPLE_ONELINE_TEXT = iamraw.path.text(
    tests.resources.HOWTO_PYPORTING,
    prefix='oneline',
)
SIMPLE_ONELINE_FONT_HEADER = iamraw.path.fontheader(
    tests.resources.HOWTO_PYPORTING,
    prefix='oneline',
)
SIMPLE_ONELINE_FONT_CONTENT = iamraw.path.fontcontent(
    tests.resources.HOWTO_PYPORTING,
    prefix='oneline',
)
SIMPLE_FONT_HEADER = iamraw.path.fontheader(tests.resources.HOWTO_PYPORTING)
SIMPLE_FONT_CONTENT = iamraw.path.fontcontent(tests.resources.HOWTO_PYPORTING)
SIMPLE_FOOTER = iamraw.path.headerfooters(tests.resources.HOWTO_PYPORTING)
SIMPLE_TOC = iamraw.path.toc(tests.resources.HOWTO_PYPORTING)
SIMPLE_FOOTERS = iamraw.path.headerfooters(tests.resources.HOWTO_PYPORTING)


@pytest.fixture
def simple():
    pagesize = serializeraw.load_pageborders(SIMPLE_PAGESIZE)
    horizontals = serializeraw.load_horizontals(SIMPLE_HORIZONTAL) # yapf:disable
    position = serializeraw.load_textpositions(SIMPLE_TEXT_POSITION) # yapf:disable
    document = serializeraw.load_document(SIMPLE_TEXT)

    assert pagesize
    assert horizontals
    assert position

    navigator = texmex.create_pagetextnavigators(
        text=document,
        text_positions=position,
    )
    return navigator, horizontals


@pytest.fixture
def simple_navigator(simple):  #pylint:disable=W0621
    navigator, _ = simple
    return navigator
