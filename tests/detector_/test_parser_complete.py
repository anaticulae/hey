# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import serializeraw

import detector.cli
import detector.feature.titlepage
import detector.parser.complete
import hey.textnavigator.navigator
import hey.textnavigator.style
import tests
import tests.fixtures.titlepage
import tests.resources


@pytest.mark.parametrize('page, expected', [
    pytest.param(
        tests.fixtures.titlepage.FIRST,
        tests.fixtures.titlepage.FIRST_EXPECTED,
        id=tests.prepare(tests.fixtures.titlepage.FIRST),
    ),
    pytest.param(
        tests.fixtures.titlepage.SECOND,
        tests.fixtures.titlepage.SECOND_EXPECTED,
        id=tests.prepare(tests.fixtures.titlepage.SECOND),
    ),
    pytest.param(
        tests.fixtures.titlepage.THIRD,
        tests.fixtures.titlepage.THIRD_EXPECTED,
        id=tests.prepare(tests.fixtures.titlepage.THIRD),
    ),
])
def test_detector_parse_complete_title_page(page, expected):
    pcn = hey.textnavigator.navigator.create_pagetextnavigator_fromstr(page)
    parsed = detector.parser.complete.parse(pcn)
    assert parsed == expected, str(parsed)


def test_detector_parser_complete_dump_and_load_titlepage():
    current = iamraw.TitlePage()

    dumped = serializeraw.dump_titlepage(current)
    assert len(dumped) > 100, str(dumped)

    loaded = serializeraw.load_titlepage(dumped)
    assert loaded == current
