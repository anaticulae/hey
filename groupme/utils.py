# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import iamraw


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
