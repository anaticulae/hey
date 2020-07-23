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

power.setup(hey.ROOT)

RESTRUCT = power.link(power.DOCU27_PDF)
RESTRUCT_TOC_LINES = 13

HOWTO_PYPORTING = power.link(power.DOCU07_PDF)
# the simple example has two 2 chapters, but there are on the same page,
# therfore 1 page_count.
HOWTO_PYPORTING_TOC_LINES = 12

# porting module
PYPORTING = power.link(power.DOCU09_PDF)
PYPORTING_CHAPTER_COUNT = 6

BACHELOR37 = power.link(power.BACHELOR037_PDF)
BACHELOR56 = power.link(power.BACHELOR056_PDF)
BACHELOR63 = power.link(power.BACHELOR063_PDF)
BACHELOR90 = power.link(power.BACHELOR090_PDF)
BACHELOR76 = power.link(power.BACHELOR076_PDF)

MASTER72 = power.link(power.MASTER072_PDF)
MASTER72_SECTIONS_AND_WORDS = power.link(
    power.MASTER072_PDF,
    folder='sectionsandwords',
)

MASTER83 = power.link(power.MASTER083_PDF)
MASTER89 = power.link(power.MASTER089_PDF)
MASTER98 = power.link(power.MASTER098_PDF)
MASTER99 = power.link(power.MASTER099_PDF)

MASTER116 = power.link(power.MASTER116_PDF)

BACHELOR111 = power.link(power.BACHELOR111_PDF)
BACHELOR111_PAGE_COUNT = 111

BACHELOR241 = power.link(power.BACHELOR241_PDF)

TECHNICAL24 = power.link(power.TECHNICAL_024)
TECHNICAL24_PAGE_COUNT = 24

TWINE = power.link(power.DOCU35_PDF)
TWINE_NO_TILE = power.link(power.DOCU35_PDF, folder='notitle')

HOWTO_ARGPARSE = power.link(power.DOCU14_PDF)
HOWTO_ARGPARSE_PAGE_COUNT = 14

HOWTOWRITE9 = power.link(power.ORDER009_PDF)
MASTER78 = power.link(power.MASTER078_PDF)
HOMEWORK50 = power.link(power.HOMEWORK050_PDF)
LEFTRIGHT = power.link(power.BOOK007_PDF)

NO_TITLE_EXAMPLE = [
    power.BACHELOR111_PDF,
    power.DOCU07_PDF,
    power.MASTER072_PDF,
    power.MASTER078_PDF,
    power.DOCU09_PDF,
    power.DOCU27_PDF,
    power.DOCU35_PDF,
]

NO_TITLE_RESTRUCTURED = power.link(power.DOCU27_PDF, folder='notitle')
