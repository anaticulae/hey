# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import serializeraw

import tests.resources
from hey.textnavigator.navigator import create_pagetextnavigators
# pylint:disable=W0611
from tests.fixtures.restruct import restructured
from tests.fixtures.restruct import restructured_fontstore
from tests.fixtures.restruct import restructured_horizontals
from tests.fixtures.restruct import restructured_sections
from tests.fixtures.restruct import restructured_sections_manual
from tests.fixtures.restruct import restructured_sizeandborder
from tests.fixtures.restruct import restructured_text
from tests.fixtures.restruct import restructured_text_positions
from tests.resources import RESTRUCT_FONT_CONTENT
from tests.resources import RESTRUCT_FONT_HEADER
from tests.resources import RESTRUCT_HORIZONTAL
from tests.resources import RESTRUCT_PAGESIZE
from tests.resources import RESTRUCT_TEXT
from tests.resources import RESTRUCT_TEXT_POSITION
from tests.resources import RESTRUCT_TOC
from words.feature.headlines import extract_headlines
from words.feature.headlines import work

EXPECTED = [
    [
        iamraw.Headline(
            text='CHAPTER 1',
            level=1,
            rawlevel='1',
            container=0,
            page=6,
        ),
        iamraw.Headline(
            text='RestructuredText Tutorial',
            level=2,
            rawlevel='',
            container=1,
            page=6,
        ),
    ],
    [
        iamraw.Headline(
            text='CHAPTER 2',
            level=1,
            rawlevel='2',
            container=0,
            page=8,
        ),
        iamraw.Headline(
            text='RestructuredText Guide',
            level=2,
            rawlevel='',
            container=1,
            page=8,
        ),
        iamraw.Headline(
            text='Basics',
            level=3,
            rawlevel='',
            container=2,
            page=8,
        ),
        iamraw.Headline(
            text='Blockquotes',
            level=3,
            rawlevel='',
            container=1,
            page=9,
        ),
        iamraw.Headline(
            text='Code: Block',
            level=3,
            rawlevel='',
            container=10,
            page=9,
        ),
    ],
]


def test_headlines_extract_headlines(
        # pylint:disable=W0621
        restructured_sections_manual,
        restructured_text_positions,
        restructured_text,
        restructured_fontstore,
        restructured_sizeandborder,
        restructured_horizontals,
):
    sections = restructured_sections_manual
    position = restructured_text_positions
    document = restructured_text
    sizeandborder = restructured_sizeandborder

    navigator = create_pagetextnavigators(
        text=document,
        text_positions=position,
    )

    extracted = extract_headlines(
        sections=sections,
        pagetextnavigators=navigator,
        fontstore=restructured_fontstore,
        sizeandborder=sizeandborder,
        horizontals=restructured_horizontals,
        chapter=[0, 1],
    )
    assert len(extracted) == len(EXPECTED)
    assert [len(item) for item in extracted] == [len(item) for item in EXPECTED]
    assert extracted == EXPECTED


def test_headlines_work():
    sections_ = restructured_sections()
    dumped = work(
        sections=sections_,
        text=RESTRUCT_TEXT,
        text_position=RESTRUCT_TEXT_POSITION,
        font_header=RESTRUCT_FONT_HEADER,
        font_content=RESTRUCT_FONT_CONTENT,
        sizeandborder=RESTRUCT_PAGESIZE,
        horizontals=RESTRUCT_HORIZONTAL,
    )
    # dump some headlines
    assert len(dumped) > 2100, str(dumped)


def test_headlines_dump_and_load_headlines():
    """Dump and load the example above"""
    dumped = serializeraw.dump_headlines(EXPECTED)
    loaded = serializeraw.load_headlines(dumped)

    assert loaded == EXPECTED


def test_headlines_master72_pages():
    master72 = tests.resources.MASTER_72PAGES
    sections = tests.resources.sections(master72)
    text = tests.resources.text(master72)
    text_positions = tests.resources.text_positions(master72)
    font_header = tests.resources.font_header(master72)
    font_content = tests.resources.font_content(master72)
    sizeandborder = tests.resources.sizeandborder(master72)
    horizontals = tests.resources.horizontals(master72)

    headlines = work(
        sections,
        text,
        text_positions,
        font_header,
        font_content,
        sizeandborder,
        horizontals,
    )
    assert len(headlines) > 400, str(headlines)

    headlines_loaded = serializeraw.load_headlines(headlines)

    with pytest.raises(AssertionError):  # TODO: REMOVE AFTER SOLVED
        assert len(headlines_loaded) == 5, str(headlines_loaded)
