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

from detector.parser.matrikel import parse


@pytest.mark.parametrize('raw, expected', [
    (
        '   Matrikelnummer: 519448   ',
        iamraw.Matrikel(519448, 'Matrikelnummer:', 'Matrikelnummer: 519448'),
    ),
    (
        'Matrikel-Nr. 1024577',
        iamraw.Matrikel(1024577, 'Matrikel-Nr.', 'Matrikel-Nr. 1024577'),
    ),
    (
        '   vorgelegt von: 321240',
        iamraw.Matrikel(321240, 'vorgelegt von:', 'vorgelegt von: 321240'),
    ),
    (
        '   16348',
        iamraw.Matrikel(16348, '', '16348'),
    ),
    (
        '321240',
        iamraw.Matrikel(321240, '', '321240'),
    ),
])
def test_parse_matrikel(raw, expected):
    parsed = parse(raw)
    assert parsed == expected, str(parsed)
