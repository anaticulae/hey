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

import groupme.abbreviation.simple


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.link(power.HOMEWORK050_PDF), 6, 18, id='homework50'),
    pytest.param(power.link(power.MASTER116_PDF), 96, 8, id='master116'),
    pytest.param(
        power.link(power.BACHELOR037_PDF),
        1,
        26,
        id='bachelor37',
        marks=pytest.mark.xfail(reason='require more complex strategy'),
    ),
])
@utilatest.skip_longrun
def test_abbreviation_parse_simple(source, pages, expected):
    content = serializeraw.create_pagetextnavigators_frompath(
        source,
        prefix='oneline',
        pages=pages,
    )
    content = groupme.abbreviation.AbbreviationData(oneline=content)
    strategy = groupme.abbreviation.simple.SimpleAbbreviationParser(content)
    parsed = strategy.result()
    assert parsed, parsed
    assert len(parsed) == expected, str(parsed)
