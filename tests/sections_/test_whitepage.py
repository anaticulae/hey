# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import tests.fixtures
import tests.resources
from sections.feature.whitepage import PageContentWhitepages
from sections.feature.whitepage import WhitePage
from sections.feature.whitepage import extract_whitepages
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_pagetextnavigators

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


def test_whitepages_extract(restructured_pagetextnavigators):  # pylint:disable=W0621
    navigators = restructured_pagetextnavigators

    document = serializeraw.load_document(tests.resources.RESTRUCT_TEXT)

    headerfooters = tests.resources.headerfooters(tests.resources.RESTRUCT)
    headerfooters = serializeraw.load_headerfooter(headerfooters)

    # work
    result = extract_whitepages(document, navigators, headerfooters)

    # convert dict to list
    assert result == RESTRUCT_EXPECTED
