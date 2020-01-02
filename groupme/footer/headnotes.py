# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Analyze content and structure of header area.

"""

import iamraw
import utila

import groupme.feature.numbers
import groupme.toc.strategy.regex as gtsr


def parse(content: str):
    result = []

    strategies = [
        parse_rawtext,
        parse_title,
        parse_pagenumber,
    ]
    for item in content:
        parsed = None
        for strategy in strategies:
            parsed = strategy(item.text, item.bounding)
            if parsed:
                break
        if not parsed:
            parsed = iamraw.RawText(text=item.text)
        result.append(parsed)

    return result


def parse_rawtext(text: str, _=None):  # pylint:disable=W0613
    if text.count(utila.NEWLINE) <= 2:
        return None
    return iamraw.RawText(text=text)


def parse_pagenumber(text: str, _=None):  # pylint:disable=W0613
    text = text.strip()
    if not groupme.feature.numbers.is_pagenumber(text):
        return None
    return iamraw.PageInformation(value=text, raw=text)


def parse_title(text: str, _=None) -> iamraw.HeaderTitle:  # pylint:disable=W0613
    regex = parse_title_regex(text)
    if regex:
        return regex

    contemporary = parse_title_contemporary(text)
    if contemporary:
        return contemporary
    return None


def parse_title_regex(text: str) -> iamraw.HeaderTitle:
    parsed = gtsr.parse(text)

    if not parsed:
        return None
    assert len(parsed) == 1, utila.log_raw(parsed)

    parsed = parsed[0]
    return iamraw.HeaderTitle(title=parsed.title, raw=parsed.raw)


def parse_title_contemporary(text: str) -> iamraw.HeaderTitle:
    """Analyze `text` based on a contemporary(`TITLES`) lookup"""
    raw = text
    text = text.strip()
    text = text.title()
    if text not in TITLES:
        return None
    return iamraw.HeaderTitle(title=text, raw=raw)


TITLES = set([
    'Aufbau und Gliederung',
    'Aufbau',
    'Inhaltsverzeichnis',
    'Motivation und Zielsetzung',
    'Zusammenfassung',
])
