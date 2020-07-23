# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest

import groupme.abbreviation.geometry


def bachelor37():
    content = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.BACHELOR037_PDF),
        pages=2,
    )
    content = groupme.abbreviation.AbbreviationData(normal=content)
    return content


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(
        power.link(power.BACHELOR037_PDF),
        1,
        26,
        id='bachelor37_abbrev',
    ),
    pytest.param(
        power.link(power.BACHELOR037_PDF),
        2,
        10,
        id='bachelor37_figure',
    ),
    pytest.param(power.link(power.HOMEWORK050_PDF), 6, 0, id='homework50'),
    pytest.param(power.link(power.MASTER116_PDF), 96, 8, id='master116'),
])
@utilatest.skip_longrun
def test_abbreviation_parse_strategy_geometry(source, pages, expected):
    content = serializeraw.create_pagetextnavigators_frompath(
        source,
        pages=pages,
    )
    content = groupme.abbreviation.AbbreviationData(normal=content)
    strategy = groupme.abbreviation.geometry.GeometryAbbreviationParser(content)
    parsed = strategy.result()
    assert len(parsed) == expected, len(parsed)


def test_abbreviation_geometry_columns():
    page = bachelor37().normal[0]  # pylint:disable=E1136
    columns = groupme.abbreviation.geometry.columns(page)
    content = [
        groupme.abbreviation.geometry.column_data(page, column)
        for column in columns
    ]
    assert len(content) == 2
    assert len(content[0]) == 11
    assert len(content[1]) == 20, str(content[1])


def test_abbreviation_geometry_all_columns():
    page = bachelor37().normal[0]  # pylint:disable=E1136
    columns = [
        groupme.abbreviation.geometry.column_data(page, x0=item)
        for item in groupme.abbreviation.geometry.columns(page)
    ]
    all_columns = groupme.abbreviation.geometry.all_columns(columns)
    assert len(all_columns) == 20, str(all_columns)
