# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import groupme.toc.extractor as gte
import tests.fixtures.tableofcontent as tft


@pytest.mark.xfail(reason='headline parsing does not work correctly')
def test_groupme_toc_strategy_master72():
    headlines = tft.master72_toc()
    expected = [3, 9, 11, 6, 1, 1, 1]
    grouped = gte.extract(headlines)
    assert len(grouped) == len(expected)

    count = [len(item) for item in grouped]
    assert count == expected


@pytest.mark.xfail(reason='headline parsing does not work correctly')
def test_groupme_toc_strategy_bachelor111():
    headlines = tft.bachelor111_toc()

    expected = [3, 16, 8, 5, 7, 8, 3, 1, 4, 1, 1, 1, 9]

    grouped = gte.extract(headlines)
    assert len(grouped) == len(expected)


def test_groupme_toc_strategy_technial24():
    headlines = tft.technical24_toc()

    expected = [1, 1, 2, 7, 5, 1, 16, 1]

    grouped = gte.extract(headlines)
    assert len(grouped) == len(expected)
