# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Example:
    docu/restructuredtext.pdf

Master of the art:
    docu/vimguide.pdf: This example contains a lot of tables, therefore
                       we have a lot of horizontal lines which challenges
                       the algorithm.
"""
import dataclasses
import typing

import iamraw
import utila

import groupme.footer
import groupme.utils
import hey.textnavigator.navigator


class FixedFooterStrategy(groupme.footer.FooterHeaderDetectionStrategy):

    def result(self):
        # TODO: HOW TO HANDLE DIFFERENT PAGE HEIGHTS
        # pageheight = utila.select_page(self.sizeandborders, 0)[0][1]
        pageheight = self.pageheight(0)
        # determine border for all pages
        top, bottom = extract_common_footer(self.horizontals, pageheight)

        # look for every page if footer/header are present
        extracted = extract_page_footerheader(
            self.horizontals,
            top,
            bottom,
            pageheight,
        )
        return extracted


@dataclasses.dataclass
class FixedFooterInformation(groupme.footer.FooterInformation):
    pass


@dataclasses.dataclass
class FixedHeaderInformation(groupme.footer.HeaderInformation):
    pass


def extract_common_footer(
        horizontals: iamraw.PagesWithHorizontalList,
        pageheight: int,
):
    with_box = [[(
        horizontal.box,
        horizontal,
    ) for horizontal in page.content] for page in horizontals]

    # cluster horizontal lines
    clusters = hey.cluster.common_items(with_box, max_difference=2.0)

    top = extract_header(clusters, pageheight)
    bottom = extract_footer(clusters, pageheight)
    if top is None:
        # could not detect any header
        top = hey.textnavigator.navigator.START
    # else:
    #     top = top / pageheight
    if bottom is None:
        # could not detect any footer
        bottom = pageheight
        # bottom = hey.textnavigator.navigator.END
    else:
        pass
        # bottom = bottom / pageheight
    # the header is on the top(0.0) and the footer is on the bottom(1.0)
    assert top < bottom, '%.2f < %.2f' % (top, bottom)

    return top, bottom


HEADER_MAX_SIZE = groupme.utils.percent(15)
FOOTER_MAX_SIZE = groupme.utils.percent(20)  # percent # TODO: HOLY VALUE


def extract_footer(
        clusters: typing.List,
        pageheight: int,
) -> float:
    """Determine all elements in the potential footer area"""
    # TODO: remove holy value
    # TODO: Make dependent on page size
    assert 0 <= FOOTER_MAX_SIZE <= 1, f'FOOTER_MAX_SIZE: {FOOTER_MAX_SIZE}'

    top_footer_border = pageheight * (1 - FOOTER_MAX_SIZE)
    bottom_footer_border = pageheight

    result = groupme.footer.area(
        clusters,
        top_footer_border,
        bottom_footer_border,
        max_groups=1,
    )
    if not result:
        return None
    return result[0]


def extract_header(
        clusters: typing.List,
        pageheight: int,
) -> float:
    """Determine all elements in the potential header area"""
    # TODO: HOLY VALUE Make dependent on page size
    assert 0 <= HEADER_MAX_SIZE <= 1, f'HEADER_MAX_SIZE: {HEADER_MAX_SIZE}'
    bottom_header_border = pageheight * HEADER_MAX_SIZE
    result = groupme.footer.area(
        clusters,
        0,
        bottom_header_border,
        max_groups=1,
    )
    if not result:
        return None
    return result[0]


def extract_page_footerheader(
        horizontals: iamraw.PagesWithHorizontalList,
        top: float,
        bottom: float,
        pageheight: float,
) -> typing.List[groupme.footer.PageContentFooterHeader]:
    result = {}
    for page in horizontals:
        top_match = groupme.footer.match_horizontals(page.content, top)
        bottom_match = groupme.footer.match_horizontals(page.content, bottom)

        header = None
        if top_match:
            top_ = utila.roundme(top / pageheight)
            header = FixedHeaderInformation(
                begin=hey.textnavigator.navigator.START,
                end=top_,
            )

        footer = None
        if bottom_match:
            bottom_ = utila.roundme(bottom / pageheight)
            footer = FixedFooterInformation(
                begin=bottom_,
                end=hey.textnavigator.navigator.END,
            )

        footerandheader = groupme.footer.PageContentFooterHeader(
            header=header,
            footer=footer,
            page=page.page,
        )
        result[page.page] = footerandheader
    return result
