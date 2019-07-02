# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
TODO:
    what should we do with empty header/footer
"""
from statistics import mode
from typing import List
from typing import Tuple

from iamraw import Border
from iamraw import Box
from iamraw import HorizontalLine
from serializeraw import load_horizontals
from utila import from_raw_or_path
from utila import uniform_result
from yaml import FullLoader
from yaml import dump
from yaml import load

from hey.cluster import common_items
from hey.utils import roundme

# TODO: Remove after upgrading iamraw
PagesWithBoxList = List[List[Box]]
PagesWithHorizontalList = List[List[HorizontalLine]]

Header = float
Footer = float

Top = float
Bottom = float

FooterBorder = Tuple[Top, Bottom]


def work(horizontals: str) -> str:
    """Extract footer and header area out of horizontal lines

    Args:
        horizontals(str): path to file with extract lines
    Returns:
        dumped list with top and bottom border for every page
    """

    # load
    horizontals = load_horizontals(horizontals)

    # work
    extracted = extract_pages(horizontals)

    # dump
    dumped = dump_headerfooter(extracted)
    return dumped


def extract_pages(horizontals: List[List[HorizontalLine]],
                 ) -> List[FooterBorder]:
    assert isinstance(horizontals, List), str(horizontals)
    # determine border for all pages
    top, bottom = extract_common_footer(horizontals)
    # look for every page if footer/header are present
    extracted = extract_page_footerheader(horizontals, top, bottom)
    return extracted


def document_footerheader(horizontals: PagesWithHorizontalList,
                         ) -> FooterBorder:
    """Extract most common header/footer of the document

    Args:
        horizontals: a list of pages with a list of horizontals
    Return:
        the most common header/foooter combination for the document
    """
    extracted = extract_pages(horizontals)

    top = [item for (item, _) in extracted]
    bottom = [item for (_, item) in extracted]

    top = mode(top)
    bottom = mode(bottom)
    return top, bottom


def extract_common_footer(horizontals: PagesWithHorizontalList):
    with_box = [[(
        horizontal.box,
        horizontal,
    ) for horizontal in page] for page in horizontals]

    # cluster horizontal lines
    clusters = common_items(with_box, max_difference=2.0)

    top = header(clusters)
    bottom = footer(clusters)

    # the header is on the top(0.0) and the footer is on the bottom(1.0)
    assert top < bottom, '%.2f < %.2f' % (top, bottom)
    return top, bottom


def extract_page_footerheader(
        horizontals: PagesWithHorizontalList,
        top: float,
        bottom: float,
) -> List[FooterBorder]:
    result = []
    for page in horizontals:
        topped = match_horizontals(page, top)
        bottomed = match_horizontals(page, bottom)

        result.append((
            roundme(top * topped),
            roundme(bottom * bottomed),
        ))
    return result


def match_horizontals(todo: List[HorizontalLine], vertical_position: float):
    """Check if any horizontal match the `vertical_position`

    Args:
        todo(List[HorizontalLine]): list with horizontal lines, mostly one page
        vertical_position(float): position on the page in 'pixel'
    Returns:
        True if any horizontal line match the `vertical_position`
    """
    vertical_position = round(vertical_position, 1)
    return any(round(item.box.y0, 1) == vertical_position for item in todo)


def footer(clusters: List) -> float:
    """Determine all elements in the potential footer area"""
    # TODO: remove holy value
    # TODO: Make dependent on page size
    return area(clusters, 700, 800)


def header(clusters: List) -> float:
    """Determine all elements in the potential header area"""
    # TODO: Make dependent on page size
    return area(clusters, 0, 100)


def area(clusters: List, ymin: float, ymax: float) -> int:
    bottom = area_likelihood(clusters, ymin, ymax)
    if not bottom:  # empty cluster
        return None
    index = bottom.index(max(bottom))

    _, (bounding, __) = clusters[index][0]

    # return top or bottom? The element is a line, so it does not matter
    return bounding.y1  # y0?


EMPTY = (0, 0.0)


def area_likelihood(clusters, ymin, ymax):
    result = []
    for cluster in clusters:
        _, item = cluster[0]
        bounding, _ = item
        assert bounding.y0 == bounding.y1
        yvalue = bounding.y0
        if not ymin <= yvalue <= ymax:
            result.append(EMPTY)
            continue

        result.append((
            len(cluster),
            1.0,  # TODO: need a better classificator
        ))
    uniformed = uniform_result(result)
    return uniformed


def footerborder_to_border(border: FooterBorder) -> Border:
    """Convert FooterBorder to Border"""
    border = Border(
        bottom=border[1],
        left=None,
        right=None,
        top=border[0],
    )
    return border


def dump_headerfooter(pages) -> str:
    # TODO: Move to iamraw
    result = []
    for index, (top, bottom) in enumerate(pages):
        result.append({
            'page': index,
            'headerfooter': '%.2f %.2f' % (top, bottom),
        })
    return dump(result)


def load_headerfooter(content: str) -> List[Tuple[Header, Footer]]:
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)

    result = []
    for item in loaded:
        top, bottom = [
            float(splitted) for splitted in item['headerfooter'].split()
        ]
        result.append((top, bottom))
    return result
