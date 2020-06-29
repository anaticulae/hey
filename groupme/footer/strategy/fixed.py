# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Fixed Footer Extraction Strategy
================================

Examples:

- bachelor/page_111_images_toc.pdf
- docu/restructuredtext.pdf

Master of the art:

- docu/vimguide.pdf: This example contains a lot of tables, therefore we
  have a lot of horizontal lines which challenges the algorithm.
"""
import itertools
import typing

import configo
import iamraw
import texmex
import utila

import groupme.footer
import groupme.footer.headnotes
import groupme.footer.strategy as gfs
import groupme.horizontals
import groupme.utils


class FixedFooterStrategy(gfs.FooterHeaderDetectionStrategy):
    """The `FixedFooterStrategy` detects footer and header depending on
    horizontal line position. The strategy detects the most common
    border for header and footer.

    The header is located in [top, `HEADER_MAX_SIZE`]
    The footer is located in [bottom-`FOOTER_MAX_SIZE`, bottom].

    TODO: Run strategy with second common, third common header/footer again.
    """

    def result(self):
        if not self.pagetextnavigators:
            return []
        # TODO: HOW TO HANDLE DIFFERENT PAGE HEIGHTS
        # TODO: GROUP PAGE BY PAGESIZE FIRST AND THEN COMPUTE FOR EVERY
        # DIFFERENT PAGE SIZE
        first_page = self.pagetextnavigators[0].page
        pageheight = self.pageheight(first_page)

        # determine most common border for all pages
        tops, bottoms = extract_common_footer(
            horizontals=self.horizontals,
            pageheight=pageheight,
            max_group_count=MAX_FOOTERHEADER_AREA_COUNT,
        )
        footerheader = []
        for top, bottom in itertools.zip_longest(tops, bottoms):
            # look for every page if footer/header are present
            extracted = extract_page_footerheader(
                horizontals=self.horizontals,
                top=top,
                bottom=bottom,
                pageheight=pageheight,
                pagetextnavigators=self.pagetextnavigators,
            )
            footerheader.extend(extracted)
        footerheader = decide_multiple(footerheader)
        return footerheader

    def report(self) -> gfs.FooterStrategyResultReport:
        pass


def decide_multiple(items):
    """Decide for a single page which extracted header/footer is correct.

    In some cases there are more than one possible horizontal headlines
    or footlines. This can happen when having different FixedHeader or
    MovingFooter. This strategy decides on the count of extracted
    header. The main propose is to have a single header/footer per page.
    """
    selected = {}
    for item in items:
        try:
            cur = selected[item.page]
            itemcount = len([it for it in [item.header, item.footer] if it])
            currentcount = len([it for it in [cur.header, cur.footer] if it])
            if itemcount > currentcount:
                # replace current result with better result
                selected[item.page] = item
        except KeyError:
            selected[item.page] = item
    result = [item for item in selected.values()]
    result = sorted(result, key=lambda x: x.page)
    return result


def extract_common_footer(
        horizontals: iamraw.PagesWithHorizontalList,
        pageheight: int,
        max_group_count: int = 1,
) -> typing.Tuple[int, int]:
    """Extract common footer and header based on horizontal lines.

    Args:
        horizontals: list of extract horizontals for every page
        pageheight: height of the first page in the document
        max_group_count: max count of different areas
    Returns:
        a tuple with the `top` and `bottom` border of header and footer.
        None - If no header or footer is detected.
    """
    with_box = [[(
        horizontal.box,
        horizontal,
    ) for horizontal in page.content] for page in horizontals]

    # cluster horizontal lines
    clusters = utila.common_items(
        collected=with_box,
        max_difference=COMMON_HORIZONTAL_CLASSIFICATOR_MAX_ERROR,
    )
    if not clusters:
        return NO_CLUSTER

    top = extract_inarea(
        clusters,
        pageheight=pageheight,
        upper_bound=texmex.START,
        lower_bound=HEADER_MAX_SIZE,
        max_group_count=max_group_count,
    )
    bottom = extract_inarea(
        clusters,
        pageheight=pageheight,
        upper_bound=texmex.END - FOOTER_MAX_SIZE,
        lower_bound=texmex.END,
        max_group_count=max_group_count,
    )

    if top is None:
        # could not detect any header
        top = [texmex.START]

    if bottom is None:
        # could not detect any footer
        bottom = [pageheight]

    # the header is on the top(0.0) and the footer is on the bottom(1.0)
    assert max(top) < min(bottom), f'{top} < {bottom}'
    return top, bottom


def extract_page_footerheader(
        horizontals: iamraw.PagesWithHorizontalList,
        top: float,
        bottom: float,
        pageheight: float,
        pagetextnavigators: texmex.PageTextNavigators,
) -> iamraw.PageContentFooterHeaders:
    """Extract footer and header which matches `top` and `bottom`.

    Args:
        horizontals: pages with horizontal lines
        top(pixel): position of header-border horizontal line
        bottom(pixel): position of footer-border horizontal line
        pageheight(pixel): height of pages in pixel
        pagetextnavigators: list of page content
    Returns:
        list of `iamraw.PageContentFooterHeader` for every
        page with header and footer information.
    """
    result = []
    for page in horizontals:
        content = page.content
        textnavigator = utila.select_page(pagetextnavigators, page.page)

        header = None
        if top is not None and groupme.horizontals.match(content, top):
            header = create_header(top, pageheight, textnavigator)

        footer = None
        if bottom is not None and groupme.horizontals.match(content, bottom):
            bottom_ = utila.roundme(bottom / pageheight)
            footer = iamraw.FixedFooterInformation(
                begin=bottom_,
                end=texmex.END,
            )

        if header is None and footer is None:
            # no matching horizontals
            continue

        footer_header = iamraw.PageContentFooterHeader(
            header=header,
            footer=footer,
            page=page.page,
        )
        result.append(footer_header)
    return result


def create_header(top, pageheight, textnavigator):
    top_ = utila.roundme(top / pageheight)  # TODO: Replace with utila method
    # XXX: 10% percent cause of bad font-bounding-boxing
    top_ = utila.roundme(top_ * 1.1)
    headercontent = textnavigator.between(
        texmex.START,
        top_,
    )
    parsed = groupme.footer.headnotes.parse(headercontent)

    result = iamraw.FixedHeaderInformation(begin=texmex.START, end=top_)
    for item in parsed:
        if isinstance(item, iamraw.HeaderTitle):
            result.title = item
        if isinstance(item, iamraw.RawText):
            result.undefined.append(item)  # pylint:disable=E1101
        if isinstance(item, iamraw.PageInformation):
            result.page = item
    return result



NO_CLUSTER = [texmex.START], [texmex.END] # yapf:disable

# max difference between left and right y-coordinate
COMMON_HORIZONTAL_CLASSIFICATOR_MAX_ERROR = configo.HV_FLOAT_PLUS(default=2.0).value # yapf:disable

# minimal horizontal line count in cluster to avoid low item cluster
MIN_CLUSTER_SIZE = configo.HV_INT_PLUS(default=10).value

# maximal count of different header/footer areas
MAX_FOOTERHEADER_AREA_COUNT = configo.HV_INT_PLUS(default=5).value

# maximal distance from page top in percent where header can be detected
HEADER_MAX_SIZE = configo.HV_PERCENT_PLUS(default=15, limit=100).value

# maximal distance from page bottom in percent where footer can be detected
FOOTER_MAX_SIZE = configo.HV_PERCENT_PLUS(default=20, limit=100).value


def extract_inarea(
        clusters: typing.List,
        pageheight: int,
        upper_bound: float = texmex.START,
        lower_bound: float = texmex.END,
        max_group_count: int = 1,
        min_group_size: int = MIN_CLUSTER_SIZE,
) -> float:
    """Determine all elements in the potential footer/header area"""
    ymin = pageheight * upper_bound
    ymax = pageheight * lower_bound

    result = groupme.horizontals.biggest_hlinecluster_in_area(
        clusters,
        ymin=ymin,
        ymax=ymax,
        max_group_count=max_group_count,
        min_group_size=min_group_size,
    )
    if not result:
        return None
    return result
