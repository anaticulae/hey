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

    - docu/restructuredtext.pdf

Master of the art:

    - docu/vimguide.pdf: This example contains a lot of tables, therefore
                         we have a lot of horizontal lines which challenges
                         the algorithm.
"""
import dataclasses
import typing

import configo.holyvalue
import iamraw
import utila

import groupme.footer
import groupme.horizontals
import groupme.utils
import hey.textnavigator.navigator


class FixedFooterStrategy(groupme.footer.FooterHeaderDetectionStrategy):
    """The `FixedFooterStrategy` detects footer and header depending on
    horizontal line position. The strategy detects the most common
    border for header and footer.

    The header is located in [top, `HEADER_MAX_SIZE`]
    The footer is located in [bottom-`FOOTER_MAX_SIZE`, bottom].

    TODO: Run strategy with second common, third common header/footer again.
    """

    def result(self):
        # TODO: HOW TO HANDLE DIFFERENT PAGE HEIGHTS
        pageheight = self.pageheight(0)

        # determine most common border for all pages
        top, bottom = extract_common_footer(
            horizontals=self.horizontals,
            pageheight=pageheight,
        )

        # look for every page if footer/header are present
        extracted = extract_page_footerheader(
            horizontals=self.horizontals,
            top=top,
            bottom=bottom,
            pageheight=pageheight,
        )
        return extracted


@dataclasses.dataclass  # pylint:disable=R0903
class FixedHeaderInformation(groupme.footer.HeaderInformation):
    pass


@dataclasses.dataclass  # pylint:disable=R0903
class FixedFooterInformation(groupme.footer.FooterInformation):
    pass


def extract_common_footer(
        horizontals: iamraw.PagesWithHorizontalList,
        pageheight: int,
):
    """Extract common footer and header based on horizontal lines.

    Args:
        horizontals: list of extract horizontals for every page
        pageheight: height of the first page in the document
    Returns:
        a tuple with the `top` and `bottom` border of header and footer.
        None - If no header or footer is detected.
    """
    with_box = [[(
        horizontal.box,
        horizontal,
    ) for horizontal in page.content] for page in horizontals]

    # cluster horizontal lines
    clusters = hey.cluster.common_items(
        collected=with_box,
        max_difference=COMMON_HORIZONTAL_CLASSIFICATOR_MAX_ERROR,
    )
    if not clusters:
        return NO_CLUSTER

    top = extract_inarea(
        clusters,
        pageheight=pageheight,
        upper_bound=hey.textnavigator.navigator.START,
        lower_bound=HEADER_MAX_SIZE,
    )
    bottom = extract_inarea(
        clusters,
        pageheight=pageheight,
        upper_bound=hey.textnavigator.navigator.END - FOOTER_MAX_SIZE,
        lower_bound=hey.textnavigator.navigator.END,
    )

    if top is None:
        # could not detect any header
        top = hey.textnavigator.navigator.START

    if bottom is None:
        # could not detect any footer
        bottom = pageheight

    # the header is on the top(0.0) and the footer is on the bottom(1.0)
    assert top < bottom, '%.2f < %.2f' % (top, bottom)
    return top, bottom


def extract_page_footerheader(
        horizontals: iamraw.PagesWithHorizontalList,
        top: float,
        bottom: float,
        pageheight: float,
) -> typing.List[groupme.footer.PageContentFooterHeader]:
    """Extract footer and header which matches `top` and `bottom`.

    Args:
        horizontals: pages with horizontal lines
        top(pixel): position of header-border horizontal line
        bottom(pixel): position of footer-border horizontal line
        pageheight(pixel): height of pages in pixel
    Returns:
        list of `groupme.footer.PageContentFooterHeader` for every
        page with header and footer information.
    """
    result = []
    for page in horizontals:
        header = None
        top_match = groupme.horizontals.match(page.content, top)
        if top_match:
            top_ = utila.roundme(top / pageheight)
            header = FixedHeaderInformation(
                begin=hey.textnavigator.navigator.START,
                end=top_,
            )

        footer = None
        bottom_match = groupme.horizontals.match(page.content, bottom)
        if bottom_match:
            bottom_ = utila.roundme(bottom / pageheight)
            footer = FixedFooterInformation(
                begin=bottom_,
                end=hey.textnavigator.navigator.END,
            )

        footer_header = groupme.footer.PageContentFooterHeader(
            header=header,
            footer=footer,
            page=page.page,
        )
        result.append(footer_header)
    return result


# TODO: REMOVE AFTER HAVING CONCEPT FOR DEFAULT CONFIGURATION
configo.holyvalue.DATABASE = configo.holyvalue.DataBase(
    __file__,
    current=configo.holyvalue.DataSet(),
)
# max difference between left and right y-coordinate
COMMON_HORIZONTAL_CLASSIFICATOR_MAX_ERROR = configo.HV(
    default=2.0,
    datatype=configo.DataType.FLOAT_PLUS,
)

NO_CLUSTER = hey.textnavigator.navigator.START, hey.textnavigator.navigator.END

# maximal distance from page top in percent where header can be detected
HEADER_MAX_SIZE = configo.HV(
    default=15,
    limit=100,
    datatype=configo.DataType.PERCENT_PLUS,
)

# maximal distance from page bottom in percent where footer can be detected
FOOTER_MAX_SIZE = configo.HV(
    default=20,
    limit=100,
    datatype=configo.DataType.PERCENT_PLUS,
)


def extract_inarea(
        clusters: typing.List,
        pageheight: int,
        upper_bound: float = hey.textnavigator.navigator.START,
        lower_bound: float = hey.textnavigator.navigator.END,
) -> float:
    """Determine all elements in the potential footer/header area"""
    ymin = pageheight * upper_bound
    ymax = pageheight * lower_bound

    result = groupme.horizontals.biggest_hlinecluster_in_area(
        clusters,
        ymin=ymin,
        ymax=ymax,
        max_groups=1,
    )
    if not result:
        return None
    return result[0]
