# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import hey

power.setup(hey.ROOT)

RESTRUCT_TOC_LINES = 13
# the simple example has two 2 chapters, but there are on the same page,
# therfore 1 page_count.
HOWTO_PYPORTING_TOC_LINES = 12
# porting module
PYPORTING_CHAPTER_COUNT = 6

MASTER72_SECTIONS_AND_WORDS = power.link(
    power.MASTER072_PDF,
    folder='sectionsandwords',
)

BACHELOR111_PAGE_COUNT = 111
TECHNICAL24_PAGE_COUNT = 24
HOWTO_ARGPARSE_PAGE_COUNT = 14

NO_TITLE_EXAMPLE = [
    power.BACHELOR111_PDF,
    power.DOCU07_PDF,
    power.MASTER072_PDF,
    power.MASTER078_PDF,
    power.DOCU09_PDF,
    power.DOCU27_PDF,
    power.DOCU35_PDF,
]
