# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hey.textnavigator.multiline as htm
import hey.textnavigator.navigator as htn
import tests.resources

NO_GROUP = [[18], [31], [29], [35]]  # number of items per page


def example():
    pages = tuple(range(5, 9))
    navigators = htn.create_pagetextnavigators_frompath(
        tests.resources.MASTER_72PAGES,
        pages=pages,
    )
    return navigators


@pytest.mark.xfail(reason='grouping is to soft')
def test_hey_textnavigator_multiline_group_page_no_group():
    navigators = example()
    grouped = htm.group_pages(navigators)
    count = [[len(item) for item in items] for items in grouped]
    assert count == NO_GROUP


def test_hey_textnavigator_multiline_group_page():
    navigators = example()
    grouped = htm.group_pages(navigators)
    count = [[len(item) for item in items] for items in grouped]
    expected = [
        [1, 16, 1],  # page 5, 3 MultilineGroups with `text` content
        [3, 7, 2, 13, 5, 1],
        [26, 2, 1],
        [30, 4, 1],  # page 8
    ]
    assert count == expected


def test_hey_textnavigator_multiline_group_page_by_maxdistance():
    navigators = example()
    grouped = htm.group_pages(navigators)
    count = [[len(item) for item in items] for items in grouped]
    expected = [
        [1, 16, 1],  # page 5, 3 MultilineGroups with `text` content
        [3, 7, 2, 13, 5, 1],
        [26, 2, 1],
        [30, 4, 1],  # page 8
    ]
    assert count == expected
