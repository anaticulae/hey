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
import random


def choose_random(items, count: int = 5) -> list:
    """Chose `count` random items of a collection

    Hint:
        This process does not change the source collection. There are no side
        effects.
    Args:
        items(list): data collection to select random items
        count(int): number of items to retun
    Returns:
        `count` selected items out of collections
      """
    items = list(items)  # create a copy
    random.shuffle(items)
    return items[0:count]


def lengths(first, second) -> float:
    # TODO: MOVE TO UTILA
    assert len(first) == len(second)
    summed = 0
    for left, right in zip(first, second):
        summed += pow(left - right, 2)
    return math.sqrt(summed)


def not_none(items):
    return [item for item in items if item is not None]
