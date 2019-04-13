# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Test to group chapter out of text and and headlines.
"""

from pytest import fixture
from pytest import mark
from tests.groupme_ import SIMPLE_TEXT

from iamraw import Document
from iamraw import Page
from iamraw import TextContainer
from serializeraw import dump_toc
from serializeraw import load_document
from utila import file_read

from groupme.feature.chapter import chapter
from groupme.feature.chapter import chapter_to_yaml
from groupme.feature.chapter import parse_headline
from groupme.feature.chapter import sections
from groupme.feature.chapter import sections_from_page
from groupme.feature.chapter import toc
from groupme.feature.chapter import toc_from_page
from groupme.feature.chapter import toc_to_yaml

HEADLINES_PAGE_3 = 4

TOC_LINES = 12


def test_extract_chapter():
    """Ensure that every section have an textbody"""
    result = chapter(SIMPLE_TEXT)

    assert len(result) == 3


def test_toc_to_yaml():
    """Ensure that every section have an textbody"""
    tableofcontent, _, _ = chapter(SIMPLE_TEXT)
    toc_yaml = toc_to_yaml(tableofcontent)


def test_content_to_yaml():
    """Ensure that every section have an textbody"""
    _, content, _ = chapter(SIMPLE_TEXT)
    assert len(content) == TOC_LINES
    dumped = chapter_to_yaml(content)
    assert dumped


@fixture
def document() -> Document:
    doc: Document = load_document(SIMPLE_TEXT)
    return doc


@fixture
def page_0(document: Document) -> Page:
    page: Page = document.pages[0]
    return page


@fixture
def page_2(document: Document) -> Page:
    page: Page = document.pages[2]
    return page


@fixture
def page_2_text_only(page_2: Page):
    lines = []
    for child in page_2.children:
        if not isinstance(child, TextContainer):
            continue
        lines.extend(child.text.splitlines())
    return lines


def test_extract_page_2(page_2: Page):
    blocks = sections_from_page(page_2)
    assert len(blocks) == HEADLINES_PAGE_3


def test_extract_toc(page_0: Page):
    toc = toc_from_page(page_0)
    assert len(toc) == TOC_LINES
    # assert len(blocks) == HEADLINES_PAGE_3


def test_extract_toc_from_document(document: Document):
    tableofcontent = toc(document)
    assert len(tableofcontent) == TOC_LINES


def test_extract_document(document: Document):
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


def test_parse_headlines(page_2_text_only):
    # print(len(page_3_text_only))
    # assert 0
    headlines = []
    for line in page_2_text_only:
        result = parse_headline(line)
        if not result:
            continue
        headlines.append(result[1])
    assert len(headlines) == HEADLINES_PAGE_3, headlines
