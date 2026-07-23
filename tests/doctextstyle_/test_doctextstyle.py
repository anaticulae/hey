# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import utilo
import utilotest

import doctextstyle
import doctextstyle.extractor
import doctextstyle.vector


@utilotest.nightly
@pytest.mark.parametrize('method', [
    pytest.param(
        doctextstyle.vector.run,
        id='ki_magic',
        marks=pytest.mark.xfail(reason='incomplete implementation'),
    ),
    pytest.param(doctextstyle.extractor.extract, id='old_school'),
])
def test_doctextstyle_extract(method):
    utilotest.fixture_requires(hoverpower.MASTER098_PDF)
    source = hoverpower.link(hoverpower.MASTER098_PDF)
    result = method(source)
    assert result

    assert result.text_size == 12.0
    assert result.pagenumber_size == 12.0
    assert result.footnote_size == 9.0
    assert result.footnote_distance == 10.3
    # justified text
    assert result.text_alignment == doctextstyle.JUSTIFIED


@pytest.mark.parametrize('method', [
    pytest.param(doctextstyle.vector.run, id='ki_magic'),
    pytest.param(doctextstyle.extractor.extract, id='old_school'),
])
def test_regression_doctextstyle_homework25(method):
    utilotest.fixture_requires(hoverpower.HOME025_PDF)
    source = hoverpower.link(hoverpower.HOME025_PDF)
    # shrink to content pages
    pages = utilo.rtuple(1, 22)
    result = method(source, pages=pages)
    assert result
    # expected
    expected_size = [24.79, 17.22, 14.35]
    expected_before = [None, 46.8, 39.9]
    expected_after = [47.4, 30.9, 26.9]
    size = [result.h1_size, result.h2_size, result.h3_size]
    before = [result.h1_before, result.h2_before, result.h3_before]
    after = [result.h1_after, result.h2_after, result.h3_after]
    # verify
    assert utilo.nears(size, expected_size, diff=0.5)
    assert utilo.nears(before, expected_before, diff=0.5, none=True)
    assert utilo.nears(after, expected_after, diff=0.5, none=True)


@utilotest.nightly
@utilotest.requires(hoverpower.MASTER116_PDF)
def test_regression_doctextstyle_master116():
    source = hoverpower.link(hoverpower.MASTER116_PDF)
    result = doctextstyle.extractor.extract(source)
    # justified text
    assert result.text_alignment == doctextstyle.JUSTIFIED
