# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import serializeraw
import utila
import yaml

import groupme.border.leftright
import groupme.border.most
import hey.utils


def work(
        sizeandborder: str,
        textpositions: str,
        pages: tuple = None,
) -> typing.Tuple[str]:
    sizeandborder = serializeraw.load_pageborders(sizeandborder, pages=pages)
    textpositions = serializeraw.load_textpositions(textpositions, pages=pages)

    result = determine_border(textpositions, sizeandborder)

    result = [utila.from_tuple(item) for item in result]

    dumped = yaml.dump(result)
    return dumped


def content_pages(*pageable) -> list:
    result = []
    for pages in pageable:
        for item in pages:
            result.append(item.page)
    result = utila.make_unique(result)
    result = sorted(result)
    return result


def determine_border(
        textpositions: iamraw.PageContentTextPositions,
        pagesizes: iamraw.PageSizeBorderList,
):
    pages = pagecluster(pagesizes)

    result = []
    for cluster in pages:
        textpositions_ = utila.select_pages(textpositions, cluster)
        pagesizes_ = utila.select_pages(pagesizes, cluster)

        textpositions_ = hey.utils.not_none(textpositions_)
        pagesizes_ = hey.utils.not_none(pagesizes_)

        most = groupme.border.most.run(pagesizes_)
        leftright_ = groupme.border.leftright.run(textpositions_, pagesizes_)

        def border_detector(leftright, most, page: int):
            # left, right, top, down
            # TODO: CHECK THAT PAGE CALL IS CORRECT
            left = leftright.left
            if isinstance(left, tuple):
                left = left[page % 2]  # pylint:disable=E1136

            right = leftright.right
            if isinstance(right, tuple):
                right = right[page % 2]  # pylint:disable=E1136

            pagesize = utila.select_page(pagesizes, page).size
            rightborder = pagesize.width - right
            bottomborder = pagesize.height - most.bottom

            result = (left, rightborder, most.top, bottomborder)
            result = utila.roundme(result)
            return result

        result.append([
            (page, *border_detector(leftright_, most, page)) for page in cluster
        ])
    result = utila.flatten(result)
    # sort by page number
    result = sorted(result, key=lambda x: x[0])
    return result


def pagecluster(pagesizes) -> list:

    def equal_size(candidat, clusteritem):
        # TODO: HOLY VALUE
        return hey.utils.lengths(candidat[0], clusteritem[0]) < 10.0

    grouped = utila.determine_cluster(
        pagesizes,
        classifier=equal_size,
        min_elements=3,  # TODO: HOLY VALUE
    )

    pages = [sorted(item.page for item in cluster) for cluster in grouped]
    return pages
