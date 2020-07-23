# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import texmex

SIMPLE_PAGESIZE = iamraw.path.sizeandborder(power.link(power.DOCU07_PDF))
SIMPLE_HORIZONTAL = iamraw.path.horizontals(power.link(power.DOCU07_PDF))
SIMPLE_TEXT_POSITION = iamraw.path.textposition(power.link(power.DOCU07_PDF))
SIMPLE_TEXT = iamraw.path.text(power.link(power.DOCU07_PDF))
SIMPLE_ONELINE_TEXT = iamraw.path.text(
    power.link(power.DOCU07_PDF),
    prefix='oneline',
)
SIMPLE_ONELINE_FONT_HEADER = iamraw.path.fontheader(
    power.link(power.DOCU07_PDF),
    prefix='oneline',
)
SIMPLE_ONELINE_FONT_CONTENT = iamraw.path.fontcontent(
    power.link(power.DOCU07_PDF),
    prefix='oneline',
)
SIMPLE_FONT_HEADER = iamraw.path.fontheader(power.link(power.DOCU07_PDF))
SIMPLE_FONT_CONTENT = iamraw.path.fontcontent(power.link(power.DOCU07_PDF))
SIMPLE_FOOTER = iamraw.path.headerfooters(power.link(power.DOCU07_PDF))
SIMPLE_TOC = iamraw.path.toc(power.link(power.DOCU07_PDF))
SIMPLE_FOOTERS = iamraw.path.headerfooters(power.link(power.DOCU07_PDF))


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
