# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import math

import iamraw
import utila


@dataclasses.dataclass
class MostBoundingDetected:
    left: float = None
    right: float = None
    top: float = None
    bottom: float = None
    confidence: float = 0.0


def run(sizeandborder: iamraw.PageSizeBorderList) -> MostBoundingDetected:
    borders = [item.border for item in sizeandborder]

    most = most_boundingbox(borders)
    # x0, y0, x1, y1
    # left right
    assert most[0] < most[1]
    # top bottom
    assert most[2] < most[3]

    assert most[0] < most[3]
    assert most[2] < most[1]

    result = MostBoundingDetected(
        left=most[0],
        right=most[1],
        top=most[2],
        bottom=most[3],
    )
    return result


def most_boundingbox(
        boxes: utila.Rectangles,
        roundme: bool = False,
) -> utila.Rectangle:
    """Extract bounding box of most common occurence for every side.

    Round detected boundingbox to full number to make approach more
    robust. Round numbers in direction to the border end to increase the
    detected rectangle that fit more items in it.
    """
    # TODO: Think about right and left, maybe search for the top 2 borders?
    # Filter None entries
    # left, right, top, bottom
    rounding = [math.floor, math.ceil, math.floor, math.ceil]
    result = []
    for index, method in enumerate(rounding):
        # remove None items
        filtered = [item[index] for item in boxes if item[index] is not None]
        # round to have a more robust grouping
        rounded = [method(item) for item in filtered] if roundme else filtered
        # determine most occured border to determine them as required border
        # support multiple border options.
        minimize = method is math.floor
        # TODO: REQUIRE A BETTER TY-BREAKER
        mode = utila.mode(rounded, minimize=minimize)
        result.append(mode)
    # (x0, y0, x1, y1)
    return tuple(result)
