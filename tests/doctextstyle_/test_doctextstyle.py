# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila

import doctextstyle
import doctextstyle.extractor


def test_doctextstyle_extract():
    source = power.link(power.MASTER098_PDF)
    result = doctextstyle.extractor.extract(source)
    assert result

    assert result.text_size == 12.0
    assert result.pagenumber_size == 12.0
    assert result.footnote_size == 9.0
    assert result.footnote_distance == 10.3

    # justified text
    assert result.text_alignment == doctextstyle.JUSTIFIED


def test_regression_doctextstyle_homework25():
    source = power.link(power.HOMEWORK025_PDF)
    # shrink to content pages
    pages = utila.ranged_tuple(2, 22)
    result = doctextstyle.extractor.extract(source, pages=pages)
    assert result

    expected_size = [24.79, 17.22, 14.35]
    expected_before = [None, 46.8, 39.9]
    expected_after = [47.4, 30.9, 26.9]

    size = [result.h1_size, result.h2_size, result.h3_size]
    before = [result.h1_before, result.h2_before, result.h3_before]
    after = [result.h1_after, result.h2_after, result.h3_after]

    assert size == expected_size
    assert before == expected_before
    assert after == expected_after
