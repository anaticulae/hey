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

RESTRUCT_CHAPTER_COUNT = 8
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

# the simple example has two 2 chapters, but there are on the same page,
# therfore 1 page_count.
# TODO: Change after removed xfail, see: test_sections_extract_sections_simple
SIMPLE_CHAPTER_PAGE_COUNT = 1  # change to 2
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
PYPORTING_CHAPTER_COUNT = 6

MASTER = os.path.join(RESOURCES, 'master')
MASTER_72PAGES = os.path.join(GENERATED, 'page_72_noimages_toc')

HOWTO_ARGPARSE = os.path.join(GENERATED, 'howto_argparse')
HOWTO_ARGPARSE_PDF = os.path.join(RESOURCES, 'howto_argparse/howto_argparse.pdf') # yapf:disable

MASTER_72PAGES_PDF = os.path.join(MASTER, 'page_72_noimages_toc.pdf')
MASTER_78PAGES_PDF = os.path.join(MASTER, 'page_78_images_toc.pdf')

REQURIED_RESOURCES = [
    HOWTO_ARGPARSE,
    HOWTO_ARGPARSE_PDF,
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


def pathconnector(
        path: str,
        runner: str,
        filename: str,
        prefix: str = '',
) -> str:
    assert os.path.isdir(path), str(path)
    prefix = f'{prefix}_' if prefix else ''
    filename = f'{runner}__{prefix}{filename}.yaml'
    result = os.path.join(path, filename)
    return result


# TODO: MOVE TO RAWMAKER
def text(path: str, prefix: str = '') -> str:
    """Add text file name of `rawmaker` to given `path

    Pattern:
        {path}_rawmaker_{prefix}_text_text.yaml

    Args:
        path(str): path to extracted `rawmaker`-content
        prefix(str): optional {prefix} to separate rawmaker-files
    Returns:
        comined path
    """
    return pathconnector(path, 'rawmaker', 'text_text', prefix)


def text_positions(path: str, prefix: str = '') -> str:
    return pathconnector(path, 'rawmaker', 'text_positions', prefix)


def toc(path: str, prefix: str = '') -> str:
    return pathconnector(path, 'rawmaker', 'toc_toc', prefix)


def font_header(path: str, prefix: str = '') -> str:
    return pathconnector(path, 'rawmaker', 'fonts_header', prefix)


def font_content(path: str, prefix: str = '') -> str:
    return pathconnector(path, 'rawmaker', 'fonts_content', prefix)


def sizeandborder(path: str, prefix: str = '') -> str:
    return pathconnector(path, 'rawmaker', 'border_pages', prefix)


def horizontals(path: str, prefix: str = '') -> str:
    return pathconnector(path, 'rawmaker', 'boxes_horizontal', prefix)


def sections(path: str, prefix: str = '') -> str:
    return pathconnector(path, 'sections', 'sections_result', prefix)
