# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import mark

from detector.parser.thesis import Thesis
from detector.parser.thesis import TitleThesisType
from detector.parser.thesis import parse


@mark.parametrize('raw, expected', [
    (
        'Masterarbeit',
        TitleThesisType(Thesis.MASTER, 'Masterarbeit', 'Masterarbeit'),
    ),
    (
        'Promotion',
        TitleThesisType(Thesis.DOCTOR, 'Promotion', 'Promotion'),
    ),
])
def test_parse_thesis(raw, expected):
    parsed = parse(raw)
    assert parsed == expected, str(parsed)
