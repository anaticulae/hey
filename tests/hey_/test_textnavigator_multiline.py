# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

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


@pytest.mark.parametrize('page, expected', [
    (0, [
        [0],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        [17],
    ]),
    (1, [
        [0, 1, 2],
        [3, 4, 5, 6, 7, 8, 9],
        [10, 11],
        [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        [25, 26, 27, 28, 29],
        [30],
    ]),
    (2, [
        [0, 1],
        [2, 3, 4, 5],
        [6, 7, 8],
        [9, 10],
        [11, 12, 13],
        [14, 15, 16],
        [17, 18],
        [19, 20, 21],
        [22, 23, 24, 25],
        [26, 27],
        [28],
    ]),
    (
        3,
        [[
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
            19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29
        ], [30, 31, 32, 33], [34]],
    ),
])
def test_hey_textnavigator_multiline_group_linedistances_page(page, expected):
    navigators = example()
    content = navigators[page]
    distances = htm.linedistances(content)
    grouped = htm.group_linedistances(distances, maxdiff=1.0)
    assert grouped == expected
