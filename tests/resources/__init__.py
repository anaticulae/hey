# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import exists
from os.path import join

from iamraw import Document
from iamraw import Page
from iamraw import TextContainer
from pytest import fixture
from pytest import mark
from serializeraw import load_document

from hey import ROOT

TEST_DATA = join(ROOT, 'tests/resources')

assert exists(TEST_DATA), TEST_DATA

RESTRUCT = join(TEST_DATA, 'restruct')
RESTRUCT_FONT_CONTENT = join(RESTRUCT, 'rawmaker__fonts_content.yaml')
RESTRUCT_FONT_HEADER = join(RESTRUCT, 'rawmaker__fonts_header.yaml')
RESTRUCT_HORIZONTAL = join(RESTRUCT, 'rawmaker__boxes_horizontal.yaml')
RESTRUCT_ONELINE_POSITION = join(RESTRUCT,
                                 'rawmaker__oneline_text_positions.yaml')
RESTRUCT_ONELINE_TEXT = join(RESTRUCT, 'rawmaker__oneline_text_text.yaml')
RESTRUCT_PAGESIZE = join(RESTRUCT, 'rawmaker__border_pages.yaml')
RESTRUCT_POSITION = join(RESTRUCT, 'rawmaker__text_positions.yaml')
RESTRUCT_TEXT = join(RESTRUCT, 'rawmaker__text_text.yaml')
RESTRUCT_TOC = join(RESTRUCT, 'rawmaker__toc.yaml')

RESTRUCT_TOC_LINES = 13

SIMPLE = join(TEST_DATA, 'simple')
SIMPLE_PAGESIZE = join(SIMPLE, 'rawmaker__border_pages.yaml')
SIMPLE_POSITION = join(SIMPLE, 'rawmaker__text_positions.yaml')
SIMPLE_TEXT = join(SIMPLE, 'rawmaker__text_text.yaml')
SIMPLE_TOC = join(SIMPLE, 'rawmaker__toc.yaml')
SIMPLE_HORIZONTAL = join(SIMPLE, 'rawmaker__boxes_horizontal.yaml')
SIMPLE_FONT_HEADER = join(SIMPLE, 'rawmaker__fonts_header.yaml')
SIMPLE_FONT_CONTENT = join(SIMPLE, 'rawmaker__fonts_content.yaml')

SIMPLE_HEADLINES_PAGE_3 = 4
SIMPLE_TOC_LINES = 12

for item in [
        RESTRUCT,
        RESTRUCT_FONT_CONTENT,
        RESTRUCT_FONT_HEADER,
        RESTRUCT_HORIZONTAL,
        RESTRUCT_ONELINE_POSITION,
        RESTRUCT_ONELINE_TEXT,
        RESTRUCT_PAGESIZE,
        RESTRUCT_POSITION,
        RESTRUCT_TEXT,
        SIMPLE,
        SIMPLE_FONT_CONTENT,
        SIMPLE_FONT_HEADER,
        SIMPLE_HORIZONTAL,
        SIMPLE_PAGESIZE,
        SIMPLE_POSITION,
        SIMPLE_TEXT,
        SIMPLE_TOC,
]:
    msg = 'missing resource: %s' % item
    assert exists(item), item


@fixture
def document() -> Document:
    doc: Document = load_document(SIMPLE_TEXT)
    return doc


@fixture
def page_0(document: Document) -> Page:  # pylint: disable=W0621
    page: Page = document.pages[0]
    return page


@fixture
def page_2(document: Document) -> Page:  # pylint: disable=W0621
    page: Page = document.pages[2]
    return page


@fixture
def page_2_text_only(page_2: Page):  # pylint: disable=W0621
    lines = []
    for child in page_2.children:
        if not isinstance(child, TextContainer):
            continue
        lines.extend(child.text.splitlines())
    return lines
