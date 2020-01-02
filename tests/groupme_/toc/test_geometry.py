# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.toc.extractor as gte
import groupme.toc.strategy.geometry as gtsg
import tests.fixtures.tableofcontent as tft


def test_groupme_toc_strategy_geometry():
    headlines = tft.bachelor111_toc()

    expected = [3, 16, 8, 5, 7, 8, 3, 1, 4, 1, 1, 1, 9]

    active = [
        gtsg.GeometryTocExtractor,
    ]
    grouped = gte.extract(
        headlines,
        active=active,
    )
    current = [len(item) for item in grouped]
    assert current == expected
