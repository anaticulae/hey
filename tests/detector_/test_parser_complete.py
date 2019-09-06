# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

from detector.parser.complete import TitlePage
from detector.parser.complete import dump_title_page
from detector.parser.complete import load_title_page
from detector.parser.complete import parse
from hey.textnavigator.navigator import create_pagetextnavigators
from tests import prepare
from tests.fixtures.titlepage import FIRST
from tests.fixtures.titlepage import FIRST_EXPECTED
from tests.fixtures.titlepage import SECOND
from tests.fixtures.titlepage import SECOND_EXPECTED


@pytest.mark.parametrize('page, expected', [
    pytest.param(
        FIRST,
        FIRST_EXPECTED,
        id=prepare(FIRST),
    ),
    pytest.param(
        SECOND,
        SECOND_EXPECTED,
        id=prepare(SECOND),
    ),
])
def test_detector_parse_complete_title_page(page, expected):
    parsed = parse(page)
    assert parsed == expected, str(parsed)


def test_detector_parser_complete_dump_and_load_titlepage():
    current = TitlePage()

    dumped = dump_title_page(current)
    assert len(dumped) > 100, str(dumped)

    loaded = load_title_page(dumped)

    assert loaded == current
