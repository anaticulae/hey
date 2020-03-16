# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math
import typing

import utila
import utila.math

Rectangle = typing.Tuple[float, float, float, float]
Rectangles = typing.List[Rectangle]


def diff_mode(items: utila.Numbers, max_diff: float = 2.0) -> utila.Numbers:
    """Compute mode auf `item` and determine matched `items` which does
    not more differ than `max_diff` from mode.

    Args:
        items(Numbers): items to filter
        max_diff(float): max difference to mode which matches the classifier
    Returns:
        matched items
    """
    mode = utila.modes(items)
    matched = [item for item in items if math.fabs(item - mode) <= max_diff]
    return matched


def lookup(value: utila.math.Number, table: typing.List) -> utila.math.Number:
    """Use table lookup to determine holy value.

    Args:
        value: selector to determine holy value
        table: contains holy values to determine on given `value`.
    Returns:
        selected HolyValue.
    """
    # TODO: VERY SLOW
    # TODO: MOVE TO CONFIGO
    current, result = table[0]
    assert value >= current, f'value is to small {value} >= {current}'
    for count, returnvalue in table:
        if current <= value <= count:
            return returnvalue
        current, result = count, returnvalue
    return result


def diffs(items: utila.Numbers) -> utila.Numbers:
    assert len(items) >= 2, f'no enough items: {len(items)}'
    result = [
        math.fabs(first - second) for first, second in zip(
            items[1:],
            items[0:-1],
        )
    ]
    return result
