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


@pytest.mark.parametrize('name,expected', [
    pytest.param(100, 112, id='100'),
    pytest.param(150, 172, id='150'),
    pytest.param(200, 230, id='200'),
])
def test_line_distance_percent_x(name, expected):
    # TODO: ADJUST EXPECTED LATER
    source = os.path.join(tests.LINESGENERATED, f'linedistances_percent{name}')
    if not utila.exists(source):
        pytest.skip(f'generate {name}')
    result = doctextstyle.extractor.extract(source)
    distance = result.text_distance / result.text_size
    distance = utila.roundme(distance * 100, digits=0)
    assert distance == expected
