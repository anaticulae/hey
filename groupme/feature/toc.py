# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from typing import List

from iamraw import Document
from iamraw import Page
from iamraw import Section
from iamraw import create_toc
from serializeraw import dump_toc
from utila import NEWLINE

from groupme.feature import RawSection
from groupme.feature.structure import sections_from_page


def toc(document: Document):
    """
    # TODO: Include page distance!
    """
    result = []
    for page in document.pages:
        result.extend(toc_from_page(page))

    # Title must occurs double, first in the TOC and after this, following in
    # the text.
    hundert_percent_toc = filter_double(result)
    return hundert_percent_toc


def toc_to_yaml(tableofcontent):
    termal = []
    for level, title in tableofcontent:
        level = 1 + level.count('.')  # TODO: NOT VERY STABLE
        termal.append(Section(level=level, title=title))

    return dump_toc(create_toc(termal))


def toc_from_page(page: Page) -> List[RawSection]:
    """Extract headlines from page"""
    page_sections = sections_from_page(page)
    if not page_sections:
        raise ValueError('No sections in page: %s' % page)

    result = []
    # Filter non toc items, very simple rules!
    for index, item in enumerate(page_sections, start=0):
        if not item.title or not item.level:
            continue

        if item.title.count(NEWLINE) > 1:
            continue

        if item.title.count(' .') > 2 or item.title.count('...') > 2:
            result.append(index)
            continue

        # if len(item.title) > 120:
        #     continue

        result.append(index)
    if not result:
        # TODO: No data on page ?
        return []

    group = group_segmentation(result)
    longest = [page_sections[index] for index in longest_group(group)]

    filtered = [(item.level, strip_title(item.title)) for item in longest]

    return filtered


def group_segmentation(items, max_diff: int = 0):
    """A group is a list of items which stand direct together. A gab of
    max_diff is tollerated

    Example:
        5,6,7,             11,12,13,    19     max_diff 0  - 3 groups
        5,6,7,11,12,13,    19                  max_diff 4  - 2 groups
    """
    result = []
    collect = []
    last = 1000

    for item in items:
        diff = abs(last - item) - 1  # 6-5 = 1, 1 is no diff, it is next number
        if diff > max_diff:
            if collect:
                result.append(collect)
                collect = []
        last = item
        collect.append(item)
    if collect:
        result.append(collect)
    return result


def longest_group(groups):
    size = 0
    longest = None
    for group in groups:
        if len(group) > size:
            longest = group
            size = len(longest)
    return longest


def strip_title(title: str):
    """Remove ... in toc lines"""
    # split ...? .. ....
    return title.split(' .')[0]


def filter_double(items):
    """Return items which occurs twice"""
    result = []
    last = set()
    for item in items:
        before = len(last)
        last.add(item)
        if len(last) == before:
            result.append(item)
    return result
