# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import statistics
import typing

import iamraw

BorderList = typing.List[typing.Tuple[iamraw.Border, int]]


@dataclasses.dataclass
class Selector:

    left: callable = None
    right: callable = None
    top: callable = None
    bottom: callable = None


DEFAULT_SELECTOR = Selector(
    left=statistics.mode,
    right=statistics.mode,
    top=statistics.mode,
    bottom=statistics.mode,
)

BORDER_SELECTOR = Selector(left=min, right=max, top=min, bottom=max)


def document_border(
        contentborders: BorderList,
        selector: Selector = DEFAULT_SELECTOR,
) -> iamraw.Border:
    """Extract all content border for every page and determine the most
    common border. Every direction is analyzed separatly.

    Args:
        contentborders(BorderList): list of tuple of Border and page number
        selector: operators(callable) to judge result for border
                  direction. Use max, min, mode etc.
    Returns:
        most common border
    """
    # TODO: Move this code
    # TODO: Check the positions - pages?
    left = [item.left for item in contentborders]
    right = [item.right for item in contentborders]
    top = [item.top for item in contentborders]
    bottom = [item.bottom for item in contentborders]

    left = selector.left(left)
    right = selector.right(right)
    top = selector.top(top)
    bottom = selector.bottom(bottom)

    return iamraw.Border(left=left, bottom=bottom, right=right, top=top)


def document_border_max(contentborders: BorderList):
    result = document_border(contentborders, selector=BORDER_SELECTOR)
    return result
