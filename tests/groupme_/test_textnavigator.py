# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from iamraw import BoundingBox
from pytest import fixture

from groupme.textnavigator import PageTextNavigator

SAMPLE = [
    (0, BoundingBox.from_str("130.91 668.55 540.00 704.02")),
    (2, BoundingBox.from_str("358.45 605.24 480.47 625.77")),
    (1, BoundingBox.from_str("467.46 650.40 540.00 667.51")),
    (4, BoundingBox.from_str("409.67 513.88 540.01 558.02")),
    (5, BoundingBox.from_str("550.0 513.88 600.0 558.02")),
    (3, BoundingBox.from_str("304.91 587.31 534.01 607.84")),
    (6, BoundingBox.from_str("77.38 216.25 121.22 230.47")),
    (8, BoundingBox.from_str("303.26 40.18 308.74 54.44")),
    (7, BoundingBox.from_str("77.38 102.67 534.62 206.45")),
]


@fixture
def navigator():
    navigator = PageTextNavigator()

    for item, position in SAMPLE:
        navigator.insert(position, item)
    assert len(navigator) == len(SAMPLE)
    return navigator


def test_insert_order(navigator):
    for index in range(len(navigator) - 1):
        before, _ = navigator[index]
        after, _ = navigator[index + 1]

        assert before.y_top >= after.y_top
        if before.y_top == after.y_top:
            assert before.x_bottom <= after.x_bottom

    current_order = [item for pos, item in navigator]

    # items are sorted in ascending
    assert current_order == list(range(len(navigator))), current_order


def test_after(navigator):
    # Bottom footer
    after = 0.8  # from 80% to 100%
    # smaller than 158.4
    # 1 item in this example
    result = navigator.after(after)
    assert len(result) == 1, result


def test_before(navigator):
    # Top footer
    before = 0.2  # from 20% to 0%
    # greater than 633.6
    # 2 items in this example
    result = navigator.before(before)
    assert len(result) == 2, before
