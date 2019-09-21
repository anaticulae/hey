# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import hey

RESOURCES = os.path.join(hey.ROOT, 'tests/resources')

assert os.path.exists(RESOURCES), RESOURCES

BOXES_BOXES = 'rawmaker__boxes_boxes.yaml'
FONTS_CONTENT = 'rawmaker__fonts_content.yaml'
FONTS_HEADER = 'rawmaker__fonts_header.yaml'
HORIZONTAL = 'rawmaker__boxes_horizontal.yaml'
ONELINE_FONTS_CONTENT = 'rawmaker__oneline_fonts_content.yaml'
ONELINE_FONTS_HEADER = 'rawmaker__oneline_fonts_header.yaml'
ONELINE_POSITION = 'rawmaker__oneline_text_positions.yaml'
ONELINE_TEXT = 'rawmaker__oneline_text_text.yaml'
PAGESIZE = 'rawmaker__border_pages.yaml'
TEXT = 'rawmaker__text_text.yaml'
TEXT_POSITION = 'rawmaker__text_positions.yaml'
TOC = 'rawmaker__toc_toc.yaml'

# restruct

GENERATED = os.path.join(RESOURCES, 'generated')

RESTRUCT = os.path.join(GENERATED, 'restruct')
RESTRUCT_BOXES = os.path.join(RESTRUCT, BOXES_BOXES)
RESTRUCT_FONT_CONTENT = os.path.join(RESTRUCT, FONTS_CONTENT)
RESTRUCT_FONT_HEADER = os.path.join(RESTRUCT, FONTS_HEADER)
RESTRUCT_HORIZONTAL = os.path.join(RESTRUCT, HORIZONTAL)
RESTRUCT_ONELINE_FONT_CONTENT = os.path.join(RESTRUCT, ONELINE_FONTS_CONTENT)
RESTRUCT_ONELINE_FONT_HEADER = os.path.join(RESTRUCT, ONELINE_FONTS_HEADER)
RESTRUCT_ONELINE_POSITION = os.path.join(RESTRUCT, ONELINE_POSITION)
RESTRUCT_ONELINE_TEXT = os.path.join(RESTRUCT, ONELINE_TEXT)
RESTRUCT_PAGESIZE = os.path.join(RESTRUCT, PAGESIZE)
RESTRUCT_PDF = os.path.join(RESOURCES, 'restruct/restructuredtext.pdf')
RESTRUCT_TEXT = os.path.join(RESTRUCT, TEXT)
RESTRUCT_TEXT_POSITION = os.path.join(RESTRUCT, TEXT_POSITION)
RESTRUCT_TOC = os.path.join(RESTRUCT, TOC)

RESTRUCT_TOC_LINES = 13

# simple

SIMPLE = os.path.join(GENERATED, 'simple')
SIMPLE_FONT_CONTENT = os.path.join(SIMPLE, FONTS_CONTENT)
SIMPLE_FONT_HEADER = os.path.join(SIMPLE, FONTS_HEADER)
SIMPLE_HORIZONTAL = os.path.join(SIMPLE, HORIZONTAL)
SIMPLE_ONELINE_FONT_CONTENT = os.path.join(SIMPLE, ONELINE_FONTS_CONTENT)
SIMPLE_ONELINE_FONT_HEADER = os.path.join(SIMPLE, ONELINE_FONTS_HEADER)
SIMPLE_ONELINE_POSITION = os.path.join(SIMPLE, ONELINE_POSITION)
SIMPLE_ONELINE_TEXT = os.path.join(SIMPLE, ONELINE_TEXT)
SIMPLE_PAGESIZE = os.path.join(SIMPLE, PAGESIZE)
SIMPLE_TEXT = os.path.join(SIMPLE, TEXT)
SIMPLE_TEXT_POSITION = os.path.join(SIMPLE, TEXT_POSITION)
SIMPLE_TOC = os.path.join(SIMPLE, TOC)

SIMPLE_HEADLINES_PAGE_3 = 4
SIMPLE_TOC_LINES = 12

# porting module

PYPORTING = os.path.join(GENERATED, 'porting_module')
PYPORTING_FONT_CONTENT = os.path.join(PYPORTING, FONTS_CONTENT)
PYPORTING_FONT_HEADER = os.path.join(PYPORTING, FONTS_HEADER)
PYPORTING_HORIZONTAL = os.path.join(PYPORTING, HORIZONTAL)
PYPORTING_ONELINE_FONT_CONTENT = os.path.join(PYPORTING, ONELINE_FONTS_CONTENT)
PYPORTING_ONELINE_FONT_HEADER = os.path.join(PYPORTING, ONELINE_FONTS_HEADER)
PYPORTING_ONELINE_TEXT = os.path.join(PYPORTING, ONELINE_TEXT)
PYPORTING_PAGESIZE = os.path.join(PYPORTING, PAGESIZE)
PYPORTING_TEXT = os.path.join(PYPORTING, TEXT)
PYPORTING_TEXT_POSITION = os.path.join(PYPORTING, TEXT_POSITION)
PYPORTING_TOC = os.path.join(PYPORTING, TOC)

MASTER = os.path.join(RESOURCES, 'master')
MASTER_72PAGES = os.path.join(GENERATED, 'page_72_noimages_toc')

MASTER_72PAGES_PDF = os.path.join(MASTER, 'page_72_noimages_toc.pdf')
MASTER_78PAGES_PDF = os.path.join(MASTER, 'page_78_images_toc.pdf')

REQURIED_RESOURCES = [
    MASTER_72PAGES,
    MASTER_72PAGES_PDF,
    MASTER_78PAGES_PDF,
    PYPORTING,
    PYPORTING_FONT_CONTENT,
    PYPORTING_FONT_HEADER,
    PYPORTING_HORIZONTAL,
    PYPORTING_ONELINE_FONT_CONTENT,
    PYPORTING_ONELINE_FONT_HEADER,
    PYPORTING_ONELINE_TEXT,
    PYPORTING_PAGESIZE,
    PYPORTING_TEXT,
    PYPORTING_TEXT_POSITION,
    PYPORTING_TOC,
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
    RESTRUCT_PDF,
    RESTRUCT_TEXT,
    RESTRUCT_TEXT_POSITION,
    RESTRUCT_TOC,
    SIMPLE,
    SIMPLE_FONT_CONTENT,
    SIMPLE_FONT_HEADER,
    SIMPLE_HORIZONTAL,
    SIMPLE_ONELINE_FONT_CONTENT,
    SIMPLE_ONELINE_FONT_HEADER,
    SIMPLE_ONELINE_POSITION,
    SIMPLE_ONELINE_TEXT,
    SIMPLE_PAGESIZE,
    SIMPLE_TEXT,
    SIMPLE_TEXT_POSITION,
    SIMPLE_TOC,
]
