# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import mark
from pytest import param

from detector.parser.complete import parse
from tests import prepare
from tests.fixtures.titlepage import FIRST
from tests.fixtures.titlepage import FIRST_EXPECTED
from tests.fixtures.titlepage import SECOND
from tests.fixtures.titlepage import SECOND_EXPECTED


@mark.parametrize('page, expected', [
    param(
        FIRST,
        FIRST_EXPECTED,
        id=prepare(FIRST),
    ),
    param(
        SECOND,
        SECOND_EXPECTED,
        id=prepare(SECOND),
    ),
])
def test_detector_parse_complete_title_page(page, expected):
    parsed = parse(page)
    assert parsed == expected, str(parsed)
