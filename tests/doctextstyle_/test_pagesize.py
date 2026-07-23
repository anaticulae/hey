# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw.path
import utilotest

import doctextstyle.features.pagesize


@utilotest.requires(hoverpower.MASTER116_PDF)
def test_pagesize():
    path = iamraw.path.sizeandborder(hoverpower.link(hoverpower.MASTER116_PDF))
    sizes = doctextstyle.features.pagesize.pagesizes(path)
    assert len(sizes) == 2
