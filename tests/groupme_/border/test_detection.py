# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import groupme.border.most


@pytest.mark.parametrize('roundme, expected', [
    (True, (50, 42, 544, 808)),
    (False, (50.4, 41.15, 544.88, 807.93)),
])
def test_border_most_boundingbox(roundme, expected):
    vim_diff_example = [
        (194.37, 72.0, 400.9, 648.34),
        (50.4, 40.18, 544.88, 700.13),
        (50.4, 40.18, 544.88, 700.78),
        (50.4, 41.15, 544.88, 807.93),
        (50.4, 41.15, 544.88, 807.93),
        (47.01, 41.15, 548.26, 807.93),
        (50.4, 41.15, 544.88, 807.93),
        (50.4, 41.15, 544.89, 807.93),
        (50.4, 41.15, 544.88, 807.93),
        (50.4, 41.15, 544.88, 807.93),
        (50.4, 41.15, 544.89, 807.93),
        (50.4, 41.15, 544.89, 807.93),
        (50.4, 41.15, 544.88, 807.93),
    ]
    result = groupme.border.most.most_boundingbox(
        vim_diff_example,
        roundme=roundme,
    )
    assert result == expected
