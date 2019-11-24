# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import pytest

import groupme.toc.group as gtg
import tests.fixtures.headlines


@pytest.mark.xfail(reason='headline parsing does not work correctly')
def test_groupme_toc_group_group_master72():
    headlines = tests.fixtures.headlines.master72_headlines()
    expected = [3, 9, 11, 6, 1, 1, 1]

    grouped = gtg.group(headlines)
    assert len(grouped) == len(expected)

    count = [len(item) for item in grouped]
    for items in grouped:
        for item in items:
            print(item.title)
        print()
    assert count == expected


@pytest.mark.xfail(reason='headline parsing does not work correctly')
def test_groupme_toc_group_group_bachelor111():
    headlines = tests.fixtures.headlines.bachelor111_headlines()

    expected = [3, 16, 8, 5, 7, 8, 3, 1, 4, 1, 1, 1, 9]

    grouped = gtg.group(headlines)
    for item in grouped:
        print(item)
    assert len(grouped) == len(expected)
