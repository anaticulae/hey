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

import iamraw
import pytest
import serializeraw
import utila

import groupme.feature.chapter
import groupme.structure
import tests.resources
# pylint: disable=unused-import
from tests.fixtures.simple import simple_document
from tests.fixtures.simple import simple_page_2
from tests.fixtures.simple import simple_page_2_text_only


def test_groupme_chapter_dump_and_load_chapter():
    """Ensure that every section have an textbody"""
    doc = utila.file_read(tests.resources.SIMPLE_TEXT)
    doc = serializeraw.load_document(doc)

    content = groupme.feature.chapter.chapters(doc)
    assert len(content) == tests.resources.SIMPLE_TOC_LINES

    dumped = serializeraw.dump_chapter(content)
    assert dumped

    loaded = serializeraw.load_chapter(dumped)
    assert loaded == content


def test_groupme_chapter_extract_page2(simple_page_2: iamraw.Page):  # pylint: disable=W0621
    blocks = groupme.structure.sections_from_page(simple_page_2)
    assert len(blocks) == tests.resources.SIMPLE_HEADLINES_PAGE_3


def test_groupme_chapter_extract_document(simple_document: iamraw.Document):  # pylint: disable=W0621
    result = groupme.structure.sections(simple_document)
    assert result


@pytest.mark.parametrize('headline', [
    '1. Erstes Kapitel',
    '12.2 Zwoelftes Kapitel',
    '1.1.1. Erstes Kapitel',
    '5.1.1.1. Erstes Kapitel',
    '5.a. Kapitel Text Ende',
    'I Inhaltsverzeichnis',
])
def test_groupme_chapter_headline_match(headline):
    parsed = groupme.structure.parse_headline(headline)
    assert parsed is not None, str(headline)
    assert len(parsed) == 2, parsed


def test_groupme_chapter_test_parse_headlines(simple_page_2_text_only):  # pylint: disable=W0621
    headlines = []
    for line in simple_page_2_text_only:
        result = groupme.structure.parse_headline(line)
        if not result:
            continue
        headlines.append(result[1])
    assert len(headlines) == tests.resources.SIMPLE_HEADLINES_PAGE_3, headlines


@pytest.mark.timeout(20, "slow", method="thread")
def test_groupme_chapter_parse_headline_problematic():
    """The old regex had a problem to parse the example below. Before this fix
    the time of parsing this string was enormous."""
    problem = '1.0011001100110011001100110011001100110011001100110011'
    # TODO: add timeout to parse_headline
    parsed = groupme.structure.parse_headline(problem)
    assert parsed is None, str(parsed)
