# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import detector.literature.column
import tests.resources


def test_parse_literature_bachelor63_page59():
    """Latex double column. Left side with [Hem10] pattern"""
    pages = (59)
    navigators = serializeraw.create_pagetextnavigators_frompath(
        tests.resources.BACHELOR63,
        # fill_empty=False,
        pages=pages,
    )
    parsed = detector.literature.column.extracts(navigators)
    assert len(parsed) == 12, str(parsed)
