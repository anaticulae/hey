# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import typing
from statistics import mode

from iamraw import Border

BorderList = typing.List[typing.Tuple[Border, int]]


def document_border(
        contentborders: BorderList,
        selector=[mode, mode, mode, mode],
) -> Border:
    """Extract all content border for every page and determine the most common
    border. Every direction is analyzed separatly.

    Args:
        contentborders(BorderList):
    Returns:
        most common border
    """
    # TODO: Move this code
    # TODO: Change!
    # 'left bottom right top'
    left, bottom, right, top = [], [], [], []

    # TODO: Check the positions
    for item in contentborders:
        left.append(item.left)
        bottom.append(item.bottom)
        right.append(item.right)
        top.append(item.top)

    left, bottom, right, top = [
        operator(data)
        for operator, data in zip(selector, [left, bottom, right, top])
    ]

    return Border(left=left, bottom=bottom, right=right, top=top)


def document_border_max(contentborders: BorderList):
    selector = [min, max, max, min]
    process = functools.partial(document_border, selector=selector)

    result = process(contentborders)
    return result
