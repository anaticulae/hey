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
import utila
from iamraw import BoundingBox

import hey.textnavigator.navigator as htn
import tests.fixtures.headlines
import tests.resources
from hey.textnavigator.merger import merge_content
from hey.textnavigator.merger import merge_content_join
from hey.textnavigator.navigator import PageTextNavigator
from hey.textnavigator.navigator import navigator_to_bounds
from hey.textnavigator.navigator import percent_to_pagesize
from hey.textnavigator.navigator import to_content
#pylint:disable=W0611
from tests.fixtures.simple import simple_document
from tests.fixtures.simple import simple_pagetextnavigators
from tests.fixtures.simple import simple_second_page_navigator
from tests.groupme_ import navigator  # pylint:disable=W0611


def test_insert_order(navigator: PageTextNavigator):  #pylint:disable=W0621
    for before, after in zip(navigator[:-1], navigator[1:]):
        before = before.bounding
        after = after.bounding
        assert before.y0 <= after.y0
        if before.y0 == after.y0:
            assert before.x0 <= after.x0

    current_order = [item.text for item in navigator]

    # items are sorted in ascending
    assert current_order == list(range(len(navigator))), current_order


def test_after(navigator: PageTextNavigator):  #pylint:disable=W0621
    # Bottom footer
    after = 0.8  # from 80% to 100%
    # greater than 563
    # 1 item in this example
    result = navigator.after(after)
    assert len(result) == 4, result


def test_before(navigator: PageTextNavigator):  #pylint:disable=W0621
    # Top footer
    # smaller than 158.4
    before = 0.2  # from 20% to 0%
    # 2 items in this example
    result = navigator.before(before)
    assert len(result) == 1, before


@pytest.mark.parametrize('size,percent,expected', [
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


def test_hey_navigator_merge_content(simple_second_page_navigator):
    content = to_content(simple_second_page_navigator)
    merged, _ = merge_content(content)
    merged = merge_content_join(merged)

    paragraph_after_merge = 8

    content = to_content(simple_second_page_navigator)
    merged, _ = merge_content(content)  # split content and merge_ids
    merged_content = merge_content_join(merged)

    expectend_content = utila.NEWLINE.join([item.text for item in content])
    merged_content = utila.NEWLINE.join([item.text for item in merged_content])

    assert len(merged) == paragraph_after_merge

    assert merged_content == expectend_content
    content_count = len(expectend_content)
    merged_count = len(merged_content)
    # ensure that no data is lost while merging
    assert content_count == merged_count


def test_hey_navigator_create_pagetextcontent_navigator_frompath():
    loaded = htn.create_pagetextcontentnavigators_frompath(
        tests.resources.BACHELOR111,
        pages=(1, 2, 3, 4),
        prefix='oneline',
    )
    first = loaded[0]
    lasttext = first[-1].text
    assert lasttext != 'i', lasttext


def test_hey_navigator_find():
    navigator = htn.PageTextNavigator()
    location = iamraw.BoundingBox.from_str('10.0 12.0 15 20')
    navigator.insert('me', bounding=location, style=None)
    location = iamraw.BoundingBox.from_str('100.0 120.0 150 200')
    navigator.insert('hello', bounding=location, style=None)

    located = navigator.find(location)
    assert located.text == 'hello'
