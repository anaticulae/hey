# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Analyze content and structure of header area.

"""

import iamraw
import utila

import groupme.feature.numbers
import groupme.footer
import groupme.toc.regex


def parse(content: str):
    result = []

    strategies = [
        parse_rawtext,
        parse_title,
        parse_pagenumber,
    ]
    for bounds, text in content:
        parsed = None
        for strategy in strategies:
            parsed = strategy(text, bounds)
            if parsed:
                break
        if not parsed:
            parsed = iamraw.RawText(text=text)
        result.append(parsed)

    return result


def parse_rawtext(text: str, _):
    if text.count(utila.NEWLINE) <= 2:
        return None
    return iamraw.RawText(text=text)


def parse_pagenumber(text: str, _):
    text = text.strip()
    if not groupme.feature.numbers.is_pagenumber(text):
        return None
    return iamraw.PageInformation(value=text, raw=text)


def parse_title(text: str, _):
    parsed = groupme.toc.regex.parse(text)

    if not parsed:
        return None
    assert len(parsed) == 1, utila.log_raw(parsed)

    parsed = parsed[0]
    return iamraw.HeaderTitle(title=parsed.title, raw=parsed.raw)
