# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""common text strategy
====================

The ``common text strategy`` extracts header or footer based on common
text and images. There is no horizontal line required.

.. note ::
    TODO: SUPPORT COMMON IMAGES
"""

import collections

import configo
import iamraw
import texmex
import utila

import groupme.footer.strategy as gfs

COMMON_HEADER_MAX_ERROR = 1.0  # TODO: HOLY VALUE
# minimal items in a cluster to be detected and accepted as feature.
MIN_CLUSTER_COUNT = configo.HV_INT_PLUS(5)
MIN_OCCURRENCE = 0.5
TOP_AREA = 0.15  # TODO: HOLY VALUE


class CommonTextStrategy(gfs.FooterHeaderDetectionStrategy):  # pylint:disable=W0223

    def result(self):
        header = cluster_pages(self.pagetextnavigators)

        result = [
            iamraw.PageContentFooterHeader(
                header=header,
                footer=None,
                page=page,
            ) for (page, header) in header
        ]
        return result


def cluster_pages(pagenavigators):
    pagenumbers = len(pagenavigators)
    min_cluster_count = max([
        int(pagenumbers * MIN_OCCURRENCE),
        MIN_CLUSTER_COUNT,
    ])

    with_box = prepare_clustering(pagenavigators)

    # TODO REPLACE WITH COMMON POSITION CLUSTER
    clusters = utila.common_items(
        collected=with_box,
        max_difference=COMMON_HEADER_MAX_ERROR,
        min_elements=min_cluster_count,
    )
    if not clusters:
        return []

    result = {}
    for cluster in clusters:
        for (_, (bounding, text, pageheight, pagenumber)) in cluster:
            end = utila.roundme(bounding.y1 / pageheight)
            # remove newline at end TODO: REMOVE LATER
            text = text.text.strip()
            try:
                result[pagenumber].append(iamraw.RawText(text=text))
                result[pagenumber].extend(end=end)
            except KeyError:
                header = iamraw.FixedHeaderInformation(
                    begin=texmex.START,
                    end=end,
                    page=iamraw.PageInformation(value=pagenumber, raw=None),
                    undefined=[iamraw.RawText(text=text)]  # pylint:disable=E1101
                )
                result[pagenumber] = header
    result = [(item, result[item]) for item in sorted(result.keys())]
    return result


def prepare_clustering(pagetextnavigators):
    collected = []
    for page in pagetextnavigators:
        content = []
        for item in page.before(TOP_AREA):
            content.append((item.bounding, item, page.height, page.page))
        collected.append(content)

    valid = header_content(collected)
    result = []
    for page in collected:
        content = [item for item in page if item[1].text.strip() in valid]
        result.append(content)
    return result


MIN_HEADER_TEXT_OCCURENCE = 5  # TODO: HOLY VALUE


def header_content(clusters) -> set:
    """Some documents does not have any header, but equal sized first
    line(s). We have to ignore this first content lines."""
    collected = collections.defaultdict(int)
    for cluster in clusters:
        for item in cluster:
            text = item[1].text.strip()
            collected[text] += 1
    valid = {
        key for key, value in collected.items()
        if value >= MIN_HEADER_TEXT_OCCURENCE
    }
    return valid
