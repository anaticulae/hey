# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Store experimental code here"""

import math


def lengths(first, second) -> float:
    # TODO: MOVE TO UTILA
    assert len(first) == len(second)
    summed = 0
    for left, right in zip(first, second):
        summed += pow(left - right, 2)
    return math.sqrt(summed)


def not_none(items):
    return [item for item in items if item is not None]
