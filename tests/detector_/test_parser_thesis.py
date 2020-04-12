# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest

import detector.parser.thesis


@pytest.mark.parametrize('raw, expected', [
    (
        'Masterarbeit',
        iamraw.TitleThesisType(
            iamraw.DocumentType.MASTER,
            'Masterarbeit',
            'Masterarbeit',
        ),
    ),
    (
        'Promotion',
        iamraw.TitleThesisType(
            iamraw.DocumentType.DOCTOR,
            'Promotion',
            'Promotion',
        ),
    ),
])
def test_parse_thesis(raw, expected):
    parsed = detector.parser.thesis.parse(raw)
    assert parsed == expected, str(parsed)
