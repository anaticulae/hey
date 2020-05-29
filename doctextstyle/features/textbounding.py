# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import texmex
import utila


def text_width(cnavigators):
    result = widths(cnavigators)
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


def document_textfeed(navigators):
    try:
        left = texmex.document_textfeed(navigators)
    except IndexError:
        left = None  # TODO: REMOVE LATER
    try:
        right = texmex.document_textfeed(navigators, left=False)
    except IndexError:
        right = None  # TODO: REMOVE LATER
    return left, right
