# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import iamraw
import pytest

import hey.classificator


@pytest.mark.parametrize('min_elements, expected_groups', [
    (1, 3),
    (2, 1),
])
def test_cluster_common_items_2groups(min_elements, expected_groups):
    example = [
        [(iamraw.BoundingBox.from_list((1, 2, 3, 4)), '1')],
        [(iamraw.BoundingBox.from_list((1, 2, 3, 4)), '2')],
        [(iamraw.BoundingBox.from_list((1, 2, 3, 4)), '3')],
        [(iamraw.BoundingBox.from_list((1, 2, 3, 4)), '4')],
        [
            (iamraw.BoundingBox.from_list((100, 2, 120, 4)), '10'),
            (iamraw.BoundingBox.from_list((10, 2, 15, 4)), '2'),
        ],
    ]
    collected = hey.classificator.common_items(
        example,
        min_elements=min_elements,
    )
    assert len(collected) == expected_groups, collected
