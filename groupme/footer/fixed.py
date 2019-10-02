# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import utila

import groupme.footer
import hey.textnavigator.navigator


class FixedFooterStrategy(groupme.footer.FooterHeaderDetectionStrategy):

    def result(self):
        # determine border for all pages
        top, bottom = extract_common_footer(self.horizontals)

        # look for every page if footer/header are present
        extracted = extract_page_footerheader(
            self.horizontals,
            top,
            bottom,
        )
        return extracted


def extract_common_footer(horizontals: iamraw.PagesWithHorizontalList):
    with_box = [[(
        horizontal.box,
        horizontal,
    ) for horizontal in page.content] for page in horizontals]

    # cluster horizontal lines
    clusters = hey.cluster.common_items(with_box, max_difference=2.0)

    top = header(clusters)
    bottom = footer(clusters)
    if top is None:
        # could not detect any header
        top = hey.textnavigator.navigator.START
    if bottom is None:
        # could not detect any footer
        bottom = hey.textnavigator.navigator.END

    # the header is on the top(0.0) and the footer is on the bottom(1.0)
    assert top < bottom, '%.2f < %.2f' % (top, bottom)
    return top, bottom


def footer(clusters: typing.List) -> float:
    """Determine all elements in the potential footer area"""
    # TODO: remove holy value
    # TODO: Make dependent on page size
    result = groupme.footer.area(clusters, 700, 800, max_groups=1)
    if not result:
        return None
    return result[0]


def header(clusters: typing.List) -> float:
    """Determine all elements in the potential header area"""
    # TODO: Make dependent on page size
    result = groupme.footer.area(clusters, 0, 100, max_groups=1)
    if not result:
        return None
    return result[0]


def extract_page_footerheader(
        horizontals: iamraw.PagesWithHorizontalList,
        top: float,
        bottom: float,
) -> typing.List[groupme.footer.FooterBorder]:
    result = []
    for page in horizontals:
        topped = groupme.footer.match_horizontals(page, top)
        bottomed = groupme.footer.match_horizontals(page, bottom)

        top_ = utila.roundme(top * topped) if topped else None
        bottom_ = utila.roundme(bottom * bottomed) if bottomed else None

        footerandheader = groupme.footer.PageContentFooterHeader(
            content=(top_, bottom_),
            page=page.page,
        )
        result.append(footerandheader)
    return result
