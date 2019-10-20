# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import groupme.footer
import tests.resources


@pytest.mark.parametrize('path, expected_quality', [
    pytest.param(
        tests.resources.BACHELOR_111PAGES,
        29,
        id='bachelor111',
        marks=pytest.mark.xfail(reason='decider strategy is not good enough'),
    ),
    pytest.param(
        tests.resources.RESTRUCT,
        29,
        id='restruct',
        marks=pytest.mark.xfail(reason='decider strategy is not good enough'),
    ),
])
def test_footer_judgement_strategy_quality(path, expected_quality):
    """Ensure that enough header and footer are detected"""
    pages = tuple(range(0, 20))

    results = [
        groupme.footer.create_strategy(
            path=path,
            strategy=strategy,
            pages=pages,
        ).result() for strategy in [
            groupme.footer.moving.MovingFooterStrategy,
            groupme.footer.fixed.FixedFooterStrategy,
            groupme.footer.pages.PageNumberStrategy,
        ]
    ]
    final = groupme.feature.footer.judge_strategy(results)

    quality = sum([count(item.footer) + count(item.header) for item in final])
    assert quality >= expected_quality, f'{quality} >= {expected_quality}'


def count(item):
    if item is not None:
        return 1
    return 0
