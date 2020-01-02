# C O P Y R I G H T
# =============================================================================
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw

import detector.parser.complete

MIN_TITLEPAGE_RATING = 20  # TODO: HOLY VALUE


def select_best(pages: typing.List[iamraw.TitlePage]) -> iamraw.TitlePage:
    pages = [
        item for item in pages if detector.parser.complete.valid_titlepage(item)
    ]
    if not pages:
        # no valid page
        return None
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
    if current <= MIN_TITLEPAGE_RATING:
        # rating is to low
        # TODO: Handle different than no detection
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
