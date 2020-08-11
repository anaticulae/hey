# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.toc.decider

EXAMPLE = [
    groupme.toc.decider.ExtractionStatistic(
        validitem_count=67,
        group_count=13,
        oneline_factor=0.31,
    ),
    groupme.toc.decider.ExtractionStatistic(
        validitem_count=67,
        group_count=17,
        oneline_factor=0.53,
    ),
    groupme.toc.decider.ExtractionStatistic(
        validitem_count=64,
        group_count=17,
        oneline_factor=0.53,
    ),
]


def test_groupme_toc_decider_sort_decisions():
    assert sorted(EXAMPLE) == EXAMPLE
