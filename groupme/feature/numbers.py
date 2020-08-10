# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Page Numbers Extraction Step
============================

Start working on footer extractor.

Required resources:

    # PageSize
    # HorizontalLines
    # Text annotated with location

Required API:

    # before/ after method to determine items
"""

import collections
import typing

import iamraw
import serializeraw
import texmex
import utila

PageContentTextPosition = collections.namedtuple(
    'PageContentTextPosition',
    'content, page',
)


def work(documentpath: str, positionpath: str, pages: tuple = None) -> str:
    utila.call('numbers')
    document = serializeraw.load_document(documentpath, pages=pages)
    position = serializeraw.load_textpositions(positionpath, pages=pages)

    navigator = texmex.create_pagetextnavigators(
        text=document,
        text_positions=position,
    )
    footer_pagenumbers = determine_pagenumbers(navigator)
    dumped = serializeraw.dump_pagenumbers(footer_pagenumbers)

    return dumped


def determine_pagenumbers(navigator):
    footer_ = footer(navigator)
    return pagenumbers(footer_)


# TODO: REPLACE HOLY VALUE
TOP_BORDER = 0.1  # Header in the range of 0% till 10%
TOP_MAX_DIFFERENCE = 20.0

# TODO: Think about scaling this value depending on result
BOTTOM_BORDER = 0.8  # Footer is in range of 80% till 100%
BOTTOM_MAX_DIFFERENCE = 20.0
BOTTOM_MAX_AREA = 2500.0  # page number is not very big


def header(navigators):
    collected = [page.before(TOP_BORDER) for page in navigators]
    common = utila.common_items(
        collected,
        max_difference=TOP_MAX_DIFFERENCE,
        selector=lambda x: x.bounding,
    )
    return common


def footer(
        navigators,
        *,
        max_area: float = BOTTOM_MAX_AREA,
        max_difference: float = BOTTOM_MAX_DIFFERENCE,
        min_elements: int = 4,
        numbers_only: bool = True,
        remove_empty: bool = True,
) -> list:
    """Detect similar elements in footer area which are duplicated on
    different pages.

    Args:
        navigators(list): list of text navgiators
        max_area(float): size of items which are grouped to a cluster
        max_difference(float): difference of BoundingBox-coordinates in
                               same cluster
        min_elements(int): minimum elements of detected clusters
        numbers_only(bool): if True, remove all non numeric/romanic elements
        remove_empty(bool): remove empty elements, e.g. whitespaces
    Returns:
        A list of clustered page footer content which are expected of
        beeing the page numbers.
    """
    # TODO: MOVE THIS METHOD TO MORE GENERAL FOOTER FILE BECAUSE THIS CODE
    # HAS NOTHING TODO WITH NUMBERS
    # TODO: Split method into numbers part and grouping part
    collected = [(page.page, page.after(BOTTOM_BORDER)) for page in navigators]
    filtered = []
    for pagenumber, footercontent in collected:
        pagecontent = []
        for item in footercontent:
            text = item.text.strip()
            if iamraw.area(item.bounding) > max_area:
                # ignore to big items
                continue
            if remove_empty and not text:
                # filter empty items
                continue
            if numbers_only and not is_pagenumber(text):
                # remove non numeric items
                continue
            # support -1-, -2-, ...
            clean_number = text.replace('-', '', 2).strip()
            # TODO: DELIVER RAW DATA FOR FOOTER PAGES STRATEGY DETECTION
            item = (item.bounding, clean_number, pagenumber)
            pagecontent.append(item)
        filtered.append(pagecontent)
    common = utila.common_items(
        filtered,
        max_difference=max_difference,
        min_elements=min_elements,
    )
    return common


def is_pagenumber(number: str) -> bool:
    """Determine if passed `number` is a page number. Empty `number` is
    not a page number.

    Examples:
        1, 2, 3, 4,
        -1-, -2-, -3-
        i, ii, iii, iiv, iv, v

    Args:
        number(str): string to check if it is a number
    Returns:
        True if roman or numeric number is given
    """
    # - 1 -, -2-,
    number = str(number).replace('-', '', 2)
    number = number.strip()
    if not number:
        return False
    if number.isnumeric():
        return True
    number = number.lower()
    # 'i ii iii iv v vi vii viii ix xi'
    roman = {'i', 'v', 'x', 'c', 'l'}
    isroman = all([test in roman for test in number])
    if isroman:
        return True
    return False


def is_rightpage(pdf_pagenumber: int) -> bool:
    """What pdf page is the left side?
    The first page is the right page? """
    pdf_pagenumber = int(pdf_pagenumber)
    return pdf_pagenumber % 2 == 0


Cluster = typing.List[typing.Tuple[iamraw.BoundingBox, str]]


def pagenumbers(clusters: typing.List[Cluster]) -> list:
    """Determine pagenumbers out of list of cluster

    2. Scenarios are possible, we have alternating left and right page numbers
    or the page numbers are only on one possition.

    Args:
        clusters: List of cluster -> List[List[(boundingbox, content)]]
    Returns:
        singlepage or (left, right)
    """
    used_cluster = set()
    left, right = [], []
    for clusterid, cluster in enumerate(clusters):
        for _, (bounding, content, pdf_page) in cluster:
            content = str(content)
            if not is_pagenumber(content):
                continue
            try:
                content = int(content)  # pylint:disable=R0204
            except ValueError:
                # roman number
                pass
            # save number as tuple of pdf_page and detected page
            used_cluster.add(clusterid)
            content = (
                pdf_page,
                bounding,
                content,
            )
            if is_rightpage(pdf_page):
                right.append(content)
            else:
                left.append(content)
    if len(used_cluster) == 1:
        # One cluster is used, we do not have right and left pagenumber
        singlepage = []
        singlepage.extend(left)
        singlepage.extend(right)
        # Sort by pdfpage
        singlepage = [
            item for item in sorted(singlepage, key=lambda number: number[0])
        ]
        return singlepage
    return left, right


def name():
    return 'pagenumbers'


def commandline():
    return utila.Flag(
        longcut=name(),
        message='extract page numbers from footer and header',
    )
