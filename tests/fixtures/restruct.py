# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import iamraw.path
import power
import pytest
import serializeraw

import groupme.path

RESTRUCT_BOXES = iamraw.path.boxed(power.link(power.DOCU27_PDF))
RESTRUCT_FONT_CONTENT = iamraw.path.fontcontent(power.link(power.DOCU27_PDF))
RESTRUCT_FONT_HEADER = iamraw.path.fontheader(power.link(power.DOCU27_PDF))
RESTRUCT_FOOTERS = iamraw.path.headerfooters(power.link(power.DOCU27_PDF))
RESTRUCT_HORIZONTAL = iamraw.path.horizontals(power.link(power.DOCU27_PDF))
RESTRUCT_ONELINE_FONT_CONTENT = iamraw.path.fontcontent(
    power.link(power.DOCU27_PDF),
    prefix='oneline',
)
RESTRUCT_ONELINE_FONT_HEADER = iamraw.path.fontheader(
    power.link(power.DOCU27_PDF),
    prefix='oneline',
)
RESTRUCT_ONELINE_TEXT = iamraw.path.text(
    power.link(power.DOCU27_PDF),
    prefix='oneline',
)
RESTRUCT_PAGESIZE = iamraw.path.sizeandborder(power.link(power.DOCU27_PDF))
RESTRUCT_TEXT = iamraw.path.text(power.link(power.DOCU27_PDF))
RESTRUCT_TEXT_POSITION = iamraw.path.textposition(power.link(power.DOCU27_PDF))
RESTRUCT_TOC = iamraw.path.toc(power.link(power.DOCU27_PDF))
RESTRUCT_PAGENUMBERS = groupme.path.pagenumbers(power.link(power.DOCU27_PDF))


@pytest.fixture
def restructured_text() -> iamraw.Document:
    loaded = serializeraw.load_document(RESTRUCT_TEXT)
    return loaded


@pytest.fixture
def restructured_fontstore() -> iamraw.FontStore:
    lookup = serializeraw.create_fontstore(
        RESTRUCT_FONT_HEADER,
        RESTRUCT_FONT_CONTENT,
    )
    return lookup


def restructured_fontstore_fixture() -> iamraw.FontStore:
    # TODO: Remove with new pytest - this is required, because pytest carn't
    # use pytest.fixture in paramertized tests.
    lookup = serializeraw.create_fontstore(
        RESTRUCT_FONT_HEADER,
        RESTRUCT_FONT_CONTENT,
    )
    return lookup


@pytest.fixture
def restructured_pagenumbers():
    loaded = serializeraw.load_pagenumbers(RESTRUCT_PAGENUMBERS)
    return loaded


@pytest.fixture
def restructured_horizontals():
    loaded = serializeraw.load_horizontals(RESTRUCT_HORIZONTAL)
    return loaded


@pytest.fixture
def restructured_pagetextnavigators():
    navigators = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.DOCU27_PDF))
    return navigators


@pytest.fixture
def restructured_sizeandborder():
    loaded = serializeraw.load_pageborders(RESTRUCT_PAGESIZE)
    return loaded
