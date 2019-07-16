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

from iamraw import Border
from iamraw import Document
from iamraw import Page
from iamraw import TextContainer
from pytest import fixture
from serializeraw import load_document
from serializeraw import load_horizontals
from serializeraw import load_pageborders

from groupme.feature.numbers import load_textposition
from hey import ROOT
from hey.fonts.store import FontStore
from hey.fonts.store import create_fontstore
from hey.textnavigator.navigator import PageTextNavigator
from hey.textnavigator.navigator import PageTextNavigators
from hey.textnavigator.navigator import create_pagetextnavigators
from sections.creator import add_chapter
from sections.creator import add_content
from sections.creator import add_index
from sections.creator import add_introduction
from sections.creator import add_table
from sections.creator import add_text
from sections.creator import add_title
from sections.creator import add_toc
from sections.creator import add_whitepage
from sections.creator import validate
from sections.ctor import PERCENT_100
from sections.ctor import Sections
from sections.feature.chapter import work as work_chapter
from sections.feature.index import work as work_index
from sections.feature.title import work as work_title
from sections.feature.toc import work as work_toc
from sections.feature.whitepage import work as work_whitepage

TEST_DATA = join(ROOT, 'tests/resources')

assert exists(TEST_DATA), TEST_DATA

RESTRUCT = join(TEST_DATA, 'restruct')
RESTRUCT_BOXES = join(RESTRUCT, 'rawmaker__boxes_boxes.yaml')
RESTRUCT_FONT_CONTENT = join(RESTRUCT, 'rawmaker__fonts_content.yaml')
RESTRUCT_FONT_HEADER = join(RESTRUCT, 'rawmaker__fonts_header.yaml')
RESTRUCT_HORIZONTAL = join(RESTRUCT, 'rawmaker__boxes_horizontal.yaml')
RESTRUCT_ONELINE_FONT_CONTENT = join(RESTRUCT,
                                     'rawmaker__oneline_fonts_content.yaml')
RESTRUCT_ONELINE_FONT_HEADER = join(RESTRUCT,
                                    'rawmaker__oneline_fonts_header.yaml')
RESTRUCT_ONELINE_POSITION = join(RESTRUCT,
                                 'rawmaker__oneline_text_positions.yaml')
RESTRUCT_ONELINE_TEXT = join(RESTRUCT, 'rawmaker__oneline_text_text.yaml')
RESTRUCT_PAGESIZE = join(RESTRUCT, 'rawmaker__border_pages.yaml')
RESTRUCT_TEXT = join(RESTRUCT, 'rawmaker__text_text.yaml')
RESTRUCT_TEXT_POSITION = join(RESTRUCT, 'rawmaker__text_positions.yaml')
RESTRUCT_TOC = join(RESTRUCT, 'rawmaker__toc_toc.yaml')

RESTRUCT_TOC_LINES = 13

SIMPLE = join(TEST_DATA, 'simple')
SIMPLE_FONT_CONTENT = join(SIMPLE, 'rawmaker__fonts_content.yaml')
SIMPLE_FONT_HEADER = join(SIMPLE, 'rawmaker__fonts_header.yaml')
SIMPLE_HORIZONTAL = join(SIMPLE, 'rawmaker__boxes_horizontal.yaml')
SIMPLE_PAGESIZE = join(SIMPLE, 'rawmaker__border_pages.yaml')
SIMPLE_POSITION = join(SIMPLE, 'rawmaker__text_positions.yaml')
SIMPLE_TEXT = join(SIMPLE, 'rawmaker__text_text.yaml')
SIMPLE_TOC = join(SIMPLE, 'rawmaker__toc_toc.yaml')

SIMPLE_HEADLINES_PAGE_3 = 4
SIMPLE_TOC_LINES = 12

for item in [
        RESTRUCT,
        RESTRUCT_BOXES,
        RESTRUCT_FONT_CONTENT,
        RESTRUCT_FONT_HEADER,
        RESTRUCT_HORIZONTAL,
        RESTRUCT_ONELINE_FONT_CONTENT,
        RESTRUCT_ONELINE_FONT_HEADER,
        RESTRUCT_ONELINE_POSITION,
        RESTRUCT_ONELINE_TEXT,
        RESTRUCT_PAGESIZE,
        RESTRUCT_TEXT,
        RESTRUCT_TEXT_POSITION,
        RESTRUCT_TOC,
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
