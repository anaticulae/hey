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
import dataclasses
import enum
import typing

import iamraw
import utila

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
