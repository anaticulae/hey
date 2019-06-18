# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from iamraw import BoundingBox
from pytest import mark

from groupme.textnavigator import PageTextNavigator
from groupme.textnavigator import percent_to_pagesize


def test_insert_order(navigator: PageTextNavigator):  #pylint:disable=W0621
    for index in range(len(navigator) - 1):
        before, _ = navigator[index]
        after, _ = navigator[index + 1]

        assert before.y_top >= after.y_top
        if before.y_top == after.y_top:
            assert before.x_bottom <= after.x_bottom

    current_order = [item for pos, item in navigator]

    # items are sorted in ascending
    assert current_order == list(range(len(navigator))), current_order


def test_after(navigator):  #pylint:disable=W0621
    # Bottom footer
    after = 0.8  # from 80% to 100%
    # smaller than 158.4
    # 1 item in this example
    result = navigator.after(after)
    assert len(result) == 1, result


def test_before(navigator):  #pylint:disable=W0621
    # Top footer
    before = 0.2  # from 20% to 0%
    # greater than 633.6
    # 2 items in this example
    result = navigator.before(before)
    assert len(result) == 2, before


@mark.parametrize('size,percent,expected', [
    (100.0, 1.0, 0),
    (100.0, 0.0, 100),
    (100.0, 0.75, 25),
])
def test_textnavigator_percent_to_page(size, percent, expected):
    result = percent_to_pagesize(
        size,
        percent,
    )
    assert result == expected


#pylint:disable=W0621
def test_fonts_navigator_to_bounds(navigator: PageTextNavigator):
    result = navigator_to_bounds(navigator)

    assert all([isinstance(item, BoundingBox) for item in result])
