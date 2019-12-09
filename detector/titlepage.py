# C O P Y R I G H T
# =============================================================================
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw


def select_best(pages: typing.List[iamraw.TitlePage]) -> iamraw.TitlePage:
    result = pages[0]
    current = rate(result)
    for item in pages[1:]:
        rating = rate(item)
        if rating > current:
            current = rating
            result = item
    if current <= 0:
        # No valid title page detected
        return None
    return result


def rate(title: iamraw.TitlePage) -> int:
    result = 0
    if not title:
        return result
    if title.title:
        result += 5
    if title.thesis:
        result += 10
    if title.date:
        result += 10
    if title.institution:
        result += 20
    return result
