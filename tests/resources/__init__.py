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
from typing import List

from iamraw import Border
from iamraw import Document
from iamraw import Page
from iamraw import TextContainer
from pytest import fixture
from pytest import mark
from serializeraw import load_document
from serializeraw import load_pageborders

from groupme.feature.numbers import load_textposition
from hey import ROOT
from hey.textnavigator.navigator import PageTextNavigator
from hey.textnavigator.navigator import create_pagetextnavigator

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
def simpledocument() -> Document:
    doc: Document = load_document(SIMPLE_TEXT)
    return doc


TextPageNavigators = List[PageTextNavigator]


@fixture
def simplepagetextnavigators(
        simpledocument: Document,  #pylint:disable=W0621
) -> TextPageNavigators:
    textpositions = load_textposition(SIMPLE_POSITION)

    return create_pagetextnavigator(textpositions, simpledocument)


@fixture
def simplepagesize():
    size, _ = load_pageborders(SIMPLE_PAGESIZE)
    return size


@fixture
def simplecontentborder():
    _, border = load_pageborders(SIMPLE_PAGESIZE)
    return border


@fixture
def simplepage_0(simpledocument: Document) -> Page:  # pylint: disable=W0621
    page: Page = simpledocument[0]
    return page


@fixture
def simplepage_2(simpledocument: Document) -> Page:  # pylint: disable=W0621
    page: Page = simpledocument[2]
    return page


@fixture
def simplepage_2_text_only(simplepage_2: Page):  # pylint: disable=W0621
    lines = []
    for child in simplepage_2:
        if not isinstance(child, TextContainer):
            continue
        lines.extend(child.text.splitlines())
    return lines


# TODO: Reduce amout of fixtures
@fixture
def simple_second_page_navigator(simplepagetextnavigators) -> PageTextNavigator:
    return simplepagetextnavigators[1]


@fixture
def simple_second_page_size(simplecontentborder) -> Border:
    return simplecontentborder[1]
