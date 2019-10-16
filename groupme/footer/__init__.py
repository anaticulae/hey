# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import abc
import collections
import contextlib
import dataclasses
import enum
import functools
import statistics
import typing

import iamraw
import serializeraw
import utila
import yaml

import groupme
import hey
import hey.cluster
import hey.textnavigator.navigator

Header = float
Footer = float

Top = float
Bottom = float

PageContentFooterHeader = collections.namedtuple(
    'PageContentFooterHeader',
    'header, footer, page',
)


@dataclasses.dataclass
class HeaderInformation:
    begin: float
    end: float


@dataclasses.dataclass
class FooterInformation:
    begin: float
    end: float


class FooterType(enum.Enum):
    NONE = enum.auto()
    FIXED = enum.auto()
    VARIABLE = enum.auto()


class FooterHeaderDetectionStrategy(abc.ABC):
    """
    Relative or absolut result dimension?
    """

    def __init__(
            self,
            horizontals: iamraw.PagesWithHorizontalList,
            sizeandborders,
            pagenumbers,
            pagetextnavigators,
    ):
        assert isinstance(horizontals, typing.List), str(horizontals)
        self.horizontals = horizontals
        self.sizeandborders = sizeandborders
        self.pagenumbers = pagenumbers
        self.pagetextnavigators = pagetextnavigators

        self.result__ = {}

        self.post_init()

    def post_init(self):
        pass

    def result(self):
        raise NotImplementedError()

    def pageheight(self, page):
        selected = utila.select_page(self.sizeandborders, page)
        if selected is None:
            return None
        pageheight = selected.size.height
        return pageheight


def area(
        clusters: typing.List,
        ymin: float,
        ymax: float,
        max_groups: int = 1,
) -> int:
    bottom = area_likelihood(clusters, ymin, ymax)
    if not bottom:  # empty cluster
        return None

    if not any([item > 0.0 for item in bottom]):
        # no cluster item match area classificator
        return None

    index = bottom.index(max(bottom))
    _, (bounding, __) = clusters[index][0]

    return [bounding.y1]
    # return top or bottom? The element is a line, so it does not matter
    # return [item.y1 for item in bounding]  # y0?


EMPTY = (0, 0.0)


def area_likelihood(clusters, ymin, ymax):
    result = []
    for cluster in clusters:
        _, item = cluster[0]
        bounding, _ = item
        # assert that item is horizontal
        assert abs(bounding.y0 - bounding.y1) < 2.0, str(bounding)
        yvalue = bounding.y0
        if not (ymin <= yvalue <= ymax):
            result.append(EMPTY)
            continue

        result.append((
            len(cluster),
            1.0,  # TODO: need a better classificator
        ))
    uniformed = utila.uniform_result(result)
    return uniformed


def extract_own_footerheader(horizontals: iamraw.PagesWithHorizontalList):
    result = {}
    for content, page in horizontals:
        boxes = [item.box[1] for item in content]
        top = min(boxes, default=hey.textnavigator.navigator.START)
        bottom = max(boxes, default=hey.textnavigator.navigator.START)
        result[page] = (top, bottom)
    return result


def match_horizontals(
        content: iamraw.PageContentHorizontals,
        vertical_position: float,
):
    """Check if any horizontal match the `vertical_position`

    Args:
        todo(PageContentHorizontals): list with horizontal lines, mostly one page
        vertical_position(float): position on the page in 'pixel'
    Returns:
        True if any horizontal line match the `vertical_position`
    """
    vertical = utila.roundme(vertical_position)
    # TODO: Check y0/y1
    return any([utila.roundme(item.box.y0) == vertical for item in content])
