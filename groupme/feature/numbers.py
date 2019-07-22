# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Start working on footer extractor.

Required resources:

    # PageSize
    # HorizontalLines
    # Text annotated with location

Required API:

    # before/ after method to determine items
"""
from functools import lru_cache
from typing import List
from typing import Tuple

from iamraw import BoundingBox
from serializeraw import dump_pagenumbers
from serializeraw import load_document
from utila import Flag
from utila import call
from utila import from_raw_or_path
from yaml import FullLoader
from yaml import load

from hey import CACHE_SMALL
from hey.cluster import common_items
from hey.textnavigator.navigator import create_pagetextnavigators


def work(documentpath: str, positionpath: str) -> str:
    call('numbers')
    document = load_document(documentpath)
    position = load_textposition(positionpath)

    navigator = create_pagetextnavigators(
        text=document,
        text_position=position,
    )

    footer_pagenumbers = determine_pagenumbers(navigator)
    dumped = dump_pagenumbers(footer_pagenumbers)

    return dumped


def determine_pagenumbers(navigator):
    footer_ = footer(navigator)
    return pagenumbers(footer_)


@lru_cache(CACHE_SMALL)
def load_textposition(content: str):
    # TODO: This is from rawmaker->position.py,
    # TODO: remove after moving to serialzeraw
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)

    result = []
    for page in loaded:
        pagedata = {}
        for item in page['content']:
            key, position = item.split(maxsplit=1)
            pagedata[int(key)] = BoundingBox.from_str(position)
        result.append(pagedata)
    return result


TOP_BORDER = 0.1  # Header in the range of 0% till 10%
TOP_MAX_DIFFERENCE = 20.0

BOTTOM_BORDER = 0.9  # Footer is in range of 90% till 100%
BOTTOM_MAX_DIFFERENCE = 10.0


def header(navigators):
    collected = [page.before(TOP_BORDER) for page in navigators]
    common = common_items(collected, max_difference=TOP_MAX_DIFFERENCE)
    return common


def footer(navigators):
    collected = [page.after(BOTTOM_BORDER) for page in navigators]
    common = common_items(collected, max_difference=BOTTOM_MAX_DIFFERENCE)
    return common


def is_pagenumber(item: str) -> bool:
    item = str(item).lower()
    if item.isnumeric():
        return True
    # TODO: improve this method, first try
    # 'i ii iii iv v vi vii viii ix xi'
    roman = {'i', 'v', 'x', 'c', 'l'}
    isroman = all([test in roman for test in item])
    if isroman:
        return True
    return False


def is_rightpage(pdf_pagenumber: int) -> bool:
    """What pdf page is the left side?
    The first page is the right page? """
    pdf_pagenumber = int(pdf_pagenumber)
    return pdf_pagenumber % 2 == 0


Cluster = List[Tuple[BoundingBox, str]]


def pagenumbers(clusters: List[Cluster]):
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
        for pdf_page, (bounding, content) in cluster:
            content = str(content)
            if not is_pagenumber(content):
                continue
            try:
                content = int(content)
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
    return Flag(
        longcut=name(),
        message='extract page numbers from footer and header',
    )
