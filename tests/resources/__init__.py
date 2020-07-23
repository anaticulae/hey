# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utila
import utilatest

import hey

RESOURCES = os.path.join(hey.ROOT, 'tests/resources')

GENERATED = os.path.join(RESOURCES, 'generated')
# TODO: remove _ after fixing path bug
NO_TITLE = os.path.join(GENERATED, '_notitle')

RESTRUCT = os.path.join(GENERATED, 'restruct')
RESTRUCT_TOC_LINES = 13

HOWTO_PYPORTING = os.path.join(GENERATED, 'howto_pyporting')
# the simple example has two 2 chapters, but there are on the same page,
# therfore 1 page_count.
HOWTO_PYPORTING_TOC_LINES = 12

# porting module
PYPORTING = os.path.join(GENERATED, 'porting_module')
PYPORTING_CHAPTER_COUNT = 6

BACHELOR37 = os.path.join(GENERATED, 'page_37_tables')
BACHELOR56 = os.path.join(GENERATED, 'page_56_hard_to_read')
BACHELOR63 = os.path.join(GENERATED, 'page_63_images_toc')
BACHELOR90 = os.path.join(GENERATED, 'bachelor90')
BACHELOR76 = os.path.join(GENERATED, 'page76')

MASTER72 = os.path.join(GENERATED, 'page_72_noimages_toc')
MASTER72_SECTIONS_AND_WORDS = os.path.join(GENERATED, 'page72_sectionswords')

MASTER83 = os.path.join(GENERATED, 'page_83_noimages_toc')
MASTER89 = os.path.join(GENERATED, 'page_89_noimages_toc')
MASTER98 = os.path.join(GENERATED, 'master98')
MASTER99 = os.path.join(GENERATED, 'master99')
MASTER116 = os.path.join(GENERATED, 'page_116_images_toc_formular')

BACHELOR111 = os.path.join(GENERATED, 'page_111_images_toc')
BACHELOR111_PAGE_COUNT = 111

BACHELOR241 = os.path.join(GENERATED, 'page241')

TECHNICAL24 = os.path.join(GENERATED, 'technical_24pages')
TECHNICAL24_PAGE_COUNT = 24

TWINE = os.path.join(GENERATED, 'twine')
TWINE_NO_TILE = os.path.join(NO_TITLE, 'docu_twine')

HOWTO_ARGPARSE = os.path.join(GENERATED, 'howto_argparse')
HOWTO_ARGPARSE_PAGE_COUNT = 14

HOWTOWRITE9 = os.path.join(GENERATED, 'howtowrite_pages9')
MASTER78 = os.path.join(GENERATED, 'page_78_images_toc')
HOMEWORK50 = os.path.join(GENERATED, 'homework_page_50_math')
LEFTRIGHT = os.path.join(GENERATED, 'book_leftright')

NO_TITLE_EXAMPLE = [
    power.BACHELOR111_PDF,
    power.DOCU07_PDF,
    power.MASTER072_PDF,
    power.MASTER078_PDF,
    power.DOCU09_PDF,
    power.DOCU27_PDF,
    power.DOCU35_PDF,
]
NO_TITLE_GENERATED = [
    os.path.join(NO_TITLE, item)
    for item in utilatest.simplify_testfile_names(NO_TITLE_EXAMPLE)
]

NO_TITLE_RESTRUCTURED = os.path.join(NO_TITLE, 'docu_restructuredtext')

REQURIED_RESOURCES = [
    BACHELOR111,
    BACHELOR37,
    BACHELOR56,
    BACHELOR63,
    BACHELOR76,
    BACHELOR90,
    HOMEWORK50,
    HOWTOWRITE9,
    HOWTO_ARGPARSE,
    HOWTO_PYPORTING,
    LEFTRIGHT,
    MASTER116,
    MASTER72,
    MASTER72_SECTIONS_AND_WORDS,
    MASTER78,
    MASTER83,
    MASTER89,
    MASTER98,
    MASTER99,
    PYPORTING,
    RESOURCES,
    RESTRUCT,
    TECHNICAL24,
    TWINE,
    TWINE_NO_TILE,
]

REQURIED_RESOURCES = [utila.forward_slash(item) for item in REQURIED_RESOURCES]
