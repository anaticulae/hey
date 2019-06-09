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

from itertools import chain
from typing import Iterable
from typing import List
from typing import Tuple

from iamraw import BoundingBox
from iamraw import Document
from serializeraw import load_document
from utila import Flag
from utila import from_raw_or_path
from yaml import FullLoader
from yaml import dump
from yaml import load

from groupme.textnavigator import load_pagetextnavigator


def work(documentpath: str, positionpath: str) -> str:
    document = load_document(documentpath)
    position = load_textposition(positionpath)

    navigator = load_pagetextnavigator(position, document)

    footer_pagenumbers = determine_pagenumbers(navigator)
    dumped = dump_pagenumbers(footer_pagenumbers)

    return dumped


def determine_pagenumbers(navigator):
    footer_ = footer(navigator)
    return pagenumbers(footer_)


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


def dump_pagenumbers(pagenumbers_):

    def raw(content):
        items = [{
            'pdfpage': pdfpage,
            'bounding': bounding.raw(),
            'detected': detectedpage
        } for pdfpage, bounding, detectedpage in sorted(
            content, key=lambda number: number[0])]
        return items

    try:
        result = raw(pagenumbers_)
    except ValueError:
        left, right = pagenumbers_
        result = {
            'left': raw(left),
            'right': raw(right),
        }
    dumped = dump(result)
    return dumped


def load_pagenumbers(content: str):
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)

    def to_int(item):
        try:
            return int(item)
        except ValueError:
            return item

    def fromraw(content):
        result = [(
            to_int(item['pdfpage']),
            BoundingBox.from_str(item['bounding']),
            to_int(item['detected'],),
        ) for item in content]
        return result

    try:
        return fromraw(loaded)
    except TypeError:
        return fromraw(loaded['left']), fromraw(loaded['right'])


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
        return singlepage
    return left, right


def common_items(collected, max_difference: float):
    """Cluster items due `same_area_cluster`

    Args:
        collected:
        max_difference(float): upper bound of differences which is accepted
                               by classificator as same item.
    """
    flat = list(chain.from_iterable(collected))
    clusters = same_area_cluster(
        flat,
        max_difference=max_difference,
    )

    result = [page_from_cluster(cluster, collected) for cluster in clusters]
    return result


def page_from_cluster(cluster, collected):
    result = []
    for pagecount, content in enumerate(collected):
        result.extend([(
            pagecount,
            test,
        ) for test in content if test in cluster])
    return result


def three_side_cluster_equal(todo):

    def classificator(candidat, clusteritem):

        def matcher(candidat, clusteritem):
            candidat_pos, _ = candidat
            cluster_pos, _ = clusteritem

            eqaul = sum([
                abs(first - second) < 0.001  # float difference is allowed
                for (first, second) in zip(candidat_pos, cluster_pos)
            ])
            return eqaul >= 3

        return matcher(candidat, clusteritem)

    return determine_cluster(todo, classificator)


def same_area_cluster(todo, max_difference=10.0):

    def classificator(candidat, clusteritem, max_difference=max_difference):
        assert max_difference > 0.0

        from math import sqrt

        def distance(x0, y0, x1, y1):
            return sqrt(pow((x0 - x1), 2) + pow((y0 - y1), 2))

        def matcher(candidat, clusteritem):
            testbox, _ = candidat
            goalbox, _ = clusteritem
            equality = distance(
                testbox.x_bottom,
                testbox.y_bottom,
                goalbox.x_bottom,
                goalbox.y_bottom,
            ) + distance(
                testbox.x_top,
                testbox.y_top,
                goalbox.x_top,
                goalbox.y_top,
            )
            return equality <= max_difference

        return matcher(candidat, clusteritem)

    return determine_cluster(todo, classificator)


def determine_cluster(todo, classificator):
    import warnings
    warnings.warn('Remove after upgrading to utila 0.6.3', DeprecationWarning)
    if not todo:
        return []

    # prepare cluster, a single element is a cluster
    result = [[item] for item in todo]

    def match(result, current):
        for clusterindex, cluster in enumerate(result):
            for clusteritem in cluster:
                match = [
                    classificator(candidat=test, clusteritem=clusteritem)
                    for test in current
                ]
                if any(match):
                    return clusterindex
        return None

    def clusterme(result):
        result, todo = result[0], result[1:]
        if not isinstance(result[0], list):
            result = [result]
        while todo:
            current = todo.pop()
            index = match(result, current)
            if index is None:
                # No match, create new cluster
                result.insert(0, current)
            else:
                result[index].extend(current)
        return result

    # Break when cluster does not change result
    # Cluster till cluster move does not change the result
    before = set()
    while True:
        result = clusterme(result)
        hashid = hash(str(result))
        if hashid in before:
            break
        before.add(hashid)

    # A cluster must have at least 2 items
    clusters = [item for item in result if len(item) > 1]
    return clusters


def name():
    return 'footer'


def commandline():
    return Flag(
        longcut=name(),
        message='extract data from footer and header',
    )
