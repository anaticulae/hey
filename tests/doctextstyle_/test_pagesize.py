# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path

import doctextstyle.features.pagesize
import tests.resources


def test_pagesize():
    path = iamraw.path.sizeandborder(tests.resources.MASTER116)
    sizes = doctextstyle.features.pagesize.pagesizes(path)
    assert len(sizes) == 2
