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
import configo
import iamraw
import texmex
import utila

import groupme.footer.strategy as gfs
import hey.classificator
import hey.textnavigator
import hey.textnavigator.fonts as htf

COMMON_HEADER_MAX_ERROR = 1.0  # TODO: HOLY VALUE
# minimal items in a cluster to be detected and accepted as feature.
MIN_CLUSTER_COUNT = configo.HV_INT_PLUS(5)
MIN_OCCURRENCE = 0.5
TOP_AREA = 0.15  # TODO: HOLY VALUE


class CommonTextStrategy(gfs.FooterHeaderDetectionStrategy):

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
    clusters = hey.classificator.common_items(
        collected=with_box,
        max_difference=COMMON_HEADER_MAX_ERROR,
        min_elements=min_cluster_count,
    )
    if not clusters:
        return []

    result = {}
    for cluster in clusters:
        for (page, (bounding, text, pageheight, pagenumber)) in cluster:
            end = utila.roundme(bounding.y1 / pageheight)
            try:
                result[pagenumber].append(iamraw.RawText(text=text))
                result[pagenumber].extend(end=end)
            except KeyError:
                # remove newline at end TODO: REMOVE LATER
                text = text.text.strip()
                header = iamraw.FixedHeaderInformation(
                    begin=texmex.START,
                    end=end,
                    page=iamraw.PageInformation(value=page, raw=None),
                    undefined=[iamraw.RawText(text=text)]  # pylint:disable=E1101
                )
                result[pagenumber] = header
    result = [(item, result[item]) for item in sorted(result.keys())]
    return result


def prepare_clustering(pagetextnavigators):
    textsize = htf.document_textsize(pagetextnavigators)
    result = []
    for page in pagetextnavigators:
        content = []
        for item in page.before(TOP_AREA):
            if item.style.textsize() == textsize:
                # TODO: FIND A BETTER FILTER
                continue
            content.append((item.bounding, item, page.height, page.page))
        result.append(content)
    return result
