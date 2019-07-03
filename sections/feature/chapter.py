# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Find the starts of a chapter.

What is typical for a start of chapter?

* Mostly there is a space between header and title start
* There is a number/chapter number
* There is a huge font
* The title is listed in table of content


1. Locate the distance between first line and header
2. Check the second line

"""

from re import X as VERBOSE
from re import search
from typing import List

from serializeraw import load_document
from serializeraw import load_toc
from utila import NEWLINE
from utila import from_raw_or_path
from yaml import FullLoader
from yaml import dump
from yaml import load

from groupme.feature.numbers import load_textposition
from hey.textnavigator.navigator import PageTextNavigator
from hey.textnavigator.navigator import create_pagetextnavigators


def work(document: str, position: str, tocpath: str) -> str:
    # load
    document = load_document(document)
    position = load_textposition(position)
    tocs = load_toc(tocpath)

    # TODO: Think about how to handle this, invocation order of features?
    navigators = create_pagetextnavigators(position, document)

    # work
    result = space_between_header_and_first_line(
        navigators=navigators,
        tocs=tocs,
    )
    dumped = dump_chapter_detection(result)
    return dumped


FIRST_QUARTER = 0.35


def space_between_header_and_first_line(
        navigators: List[PageTextNavigator],
        tocs,
):
    result = []
    for navigator in navigators:
        first_content = navigator.before(FIRST_QUARTER)

        chapter_rate = contain_chapter(first_content)
        chapter_rate += contain_toc(first_content, tocs)
        result.append(chapter_rate)
        # TODO: There is the possiblity that header and start of chapter
        # are together, support later
        # result.append(0.0)

    return result


NUMBER_PATTERN = r'\s[0-9]{1,2}\.?\s'


def contain_chapter(content):
    result = 0.0
    raw_content = NEWLINE.join([item for _, item in content])
    raw_content = raw_content.lower()

    if 'kapitel' in raw_content or 'chapter' in raw_content:
        result += 1.0
    # Search a number with possible dot
    if search(NUMBER_PATTERN, raw_content, flags=VERBOSE):
        result += 0.5
    else:
        result -= 0.5
    return result


def contain_toc(content, toc):
    flat_toc = [item.title for item in toc.children]

    flat_content = ' '.join([item for _, item in content])

    # is any toc title part of content
    if any(item in flat_content for item in flat_toc):
        return 1.0
    return -0.5


def chapter_value_to_percent(value: float):
    if value >= 2.5:
        return 1.0
    if value >= 1.0:
        return 0.25
    return 0.0


def dump_chapter_detection(pages: List[float]) -> str:
    result = []
    for index, chapter in enumerate(pages):
        result.append({
            'page': index,
            'chapter': '%.2f' % chapter,
        })
    return dump(result)


def load_chapter_detection(content: str) -> List[float]:
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)

    result = []
    for item in loaded:
        result.append(float(item['chapter']))
    return result
