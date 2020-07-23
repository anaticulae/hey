# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest

import groupme.feature.footer
import groupme.footer


@pytest.mark.parametrize('path, expected_quality', [
    pytest.param(
        power.link(power.BACHELOR111_PDF),
        29,
        id='bachelor111',
    ),
    pytest.param(
        power.link(power.DOCU27_PDF),
        29,
        id='restruct',
    ),
])
def test_footer_judge_strategy_quality(path, expected_quality):
    """Ensure that enough header and footer are detected"""
    pages = tuple(range(0, 20))

    strategies = groupme.footer.strategies()
    results = [
        groupme.footer.strategy.create_strategy(
            path=path,
            strategy=strategy,
            pages=pages,
        ).result() for strategy in strategies
    ]
    result = groupme.feature.footer.judge_strategy(results)

    quality = sum([count(item.footer) + count(item.header) for item in result])
    assert quality == expected_quality, f'{quality} >= {expected_quality}'


def count(item):
    if item is not None:
        return 1
    return 0


def test_footer_judge_strategy_empty():
    empty = [
        [],
        [],
        [],
    ]
    result = groupme.feature.footer.judge_strategy(empty)
    assert result == []

    with pytest.raises(AssertionError):
        groupme.feature.footer.judge_strategy(None)
