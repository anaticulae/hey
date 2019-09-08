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

from detector.parser.thesis import TitleThesisType
from detector.parser.thesis import parse


@pytest.mark.parametrize('raw, expected', [
    (
        'Masterarbeit',
        TitleThesisType(
            iamraw.DocumentType.MASTER,
            'Masterarbeit',
            'Masterarbeit',
        ),
    ),
    (
        'Promotion',
        TitleThesisType(
            iamraw.DocumentType.DOCTOR,
            'Promotion',
            'Promotion',
        ),
    ),
])
def test_parse_thesis(raw, expected):
    parsed = parse(raw)
    assert parsed == expected, str(parsed)
