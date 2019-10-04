# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import groupme.footer.fixed
from hey.textnavigator.navigator import create_pagetextnavigators
from sections.feature.whitepage import PageContentWhitepages
from sections.feature.whitepage import WhitePage
from sections.feature.whitepage import dump_whitepages
from sections.feature.whitepage import extract_whitepages
from sections.feature.whitepage import load_whitepages
from tests.resources import RESTRUCT_HORIZONTAL
from tests.resources import RESTRUCT_PAGENUMBERS
from tests.resources import RESTRUCT_PAGESIZE
from tests.resources import RESTRUCT_TEXT
from tests.resources import RESTRUCT_TEXT_POSITION

RESTRUCT_EXPECTED = [
    PageContentWhitepages(content=WhitePage.CONTENT, page=0),
    PageContentWhitepages(content=WhitePage.BLANK, page=1),
    PageContentWhitepages(content=WhitePage.CONTENT, page=2),
    PageContentWhitepages(content=WhitePage.WHITE, page=3),
    PageContentWhitepages(content=WhitePage.CONTENT, page=4),
    PageContentWhitepages(content=WhitePage.WHITE, page=5),
    PageContentWhitepages(content=WhitePage.CONTENT, page=6),
    PageContentWhitepages(content=WhitePage.WHITE, page=7),
    PageContentWhitepages(content=WhitePage.CONTENT, page=8),
    PageContentWhitepages(content=WhitePage.CONTENT, page=9),
    PageContentWhitepages(content=WhitePage.CONTENT, page=10),
    PageContentWhitepages(content=WhitePage.WHITE, page=11),
    PageContentWhitepages(content=WhitePage.CONTENT, page=12),
    PageContentWhitepages(content=WhitePage.CONTENT, page=13),
    PageContentWhitepages(content=WhitePage.CONTENT, page=14),
    PageContentWhitepages(content=WhitePage.CONTENT, page=15),
    PageContentWhitepages(content=WhitePage.CONTENT, page=16),
    PageContentWhitepages(content=WhitePage.CONTENT, page=17),
    PageContentWhitepages(content=WhitePage.CONTENT, page=18),
    PageContentWhitepages(content=WhitePage.WHITE, page=19),
    PageContentWhitepages(content=WhitePage.CONTENT, page=20),
    PageContentWhitepages(content=WhitePage.WHITE, page=21),
    PageContentWhitepages(content=WhitePage.CONTENT, page=22),
    PageContentWhitepages(content=WhitePage.WHITE, page=23),
    PageContentWhitepages(content=WhitePage.CONTENT, page=24),
    PageContentWhitepages(content=WhitePage.WHITE, page=25),
    PageContentWhitepages(content=WhitePage.CONTENT, page=26),
]


def test_whitepages_extract():
    # load
    document = serializeraw.load_document(RESTRUCT_TEXT)
    position = serializeraw.load_textpositions(RESTRUCT_TEXT_POSITION)
    horizontals = serializeraw.load_horizontals(RESTRUCT_HORIZONTAL)
    sizeandborders = serializeraw.load_pageborders(RESTRUCT_PAGESIZE)
    pagenumbers = serializeraw.load_pagenumbers(RESTRUCT_PAGENUMBERS)

    # TODO: access headers and footers directly
    headerfooters = groupme.footer.fixed.FixedFooterStrategy(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        pagenumbers=pagenumbers,
    )
    headerfooters = headerfooters.result()
    navigators = create_pagetextnavigators(
        text=document,
        text_positions=position,
    )

    # work
    result = extract_whitepages(document, navigators, headerfooters)

    # convert dict to list
    assert result == RESTRUCT_EXPECTED


def test_whitepages_dump_and_load():
    dumped = dump_whitepages(RESTRUCT_EXPECTED)
    assert len(dumped) > 100, str(dumped)
    loaded = load_whitepages(dumped)
    assert loaded == RESTRUCT_EXPECTED
