# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import typing

TocLine = collections.namedtuple('TocLine', 'level, title, page, raw')


def remove_duplication(headlines: typing.List[TocLine]):
    """Remove duplications out of list of headlines."""
    result = []
    inserted = set()
    for item in headlines:
        if item.title in inserted:
            continue
        result.append(item)
        inserted.add(item.title)
    return result


def sort_byposition(lines: typing.List[TocLine], content: str):
    position = {}
    for item in lines:
        pos = content.find(item.title)
        position[pos] = item
    result = []
    for item in sorted(position):
        result.append(position[item])
    return result
