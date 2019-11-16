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


def group_pages(
        pagetextnavigators: htn.PageTextNavigators,
        sizediff: float = 0.0,
) -> PageContentMultiLines:
    assert sizediff >= 0.0
    result = [
        group_page(page, sizediff=sizediff) for page in pagetextnavigators
    ]
    return result


def group_page(
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
