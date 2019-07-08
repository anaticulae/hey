# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from statistics import mode
from typing import List

from iamraw import Border

BorderList = List[Border]


def document_border(contentborders: BorderList) -> Border:
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

    left, bottom, right, top = mode(left), mode(bottom), mode(right), mode(top)

    return Border(left=left, bottom=bottom, right=right, top=top)
