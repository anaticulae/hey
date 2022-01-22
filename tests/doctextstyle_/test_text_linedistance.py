# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utila

import doctextstyle.extractor
import tests


@pytest.mark.parametrize(
    'expected',
    [
        pytest.param(100, id='100'),
        pytest.param(150, id='150'),
        pytest.param(200, id='200'),
    ],
)
@pytest.mark.xfail(reason='enable later')
def test_line_distance_percent_x(expected):
    source = os.path.join(tests.LINESGENERATED, f'percent{expected}')
    result = doctextstyle.extractor.extract(source)
    distance = result.text_distance / result.text_size
    distance = utila.roundme(distance * 100, digits=0)
    assert distance == expected
