# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""left right border detector
==========================

The `left right border detector` (lrbd) separates borders of the left
and right page especially which are used for books with different border
width for left and right page.

As a result of different left-right borders there are alternating border
widths which we detect. On single pages there are no alternating border.

Currently there are two strategies to detect different page border:

* simple approach
* raising edge

Simple Approach
~~~~~~~~~~~~~~~

Some documents have exceptions on some pages. We handle this via allowed
errors defined with the HolyValues `MAX_FIRSTSECOND_ERROR` and
`MIN_MIXED_ERROR`.

Raising Edge
~~~~~~~~~~~~

The change of the text feed creates an raising edge between pages. This
approach detects these edges to determine left and right page border
width.
"""

import dataclasses
import math
import statistics
import typing

import configo
import iamraw
import utila

# max diff to match in common group.
MAX_SIDE_DIFF = configo.HV_INT_PLUS(default=2.0)
# exceptions which are allowed cause of user defined error.
# TODO: REPLACE WITH HOLY VALUE CONFIGO APPROACH
MAX_FIRSTSECOND_ERROR = ((2, 0.5), (3, 0.35), (5, 0.26), (10, .21), (15, 0.05),
                         (200, 0.01))
# errors which are a result of handle alternating border as single border.
MIN_MIXED_ERROR = configo.HV_PERCENT_PLUS(default=15)
# area where left border can be located.
LEFT_PERCENT = configo.HV_PERCENT_PLUS(default=30)
# area where right border can be located.
RIGHT_PERCENT = configo.HV_PERCENT_PLUS(default=30)

MIN_RAISING_EDGE = configo.HV_PERCENT_PLUS(default=75)

# TODO: REPLACE WITH CONFIGO TABLE
RAISING_FAILRATE = (
    (5, 1 / 5),
    (7, 2 / 7),
    (10, 3 / 10),
    (40, 10 / 40),
    (200, 20 / 200),
)
# TODO: SHOULD WE DISABLE ALGO ON BIG FAIL COUNT?

LeftRight = typing.Tuple[float, float]

DetectedBorder = typing.TypeVar('DetectedBorder', typing.Tuple[float], float)


@dataclasses.dataclass
class LeftRightDetected:
    left: DetectedBorder = None
    right: DetectedBorder = None
    confidence: float = 0.0

    @property
    def valid(self):
        return isinstance(self.left, tuple)


def run(
        textpositions: iamraw.PageContentTextPositions,
        pagesizes: iamraw.PageSizeBorderList,
) -> LeftRightDetected:
    """Run LeftRight-Strategy to determine that document contains
    special leftright-border or a normal equal border for every page."""
    left, right = determine_pageborder(textpositions, pagesizes)
    left, right = handle_emptypage(left, right)

    result = simple(left, right)
    if result:
        return result

    result = raising(left, right)
    if result:
        return result

    leftborder = utila.mode(left, minimize=True)
    rightborder = utila.mode(right, minimize=False)
    return LeftRightDetected(
        left=leftborder,
        right=rightborder,
        confidence=1.0,
    )


def simple(left: utila.Numbers, right: utila.Numbers) -> LeftRightDetected:
    """Determine LeftRight border based on changing text feed. We use
    the even numbers to determine the left page and the odd numbers to
    determine the right text feed.

    This appraoch is limited when one page was missing and therefore
    these pages are mixed and therefore wrong classified.

    Args:
        left: ordered list of left text feed
        right: ending of right text content border
    Returns:
        None if no valid LeftRightDetected was detected
        LeftRightDetected if failrate is not to hight
    """
    if len(left) <= 1:
        # TODO: INVESTIGATE HERE
        utila.error('could not run simple approach')
        return None
    mixed = utila.diff_mode(left, max_diff=MAX_SIDE_DIFF.value)
    # first side
    first = left[::2]
    first_matched = utila.diff_mode(first, max_diff=MAX_SIDE_DIFF.value)
    # second side
    second = left[1::2]
    second_matched = utila.diff_mode(second, max_diff=MAX_SIDE_DIFF.value)

    mixed_error = 1 - len(mixed) / len(left)
    first_error = 1 - len(first_matched) / len(first)
    second_error = 1 - len(second_matched) / len(second)

    utila.debug(f'mixed: {mixed_error}')
    utila.debug(f'first: {first_error}')
    utila.debug(f'second: {second_error}')

    # left right
    # TODO: DEFINE BETTER CONFIDENCE APPROACH
    max_firstsecond_error = utila.lookup(
        len(first),
        MAX_FIRSTSECOND_ERROR,
    )
    if mixed_error > MIN_MIXED_ERROR.value and all([
            first_error < max_firstsecond_error,
            second_error < max_firstsecond_error,
    ]):
        leftborder = (
            utila.mode(first, minimize=True),
            utila.mode(second, minimize=True),
        )
        rightborder = (
            utila.mode(right[::2]),
            utila.mode(right[1::2]),
        )
        return LeftRightDetected(
            left=leftborder,
            right=rightborder,
            confidence=1.0,
        )
    return None


def raising(left: utila.Numbers, right: utila.Numbers) -> LeftRightDetected:
    """Determine border depending on changing text feed on left page
    border.

    This approach has no problems when one or more leftright pages are
    missing. The limit of problems is defined in lookup table
    `RAISING_FAILRATE`.

    Args:
        left: ordered list of left text feed
        right: ending of right text content border
    Returns:
        None if no valid LeftRightDetected was detected
        LeftRightDetected if `failrate` is not too high
    """
    longest_left = longest_two(left)
    longest_right = longest_two(right)

    if longest_left is None or longest_right is None:
        # single page document which does not contain left-right-pages
        return None

    first_left = statistics.mean(longest_left[0])
    second_left = statistics.mean(longest_left[1])
    edge = math.fabs(first_left - second_left)

    first_right = statistics.mean(longest_right[0])
    second_right = statistics.mean(longest_right[1])

    edges = utila.diffs(left)
    failures = [
        index for index, item in enumerate(edges)
        if item < edge * MIN_RAISING_EDGE.value
    ]
    failrate = len(failures) / len(edges)
    max_failrate = utila.lookup(
        len(edges),
        RAISING_FAILRATE,
        right_outranges_none=False,
    )

    if failrate > max_failrate:
        return None

    first_left, second_left = utila.roundme(first_left, second_left)
    first_right, second_right = utila.roundme(first_right, second_right)

    leftborder = (
        min([first_left, second_left]),
        max([first_left, second_left]),
    )
    rightborder = (
        min([first_right, second_right]),
        max([first_right, second_right]),
    )

    return LeftRightDetected(
        left=leftborder,
        right=rightborder,
        confidence=1.0,
    )


def handle_emptypage(left, right):
    # TODO: THINK ABOUT IF THIS IS ENOUGH
    # ignore empty pages
    left_none = 0.0
    left = [item if item is not None else left_none for item in left]

    right_none = max([item for item in right if item is not None])
    # NOTE: Determine more pages as large than it realy are - is this a
    # problem?
    right = [item if item is not None else right_none for item in right]

    return left, right


def determine_pageborder(textpositions, pagesizes):
    left = []
    right = []
    before = -1
    for current, (page, size) in utila.sync_pages([textpositions, pagesizes]):
        assert current > before, f'{before} < {current}'
        before = current
        if not page or not size:
            left.append(None)
            right.append(None)
            continue
        bounding = [item for item, _ in page.content.values()]
        leftright = maximize_leftright(bounding, size)
        left.append(leftright[0])
        right.append(leftright[1])
    return left, right


def maximize_leftright(
        boundings: utila.Rectangles,
        size: iamraw.PageSizeBorder,
) -> LeftRight:
    """Determine the left and right border of a page based on `mode`
    selection in `size`.

    Minimize the left and maximize the right position. The area where
    mode is used to determine the most common border which is assumed as
    correct border is limit by `size` configuration.

    Args:
        boundings: textpositions of defined page
        size: width and height of current page
    Returns:
        tuple with left and right content bounding
    """
    left_max = size.size.width * LEFT_PERCENT.value
    right_min = size.size.width * (1 - RIGHT_PERCENT.value)
    left_max, right_min = utila.roundme(left_max, right_min)
    assert left_max <= right_min, 'left and right bounds are flipped'

    left = [item[0] for item in boundings if item[0] <= left_max]
    right = [item[2] for item in boundings if item[2] >= right_min]

    # TODO: DO WE RELAY NEED THIS?
    if not left:
        left = 0.0
    else:
        left = utila.mode(left, minimize=True)
    if not right:
        right = size.size.width
    else:
        right = utila.mode(right, minimize=False)
    return left, right


def longest_two(items: utila.Numbers) -> typing.Tuple[float, float]:

    def close(candidat, clusteritem):
        # TODO: HOLY VALUE
        return math.fabs(candidat - clusteritem) < 2.0

    clustered = utila.determine_cluster(items, close)
    result = sorted(clustered, key=len, reverse=True)
    if len(result) < 2:
        return None
    return result[0], result[1]
