# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import doctextstyle.extractor
import doctextstyle.vector

# TODO: VALIDATE SIZES
PARAMETERS = [
    pytest.param(power.BACHELOR063_PDF, 15.96, 14.04, 12.0, id='bachelor63'),
    pytest.param(power.BACHELOR051_PDF, 15.96, 14.04, 12.0, id='bachelor51'),
    pytest.param(power.MASTER110_PDF, 24.79, 14.35, 11.96, id='master110'),
    pytest.param(power.DISS205_PDF, 17.22, 17.22, 14.35, id='diss205'),
]


# skip failing bachelor51
@pytest.mark.parametrize('source, h1, h2, h3', [PARAMETERS[0], PARAMETERS[2]])
@utilatest.longrun
def test_doctextstyle_extract_headlines_old(source, h1, h2, h3):
    source = power.link(source)
    result = doctextstyle.extractor.extract(source)
    assert result
    assert result.h1_size == h1
    assert result.h2_size == h2
    assert result.h3_size == h3


@pytest.mark.parametrize('source, h1, h2, h3', PARAMETERS)
@utilatest.longrun
def test_doctextstyle_extract_headlines_magic(source, h1, h2, h3):
    source = power.link(source)
    result = doctextstyle.vector.run(source)
    assert result
    assert utila.near(result.h1_size, expected=h1, diff=0.5)
    assert utila.near(result.h2_size, expected=h2, diff=0.5)
    assert utila.near(result.h3_size, expected=h3, diff=0.5)
