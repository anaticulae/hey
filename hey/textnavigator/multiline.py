# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
r"""Multiline
    ---------

    This module aims to group/collect text depending on size and style
    into greater chunks. The first use case is to support multiple line
    headlines.

    .. code-block :: none

        font-size
        font-distance: y1[next] - y1[current]
        text-feed

    Remove high notes before starting analysis.
"""
import dataclasses
import math
import typing

import utila

import hey.textnavigator.navigator as htn
import hey.textnavigator.style as hts


@dataclasses.dataclass
class PageContentMultiLine:
    page: int = None
    content: list = dataclasses.field(default_factory=list)

    def __getitem__(self, index):
        return self.content[index]  # pylint:disable=E1136

    def __len__(self):
        return len(self.content)


PageContentMultiLines = typing.List[PageContentMultiLine]


@dataclasses.dataclass
class MultilineGroup():
    text: list = dataclasses.field(default_factory=list)
    size: float = None

    def append(self, item):
        self.text.append(item)

    def __getitem__(self, index):
        return self.text[index]  # pylint:disable=E1136

    def __len__(self):
        return len(self.text)


def group_pages_by_fontsize(
        pagetextnavigators: htn.PageTextNavigators,
        sizediff: float = 0.0,
) -> PageContentMultiLines:
    assert sizediff >= 0.0
    result = [
        group_page_by_fontsize(page, sizediff=sizediff)
        for page in pagetextnavigators
    ]
    return result


def group_page_by_fontsize(
        pagetextnavigator: htn.PageTextNavigator,
        sizediff: float = 0.0,
) -> PageContentMultiLine:
    """Group text lines by `sizediff`.

    Args:
        pagetextnavigator(content): content of page to group
        sizediff(float): maximal font size difference between 2 text lines
    Returns:
        grouped `PageContentMultiLine`
    """
    assert sizediff >= 0.0
    current = []
    style, size = None, None
    for item in pagetextnavigator:
        line = hts.style_without_highnotes(item, merge=True)
        style = line.content[0]  # pylint:disable=E1136
        currentsize = style.size
        if size is None:
            size = currentsize
            current.append(MultilineGroup(
                text=[item],
                size=size,
            ))
            continue
        if math.fabs(size - currentsize) > sizediff:
            size = currentsize
            current.append(MultilineGroup(
                text=[],
                size=size,
            ))
        current[-1].append(item)
    return PageContentMultiLine(
        page=pagetextnavigator.page,
        content=current,
    )


def linedistance(index, pagetextnavigator) -> float:
    current = pagetextnavigator[index]
    try:
        after = pagetextnavigator[index + 1]
    except IndexError:
        return None
    else:
        return utila.roundme(after.bounding.y1 - current.bounding.y1)


def linedistances(pagetextnavigator):
    return [
        linedistance(index, pagetextnavigator)
        for index in range(0, len(pagetextnavigator))
    ]


def group_linedistances(
        items: typing.List[float],
        maxdiff: float = 0.0,
) -> typing.List[int]:
    """Group items and return for every group with at least 2 members at
    list of indexes.

    Args:
        items: list of linedistances
        maxdiff(float): limit for gradient to be in same group
    Returns:
        list of list with indexs of grouped lines

    Content               linedistance
    Hallo - Headline      50

    Text                  10
    Text                  10
    Text                  30

    Pagenumber            None

    Prepare computing gradient: Duplicate first element and replace
    `None`-distance with distance before

                                    Gradient
                          50        0
    Hallo - Headline      50        -40

    Text                  10        0
    Text                  10        0
    Text                  30        20

    Pagenumber            30        0

    TODO: Extend documentation

    """
    assert items
    items = items[:]
    items = [items[0]] + items[:-1] + [items[-2]]
    # remove last None distance
    # items = items + [0]
    grad = [(after - current) for current, after in zip(items[0:-1], items[1:])]

    result = []
    current = []
    for index, diff in enumerate(grad, start=0):
        diff = diff if math.fabs(diff) > maxdiff else 0
        if diff == 0:
            current.append(index)
        # TODO: THINK ABOUT DIFF<0 and DIFF>0
        if diff < 0.0:
            if current:
                result.append(current)
            current = [index]
        if diff > 0.0:
            current.append(index)
            result.append(current)
            current = []
    if current:
        result.append(current)

    return result


# NOTE: Statistical approach for group_linedistances, think about later
# grouped = []
# current = [(0, items[0])]
# for index, item in enumerate(items[1:-1], start=1):
#     mean = statistics.mean([var[1] for var in current])
#     if item is not None:
#         diff = math.fabs(item - mean)
#     else:
#         # last item has no text distance
#         diff = 0.0
#     if diff > maxdiff:
#         grouped.append(current)
#         current = []
#     current.append((index, item))
# if current:
#     grouped.append(current)
# print(grouped)
# # cluster requires at least two items
# grouped = [item for item in grouped if len(item) >= 1]
# print(grouped)
# # filter index
# grouped = [[index for index, _ in group] for group in grouped]
# print(grouped)
# return grouped


def unite_groups(content, indexs):
    # TODO: MOVE TO MORE GENERAL PLACE
    # TODO: DIRTY CODE :|
    result = []
    for items in indexs:
        current = content[0]
        if len(current) == len(items):
            result.append(current)
            content = content[1:]
        elif len(current) > len(items):
            result.append(current[:len(items)])
            content[0] = current[len(items):]
            if not content[0]:
                content = content[1:]
        else:
            removecount = len(items)
            removecount = removecount - len(current)
            content = content[1:]
            while removecount:
                current = content[0]
                removecount = removecount - len(current)
                if removecount:
                    content = content[1:]
                else:
                    content[0] = current[len(current):]
                    if not content[0]:
                        content = content[1:]
    return result
