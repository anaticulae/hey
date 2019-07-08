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

from hey.textnavigator.navigator import PageTextNavigator
from hey.textnavigator.navigator import merge_content
from hey.textnavigator.navigator import navigator_to_bounds
from hey.textnavigator.navigator import percent_to_pagesize
from hey.textnavigator.navigator import to_content
#pylint:disable=W0611
from tests.fixtures.simple import simple_document
from tests.fixtures.simple import simple_pagetextnavigators
from tests.fixtures.simple import simple_second_page_navigator
from tests.groupme_ import navigator  # pylint:disable=W0611


def test_insert_order(navigator: PageTextNavigator):  #pylint:disable=W0621
    for (before, _), (after, _) in zip(navigator[:-1], navigator[1:]):
        assert before.y0 <= after.y0
        if before.y0 == after.y0:
            assert before.x0 <= after.x0

    current_order = [item for pos, item in navigator]

    # items are sorted in ascending
    assert current_order == list(range(len(navigator))), current_order


def test_after(navigator: PageTextNavigator):  #pylint:disable=W0621
    # Bottom footer
    after = 0.8  # from 80% to 100%
    # greater than 633.6
    # 1 item in this example
    result = navigator.after(after)
    assert len(result) == 2, result


def test_before(navigator: PageTextNavigator):  #pylint:disable=W0621
    # Top footer
    # smaller than 158.4
    before = 0.2  # from 20% to 0%
    # 2 items in this example
    result = navigator.before(before)
    assert len(result) == 1, before


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


def test_groupme_navigator_merge_content(simple_second_page_navigator):
    content = to_content(simple_second_page_navigator)

    paragraph_after_merge = 8

    merged = merge_content(content)
    assert len(merged) == paragraph_after_merge
