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

from iamraw import Document
from iamraw import Page
from pytest import mark
from serializeraw import load_document
from utila import file_read

from groupme.feature.chapter import chapter_to_yaml
from groupme.feature.chapter import chapters
from groupme.structure import parse_headline
from groupme.structure import sections
from groupme.structure import sections_from_page
from tests.groupme_ import HEADLINES_PAGE_3
from tests.groupme_ import SIMPLE_TEXT
from tests.groupme_ import TOC_LINES
from tests.groupme_ import document  # pylint: disable=unused-import
from tests.groupme_ import page_2  # pylint: disable=unused-import
from tests.groupme_ import page_2_text_only  # pylint: disable=unused-import


def test_content_to_yaml():
    """Ensure that every section have an textbody"""
    doc = load_document(file_read(SIMPLE_TEXT))
    content = chapters(doc)
    assert len(content) == TOC_LINES
    dumped = chapter_to_yaml(content)
    assert dumped


def test_extract_page_2(page_2: Page):  # pylint: disable=W0621
    blocks = sections_from_page(page_2)
    assert len(blocks) == HEADLINES_PAGE_3


def test_extract_document(document: Document):  # pylint: disable=W0621
    result = sections(document)
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


def test_parse_headlines(page_2_text_only):  # pylint: disable=W0621
    # print(len(page_3_text_only))
    # assert 0
    headlines = []
    for line in page_2_text_only:
        result = parse_headline(line)
        if not result:
            continue
        headlines.append(result[1])
    assert len(headlines) == HEADLINES_PAGE_3, headlines
