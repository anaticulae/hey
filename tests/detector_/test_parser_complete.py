# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from detector.parser.complete import parse
from tests.fixtures.titlepage import FIRST
from tests.fixtures.titlepage import FIRST_EXPECTED


def test_detector_parser_complete_parse():
    parsed = parse(FIRST)

    assert parsed == FIRST_EXPECTED, str(parsed)
