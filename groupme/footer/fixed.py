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

    - bachelor/page_111_images_toc.pdf
    - docu/restructuredtext.pdf

Master of the art:

    - docu/vimguide.pdf: This example contains a lot of tables, therefore
                         we have a lot of horizontal lines which challenges
                         the algorithm.
"""
import collections
import dataclasses
import itertools
import typing

import configo.holyvalue
import iamraw
import utila

import groupme.footer
import groupme.footer.headnotes
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
        return footerheader


@dataclasses.dataclass
class FixedHeaderInformation(groupme.footer.HeaderInformation):

    title: groupme.footer.headnotes.HeaderTitle = None

    undefined: typing.List[groupme.footer.headnotes.RawText] =\
                                         dataclasses.field(default_factory=list)

    images: typing.List[groupme.footer.headnotes. HeaderImages] =\
                                         dataclasses.field(default_factory=list)


@dataclasses.dataclass  # pylint:disable=R0903
class FixedFooterInformation(groupme.footer.FooterInformation):
    pass


def extract_common_footer(
        horizontals: iamraw.PagesWithHorizontalList,
        pageheight: int,
        max_group_count: int = 1,
):
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
        max_group_count=max_group_count,
    )
    bottom = extract_inarea(
        clusters,
        pageheight=pageheight,
        upper_bound=hey.textnavigator.navigator.END - FOOTER_MAX_SIZE,
        lower_bound=hey.textnavigator.navigator.END,
        max_group_count=max_group_count,
    )

    if top is None:
        # could not detect any header
        top = [hey.textnavigator.navigator.START]

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
        pagetextnavigators,
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
        content = page.content
        textnavigator = utila.select_page(pagetextnavigators, page.page)

        header = None
        if top is not None and groupme.horizontals.match(content, top):
            header = create_header(top, pageheight, textnavigator)

        footer = None
        if bottom is not None and groupme.horizontals.match(content, bottom):
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


def create_header(top, pageheight, textnavigator):
    """
    Args:
        top(pixel)
    """
    top_ = utila.roundme(top / pageheight)  # TODO: Replace with utila method
    # XXX: 10% percent cause of bad font-bounding-boxing
    top_ = utila.roundme(top_ * 1.1)
    headercontent = textnavigator.between(
        hey.textnavigator.navigator.START,
        top_,
    )
    parsed = groupme.footer.headnotes.parse(headercontent)

    result = FixedHeaderInformation(
        begin=hey.textnavigator.navigator.START,
        end=top_,
    )
    for item in parsed:
        if isinstance(item, groupme.footer.headnotes.HeaderTitle):
            result.title = item
        if isinstance(item, groupme.footer.headnotes.RawText):
            result.undefined.append(item)  # pylint:disable=E1101
        if isinstance(item, groupme.footer.PageInformation):
            result.page = item
    return result


def remove_duplication(items):
    """In some cases more than one potential header or footer are
    detected for one page. This method judges the problem and select the
    `best` result.
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
    # TODO: Stategy how to judge multiple matches
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


NO_CLUSTER = [hey.textnavigator.navigator.START], [hey.textnavigator.navigator.END] # yapf:disable

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

# minimal horizontal line count in cluster to avoid low item cluster
MIN_CLUSTER_SIZE = configo.HV(
    default=10,
    datatype=configo.DataType.INT_PLUS,
)

# maximal count of different header/footer areas
MAX_FOOTERHEADER_AREA_COUNT = configo.HV(
    default=5,
    datatype=configo.DataType.INT_PLUS,
)

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
