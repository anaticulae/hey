# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utilatest

import doctextstyle.extractor


@pytest.mark.parametrize('source, h1, h2, h3', [
    pytest.param(power.BACHELOR063_PDF, 15.96, 14.04, 12.0, id='bachelor63'),
    pytest.param(power.BACHELOR051_PDF, 15.96, 14.04, 12.0, id='bachelor51'),
])  # pylint:disable=C0103
@utilatest.skip_longrun
def test_doctextstyle_extract_headlines(source, h1, h2, h3):
    source = power.link(source)
    result = doctextstyle.extractor.extract(source)
    assert result
    assert result.h1_size == h1
    assert result.h2_size == h2
    assert result.h3_size == h3
