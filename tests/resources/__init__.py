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

from hey import ROOT

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
SIMPLE_TEXT_POSITION = join(SIMPLE, 'rawmaker__text_positions.yaml')
SIMPLE_ONELINE_TEXT = join(SIMPLE, 'rawmaker__oneline_text_text.yaml')
SIMPLE_ONELINE_FONT_CONTENT = join(SIMPLE,
                                   'rawmaker__oneline_fonts_content.yaml')
SIMPLE_ONELINE_FONT_HEADER = join(SIMPLE, 'rawmaker__oneline_fonts_header.yaml')

SIMPLE_HEADLINES_PAGE_3 = 4
SIMPLE_TOC_LINES = 12

RESOURCES = [
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
    SIMPLE_ONELINE_FONT_CONTENT,
    SIMPLE_ONELINE_FONT_HEADER,
    SIMPLE_ONELINE_TEXT,
    SIMPLE_PAGESIZE,
    SIMPLE_POSITION,
    SIMPLE_TEXT,
    SIMPLE_TOC,
]
