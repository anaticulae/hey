# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from serializeraw import load_document
from serializeraw import load_horizontals

from groupme.feature.footer import extract_pages
from groupme.feature.numbers import load_textposition
from groupme.textnavigator import create_pagetextnavigator
from sections.feature.whitepage import WhitePage
from sections.feature.whitepage import dump_whitepages
from sections.feature.whitepage import extract_whitepages
from sections.feature.whitepage import load_whitepages
from tests.groupme_ import FOOTER_HORIZONTAL
from tests.groupme_ import FOOTER_POSITION
from tests.groupme_ import FOOTER_TEXT

FOOTER_EXPECTED = [
    None,
    WhitePage.BLANK,
    None,
    WhitePage.WHITE,
    None,
    WhitePage.WHITE,
    None,
    WhitePage.WHITE,
    None,
    None,
    None,
    WhitePage.WHITE,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    WhitePage.WHITE,
    None,
    WhitePage.WHITE,
    None,
    WhitePage.WHITE,
    None,
    WhitePage.WHITE,
    None,
]


def test_whitepages_extract():

    # load
    document = load_document(FOOTER_TEXT)
    position = load_textposition(FOOTER_POSITION)
    horizontals = load_horizontals(FOOTER_HORIZONTAL)

    # TODO: Think about how to handle this, invocation order of features?
    headerfooters = extract_pages(horizontals)
    navigators = create_pagetextnavigator(position, document)

    # work
    result = extract_whitepages(document, navigators, headerfooters)

    assert result == FOOTER_EXPECTED


def test_whitepages_dump_and_load():
    dumped = dump_whitepages(FOOTER_EXPECTED)

    loaded = load_whitepages(dumped)

    assert loaded == FOOTER_EXPECTED
