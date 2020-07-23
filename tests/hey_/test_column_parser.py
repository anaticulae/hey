# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import hey.geometry.double_column
import tests.resources


def test_parse_column_bachelor63_page59():
    """Latex double column. Left side with [Hem10] pattern"""
    pages = (59)
    navigators = serializeraw.create_pagetextnavigators_frompath(
        tests.resources.BACHELOR63,
        # fill_empty=False,
        pages=pages,
    )
    parsed = hey.geometry.double_column.parse_page(navigators[0])
    assert len(parsed) == 12, str(parsed)


def test_parse_column_bachelor63_page59_all_columns():
    """Latex double column. Left side with [Hem10] pattern"""
    pages = (59,)
    navigators = serializeraw.create_pagetextnavigators_frompath(
        tests.resources.BACHELOR63,
        # fill_empty=False,
        pages=pages,
    )
    page = navigators[0]
    marker = hey.geometry.double_column.columns(page)
    (short, description), _ = hey.geometry.double_column.split_bymarker(
        page,
        marker,
    ) # yapf:disable
    inside_all = hey.geometry.double_column.all_columns(
        [short, description],
        vertical_diff=5.0,
    )
    text = [item.text.strip() for item in inside_all]
    # reducing vertical diff leads to droping out of detection
    assert '[Ohm91]' in text, text
