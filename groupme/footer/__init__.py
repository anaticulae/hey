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
jugement-unit to decide which result is the best. In some cases the best
strategy changes from page to page.

As a result we have the `HeaderInformation` and `FooterInformation` with
additional data. As a further the **decider** program judges about
header anf footer and gives adives to the user about failures and
possible improvements.
"""
import abc
import collections
import dataclasses
import enum
import typing

import iamraw
import utila

PageContentFooterHeader = collections.namedtuple(
    'PageContentFooterHeader',
    'header, footer, page',
)


@dataclasses.dataclass  # pylint:disable=R0903
class PageInformation:
    value: str = None
    raw: str = None


@dataclasses.dataclass  # pylint:disable=R0903
class HeaderInformation:
    begin: float
    end: float
    page: PageInformation = None


@dataclasses.dataclass  # pylint:disable=R0903
class FooterInformation:
    begin: float
    end: float
    page: PageInformation = None


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
        """Run after __init__"""

    def result(self):
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
