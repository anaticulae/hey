# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Test to group chapter out of text and and headlines.
"""

import serializeraw
from iamraw import Document
from iamraw import Page
from pytest import mark
from utila import file_read

from groupme.feature.chapter import chapters
from groupme.structure import parse_headline
from groupme.structure import sections
from groupme.structure import sections_from_page
# pylint: disable=unused-import
from tests.fixtures.simple import simple_document
from tests.fixtures.simple import simple_page_2
from tests.fixtures.simple import simple_page_2_text_only
from tests.resources import SIMPLE_HEADLINES_PAGE_3
from tests.resources import SIMPLE_TEXT
from tests.resources import SIMPLE_TOC_LINES


def test_dump_and_load_chapter():
    """Ensure that every section have an textbody"""
    doc = serializeraw.load_document(file_read(SIMPLE_TEXT))
    content = chapters(doc)
    assert len(content) == SIMPLE_TOC_LINES

    dumped = serializeraw.dump_chapter(content)
    assert dumped

    loaded = serializeraw.load_chapter(dumped)
    assert loaded == content


def test_extract_page_2(simple_page_2: Page):  # pylint: disable=W0621
    blocks = sections_from_page(simple_page_2)
    assert len(blocks) == SIMPLE_HEADLINES_PAGE_3


def test_extract_document(simple_document: Document):  # pylint: disable=W0621
    result = sections(simple_document)
    assert result


@mark.parametrize('headline', [
    '1. Erstes Kapitel',
    '12.2 Zwoelftes Kapitel',
    '1.1.1. Erstes Kapitel',
    '5.1.1.1. Erstes Kapitel',
    '5.a. Kapitel Text Ende',
    'I Inhaltsverzeichnis',
])
def test_headline_match(headline):
    parsed = parse_headline(headline)
    assert parsed is not None, str(headline)
    assert len(parsed) == 2, parsed


def test_parse_headlines(simple_page_2_text_only):  # pylint: disable=W0621
    headlines = []
    for line in simple_page_2_text_only:
        result = parse_headline(line)
        if not result:
            continue
        headlines.append(result[1])
    assert len(headlines) == SIMPLE_HEADLINES_PAGE_3, headlines


# TODO: add timeout to this unit test
# TODO: add timeout to parse_headline
def test_parse_headline_problematic():
    """The old regex had a problem to parse the example below. Before this fix
    the time of parsing this string was enormous."""
    problem = '1.0011001100110011001100110011001100110011001100110011'
    parsed = parse_headline(problem)
    assert parsed is None, str(parsed)
