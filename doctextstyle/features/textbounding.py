# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import utila

import doctextstyle


def text_width(cnavigators):
    result = widths(cnavigators)
    result = utila.roundme(result, digits=0, convert=False)  # pylint:disable=R0204
    return utila.mode(result)


def text_width_max(cnavigators):
    result = widths(cnavigators)
    if not result:
        return None
    return max(result)


def text_width_min(cnavigators):
    result = widths(cnavigators)
    if not result:
        return None
    return min(result)


def widths(cnavigators):
    result = []
    for content in cnavigators:
        for line in content:
            bounding = line.bounding
            diff = utila.roundme(bounding.x1 - bounding.x0)
            result.append(diff)
    return result


MIN_JUSTIFIED_LINES = configo.HV_PERCENT_PLUS(85).value


def justified(cnavigators, right_mode) -> int:
    if not cnavigators or right_mode is None:
        return None
    # TODO: REMOVE SHORT CENTERED LINES
    items = ([line.bounding.x1 for line in page] for page in cnavigators)
    items = utila.flatten(items)

    items = [item for item in items if item >= right_mode * 0.9]

    fit = right_mode - 5
    matched = [item for item in items if item >= fit]

    if not items:
        return None

    quote = len(matched) / len(items)
    if quote >= MIN_JUSTIFIED_LINES:
        return doctextstyle.JUSTIFIED
    return doctextstyle.NOT_JUSTIFIED
