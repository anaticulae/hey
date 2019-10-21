# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""The `footer` module extract the header and footer area out of
pdf-pages.
There are three different strategies:

- FixedFooterStrategy
- MovingFooterStrategy
- PageNumberStrategy

The strategy is to run these different strategies and use a
judgement-unit to decide which result is the best. In some cases the best
strategy changes from page to page.

As a result we have the `HeaderInformation` and `FooterInformation` with
additional data. As a further the **decider** program judges about
header and footer and gives advices to the user about failures and
possible improvements.
"""
import abc
import collections
import dataclasses
import os
import typing

import iamraw
import serializeraw
import utila

import hey.textnavigator.navigator


@dataclasses.dataclass  # pylint:disable=R0903
class FooterStrategyResultReport:
    pass


class FooterHeaderDetectionStrategy(abc.ABC):
    """
    Relative or absolute result dimension?
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
        """Run after __init__"""

    def result(self):
        raise NotImplementedError()

    def report(self) -> FooterStrategyResultReport:
        """Return meta data to determined `result`. The main propose of
        this report is to have a better view why the algorithm produces
        this given result."""
        raise NotImplementedError()

    def pageheight(self, page):
        """Determine `pageheight` of current `page` in `pixel`.

        Args:
            page(int): page of pdf document
        Returns:
            pageheight if pageheight exists
            None if pageheight not exists
        """
        selected = utila.select_page(self.sizeandborders, page)
        if selected is None:
            return None
        pageheight = selected.size.height
        return pageheight


def create_strategy(
        path: str,
        strategy: 'FooterHeaderDetectionStrategy-class',
        pages=None,
):
    horizontals = os.path.join(path, 'rawmaker__boxes_horizontal.yaml')
    horizontals = serializeraw.load_horizontals(horizontals, pages=pages)

    sizeandborders = os.path.join(path, 'rawmaker__border_pages.yaml')
    sizeandborders = serializeraw.load_pageborders(sizeandborders, pages=pages)

    pagenumbers = os.path.join(path, 'groupme__pagenumbers_pagenumbers.yaml')
    pagenumbers = serializeraw.load_pagenumbers(pagenumbers, pages=pages)

    navigator = hey.textnavigator.navigator.create_pagetextnavigators_frompath(
        path,
        pages=pages,
    )

    result = strategy(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        pagenumbers=pagenumbers,
        pagetextnavigators=navigator,
    )
    return result


def remove_duplication(items):
    """In some cases more than one potential header or footer are
    detected for one page. This method judges the problem and select the
    `best` result.

    Args:
        items: list of `PageContentFooterHeader`
    Returns:
        sorted list without page duplications
    """
    source = collections.defaultdict(list)
    for item in items:
        source[item.page].append(item)

    result = []
    for values in source.values():
        if len(values) == 1:
            result.append(values)
            continue
        result.append(multijudgement(values))

    result = sorted(result, key=lambda x: x.page)
    return result


def multijudgement(judges):
    # TODO: Strategy how to judge multiple matches
    # BIGGER ONE, ITEM OF BIGGER CLUSTER?

    def count_item(item):
        return int(item.footer is not None) + int(item.header is not None)

    current = judges[0]
    count = count_item(current)
    for item in judges[1:]:
        cur_count = count_item(item)
        if cur_count < count:
            continue
        current = item
        current = item
    return current
