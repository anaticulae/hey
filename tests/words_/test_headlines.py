# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from pytest import fixture

from hey.textnavigator.navigator import create_pagetextnavigators
from sections.feature.chapter import work as chapter_work
from sections.feature.index import work as index_work
from sections.feature.sections import work as section_work
from sections.feature.title import work as title_work
from sections.feature.toc import work as toc_work
from sections.feature.whitepage import work as whitepage_work
# pylint:disable=W0611
from tests.fixtures.restruct import restructured
from tests.fixtures.restruct import restructured_fontstore
from tests.fixtures.restruct import restructured_horizontals
from tests.fixtures.restruct import restructured_sections
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
from words.feature.headlines import Headline
from words.feature.headlines import dump_headlines
from words.feature.headlines import extract_headlines
from words.feature.headlines import load_headlines
from words.feature.headlines import work

EXPECTED = [
    [
        Headline(
            text='CHAPTER 1',
            level=1,
            rawlevel='1',
            container=0,
            page=6,
        ),
        Headline(
            text='RestructuredText Tutorial',
            level=2,
            rawlevel='',
            container=1,
            page=6,
        ),
    ],
    [
        Headline(
            text='CHAPTER 2',
            level=1,
            rawlevel='2',
            container=0,
            page=8,
        ),
        Headline(
            text='RestructuredText Guide',
            level=2,
            rawlevel='',
            container=1,
            page=8,
        ),
        Headline(
            text='Basics',
            level=3,
            rawlevel='',
            container=2,
            page=8,
        ),
        Headline(
            text='Blockquotes',
            level=3,
            rawlevel='',
            container=1,
            page=9,
        ),
        Headline(
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
        restructured_sections,
        restructured_text_positions,
        restructured_text,
        restructured_fontstore,
        restructured_sizeandborder,
        restructured_horizontals,
):
    sections = restructured_sections
    position = restructured_text_positions
    document = restructured_text
    sizeandborder = restructured_sizeandborder

    navigator = create_pagetextnavigators(
        text=document,
        text_position=position,
    )

    extracted = extract_headlines(
        sections=sections,
        pagetextnavigator=navigator,
        fontstore=restructured_fontstore,
        sizeandborder=sizeandborder,
        horizontals=restructured_horizontals,
        chapter=[0, 1],
    )
    assert len(extracted) == len(EXPECTED)
    assert [len(item) for item in extracted] == [len(item) for item in EXPECTED]
    assert extracted == EXPECTED


def sections():
    chapter = chapter_work(RESTRUCT_TEXT, RESTRUCT_TEXT_POSITION, RESTRUCT_TOC)

    index = index_work(RESTRUCT_TEXT)
    title = title_work(
        RESTRUCT_TEXT,
        RESTRUCT_FONT_HEADER,
        RESTRUCT_FONT_CONTENT,
    )
    toc = toc_work(RESTRUCT_TEXT)
    whitepage = whitepage_work(
        RESTRUCT_TEXT,
        RESTRUCT_TEXT_POSITION,
        RESTRUCT_HORIZONTAL,
    )
    result = section_work(chapter, index, title, toc, whitepage)
    return result


def test_headlines_work():
    sections_ = sections()
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


@fixture
def restructured_headlines():
    sections_ = sections()
    dumped = work(
        sections=sections_,
        text=RESTRUCT_TEXT,
        text_position=RESTRUCT_TEXT_POSITION,
        font_header=RESTRUCT_FONT_HEADER,
        font_content=RESTRUCT_FONT_CONTENT,
        sizeandborder=RESTRUCT_PAGESIZE,
        horizontals=RESTRUCT_HORIZONTAL,
    )
    return dumped


def test_headlines_dump_and_load_headlines():
    """Dump and load the example above"""
    dumped = dump_headlines(EXPECTED)
    loaded = load_headlines(dumped)

    assert loaded == EXPECTED
