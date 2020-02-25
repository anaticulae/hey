# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import groupme.abbreviation.parser
import hey.textnavigator.navigator
import tests.resources


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(tests.resources.MASTER116, 96, 8, id='master116'),
    pytest.param(tests.resources.HOMEWORK50, 6, 18, id='homework50'),
    pytest.param(
        tests.resources.BACHELOR37,
        1,
        26,
        id='bachelor37',
        marks=pytest.mark.xfail(reason='require more complex strategy'),
    ),
])
def test_abbreviation_parse_example(source, pages, expected):
    ptn = hey.textnavigator.navigator.create_pagetextnavigators_frompath(
        source,
        prefix='oneline',
        pages=pages,
    )
    content = ptn
    parsed = groupme.abbreviation.parser.parse(content)
    assert parsed, parsed
    assert len(parsed) == expected, str(parsed)
