# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import utila

import hey
import hey.example

RESOURCES = os.path.join(hey.ROOT, 'tests/resources')

BACHELOR = os.path.join(RESOURCES, 'bachelor')
BOOK = os.path.join(RESOURCES, 'book')
DOCU = os.path.join(RESOURCES, 'docu')
HOMEWORK = os.path.join(RESOURCES, 'homework')
MASTER = os.path.join(RESOURCES, 'master')
ORDER = os.path.join(RESOURCES, 'order')
TECHNICAL = os.path.join(RESOURCES, 'technical')

GENERATED = os.path.join(RESOURCES, 'generated')
NO_TITLE = os.path.join(GENERATED, 'notitle')

RESTRUCT = os.path.join(GENERATED, 'restruct')
RESTRUCT_PDF = os.path.join(DOCU, 'restructuredtext.pdf')
RESTRUCT_CHAPTER_COUNT = 8
RESTRUCT_TOC_LINES = 13

HOWTO_PYPORTING = os.path.join(GENERATED, 'howto_pyporting')
HOWTO_PYPORTING_PDF = os.path.join(DOCU, 'howto_pyporting.pdf')
# the simple example has two 2 chapters, but there are on the same page,
# therfore 1 page_count.
# TODO: Change after removed xfail, see: test_sections_extract_sections_simple
HOWTO_PYPORTING_CHAPTER_PAGE_COUNT = 1  # change to 2
HOWTO_PYPORTING_HEADLINES_PAGE_3 = 4
HOWTO_PYPORTING_TOC_LINES = 12

# porting module
PYPORTING = os.path.join(GENERATED, 'porting_module')
PYPORTING_PDF = os.path.join(DOCU, 'porting_extension_modules.pdf')
PYPORTING_CHAPTER_COUNT = 6

BACHELOR37 = os.path.join(GENERATED, 'page_37_tables')
BACHELOR37_PDF = os.path.join(BACHELOR, 'page_37_tables.pdf')

BACHELOR56 = os.path.join(GENERATED, 'page_56_hard_to_read')
BACHELOR56_PDF = os.path.join(BACHELOR, 'page_56_hard_to_read.pdf')

BACHELOR63 = os.path.join(GENERATED, 'page_63_images_toc')
BACHELOR63_PDF = os.path.join(BACHELOR, 'page_63_images_toc.pdf')

MASTER72 = os.path.join(GENERATED, 'page_72_noimages_toc')
MASTER72_PDF = os.path.join(MASTER, 'page_72_noimages_toc.pdf')

MASTER89 = os.path.join(GENERATED, 'page_89_noimages_toc')
MASTER89_PDF = os.path.join(MASTER, 'page_89_noimages_toc.pdf')

MASTER116 = os.path.join(GENERATED, 'page_116_images_toc_formular')
MASTER116_PDF = os.path.join(MASTER, 'page_116_images_toc_formular.pdf')

BACHELOR111 = os.path.join(GENERATED, 'page_111_images_toc')
BACHELOR111_PDF = os.path.join(BACHELOR, 'page_111_images_toc.pdf')
BACHELOR111_PAGE_COUNT = 111

TECHNICAL24 = os.path.join(GENERATED, 'technical_24pages')
TECHNICAL24_PDF = os.path.join(TECHNICAL, 'page_24_color_figures_images.pdf')
TECHNICAL24_PAGE_COUNT = 24

TWINE = os.path.join(GENERATED, 'twine')
TWINE_PDF = os.path.join(DOCU, 'twine.pdf')

TWINE_NO_TILE = os.path.join(NO_TITLE, 'docu_twine')

HOWTO_ARGPARSE = os.path.join(GENERATED, 'howto_argparse')
HOWTO_ARGPARSE_PDF = os.path.join(DOCU, 'howto_argparse.pdf')
HOWTO_ARGPARSE_PAGE_COUNT = 14

HOWTOWRITE9 = os.path.join(GENERATED, 'howtowrite_pages9')
HOWTOWRITE9_PDF = os.path.join(ORDER, 'howtowrite_pages9.pdf')

MASTER78_PDF = os.path.join(MASTER, 'page_78_images_toc.pdf')

HOMEWORK50 = os.path.join(GENERATED, 'homework_page_50_math')
HOMEWORK50_PDF = os.path.join(HOMEWORK, 'page_50_math.pdf')

LEFTRIGHT_PDF = os.path.join(BOOK, 'leftright.pdf')
LEFTRIGHT = os.path.join(
    GENERATED,
    'book_leftright',
)

NO_TITLE_EXAMPLE = [
    BACHELOR111_PDF,
    HOWTO_PYPORTING_PDF,
    MASTER72_PDF,
    MASTER78_PDF,
    PYPORTING_PDF,
    RESTRUCT_PDF,
    TWINE_PDF,
]
NO_TITLE_GENERATED = [
    os.path.join(NO_TITLE, item)
    for item in hey.example.output_names(NO_TITLE_EXAMPLE)
]

REQURIED_RESOURCES = [
    # BACHELOR63, TODO: ENABLE LATER
    BACHELOR111,
    BACHELOR111_PDF,
    BACHELOR37,
    BACHELOR37_PDF,
    BACHELOR56,
    BACHELOR56_PDF,
    BACHELOR63_PDF,
    HOMEWORK50,
    HOMEWORK50_PDF,
    HOWTOWRITE9,
    HOWTOWRITE9_PDF,
    HOWTO_ARGPARSE,
    HOWTO_ARGPARSE_PDF,
    HOWTO_PYPORTING,
    HOWTO_PYPORTING_PDF,
    LEFTRIGHT,
    LEFTRIGHT_PDF,
    MASTER116,
    MASTER116_PDF,
    MASTER72,
    MASTER72_PDF,
    MASTER78_PDF,
    MASTER89,
    MASTER89_PDF,
    PYPORTING,
    PYPORTING_PDF,
    RESOURCES,
    RESTRUCT,
    RESTRUCT_PDF,
    TECHNICAL24,
    TECHNICAL24_PDF,
    TWINE,
    TWINE_NO_TILE,
    TWINE_PDF,
]

REQURIED_RESOURCES = [
    utila.forward_slash(item, save_newline=False) for item in REQURIED_RESOURCES
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


def boxed(path: str, prefix: str = '') -> str:
    return pathconnector(path, 'rawmaker', 'boxes_boxes', prefix)


def pagenumbers(path: str, prefix: str = '') -> str:
    return pathconnector(path, 'groupme', 'pagenumbers_pagenumbers', prefix)


def headerfooters(path: str, prefix: str = '') -> str:
    return pathconnector(path, 'groupme', 'footer_footerheader', prefix)
