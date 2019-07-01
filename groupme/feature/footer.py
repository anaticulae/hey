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
from serializeraw import load_horizontals
from utila import from_raw_or_path
from utila import uniform_result
from yaml import FullLoader
from yaml import dump
from yaml import load

from groupme.feature.numbers import common_items
from hey.utils import roundme


def work(horizontal_lines: str) -> str:
    """Extract footer and header area out of horizontal lines

    Args:
        horizontal_lines(str): path to file with extract lines
    Returns:
        dumped list with top and bottom border for every page
    """

    # load
    horizontals = load_horizontals(horizontal_lines)

    # work
    extracted = extract_pages(horizontals)

    # dump
    dumped = dump_headerfooter(extracted)
    return dumped


Top = float
Bottom = float

FooterBorder = Tuple[Top, Bottom]


def document_footer(horizontals) -> FooterBorder:
    extracted = extract_pages(horizontals)

    top = [item for (item, _) in extracted]
    bottom = [item for (_, item) in extracted]

    top = mode(top)
    bottom = mode(bottom)
    return top, bottom


def footerborder_to_bounds(border: FooterBorder) -> Border:
    border = Border(None, border[1], None, border[0])
    return border


def extract_pages(horizontals: List):
    assert isinstance(horizontals, List), str(horizontals)
    # determine border for all pages
    top, bottom = extract_common_footer(horizontals)
    # look for every page if footer/header are present
    extracted = extract_page_footerheader(horizontals, top, bottom)
    return extracted


def extract_common_footer(horizontal_lines):
    with_box = [[(
        horizontal.box,
        horizontal,
    ) for horizontal in page] for page in horizontal_lines]

    # cluster horizontal lines
    clusters = common_items(with_box, max_difference=2.0)

    top = header(clusters)
    bottom = footer(clusters)

    assert top > bottom

    return top, bottom


def extract_page_footerheader(
        horizontal_lines,
        top: float,
        bottom: float,
) -> List:
    result = []
    for page in horizontal_lines:
        topped = match_horizontals(page, top)
        bottomed = match_horizontals(page, bottom)

        result.append((
            roundme(top * topped),
            roundme(bottom * bottomed),
        ))
    return result


Header = float
Footer = float


def dump_headerfooter(pages) -> str:
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


def match_horizontals(todo, position: float):
    return any(item.box.y_top == position for item in todo)


def footer(clusters: List) -> float:
    # TODO: remove holy value
    # TODO: Make dependent on page size
    return area(clusters, 0, 100)


def header(clusters: List) -> float:
    # TODO: Make dependent on page size
    return area(clusters, 700, 800)


def area(clusters: List, ymin: float, ymax: float) -> int:
    bottom = area_likelihood(clusters, ymin, ymax)
    if not bottom:  # empty cluster
        return None
    index = bottom.index(max(bottom))

    _, (bounding, __) = clusters[index][0]

    return bounding.y_bottom


EMPTY = (0, 0.0)


def area_likelihood(clusters, ymin, ymax):
    result = []
    for cluster in clusters:
        _, item = cluster[0]
        bounding, _ = item
        assert bounding.y_top == bounding.y_bottom
        yvalue = bounding.y_top
        if not ymin <= yvalue <= ymax:
            result.append(EMPTY)
            continue

        result.append((
            len(cluster),
            1.0,  # TODO: need a better classificator
        ))
    uniformed = uniform_result(result)
    return uniformed
