# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import contextlib

import iamraw
import utila

import hey.textnavigator.navigator as htn


def count_textlines(page: iamraw.Page, remove_empty=False) -> int:
    """Iterate over `page`-content and extract textlines. If
    `remove_empty` is True, all lines which contain nothing or spaces
    will be ignored.

    Args:
        page(Page):
        remove_empty(bool):
    Returns:
        count of text lines on single page
    """
    # TODO: MOVE TO IAMRAW PACKAGE
    content = []
    if htn.isnavigator(page):
        return len([item for item in page if item.text.strip()])

    for item in page:
        with contextlib.suppress(AttributeError):
            content.extend([item.text for item in item.lines])

    if remove_empty:
        content = [item for item in content if item.strip()]
    return len(content)


def percent(value):
    assert value >= 0.0, str(value)
    return value * 0.01


def between(bounding, ymin, ymax):
    top = ymin <= bounding.y0 <= ymax
    bottom = ymin <= bounding.y1 <= ymax
    return top and bottom


def split(items, key=None):
    # assert isinstance(key, callable), 'require callable'
    matched = []
    not_matched = []
    if key is None:
        return items[:]
    for item in items:
        if key(item):
            matched.append(item)
        else:
            not_matched.append(item)

    return matched, not_matched


def validate(items: list):
    """Validate list of pageable items. If some `page` attribute is
    duplicated, raise ValueError.

    Args:
        items(list): list of objects with <page,content>
    Raises:
        ValueError: if some page attribute is duplicated.
    """
    # TODO: REMOVE AFTER UPGRADING IAMRAW
    counter = collections.Counter()
    for item in items:
        counter[item.page] += 1
    msg = []
    for page, value in counter.most_common():
        if value <= 1:
            continue
        msg.append(f'duplicated page: {page} ({value})')
    if msg:
        raise ValueError(utila.NEWLINE.join(msg))
