# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This strategy aims to detect footer which contains only a page number
and distance to text before.

Example:
    docu/howto_argparse.pdf
    technical/page_24_color_figures_images.pdf

Extract page numbers as footer if the distance between page number and
next horizontal line is greater than `MIN_DISTANCE_TO_HORIZONTAL`.

"""
import dataclasses

import iamraw
import utila

import groupme.footer
import hey.textnavigator.navigator

MIN_DISTANCE_TO_HORIZONTAL = 50  # TODO: HOLY VALUE


@dataclasses.dataclass
class PagesFooterInformation(groupme.footer.FooterInformation):
    page_location: iamraw.BoundingBox = None


class PageNumberStrategy(groupme.footer.FooterHeaderDetectionStrategy):

    def result(self):
        result = []
        if isinstance(self.pagenumbers, tuple):
            assert len(self.pagenumbers) == 2, 'require left and right pages'
            left = self.process_pageside(self.pagenumbers[0])
            right = self.process_pageside(self.pagenumbers[1])
            result.extend(left)
            result.extend(right)
        else:
            result = self.process_pageside(self.pagenumbers)
        return result

    def process_pageside(self, pagenumbers):
        result = []
        pagenumbers = {item[0]: (item[1], item[2]) for item in pagenumbers}
        for page in self.sizeandborders:
            pdfpage = page.page
            pageheight = self.pageheight(pdfpage)
            assert pageheight > 0, f'invalid pageheight: {pageheight}'

            rawpage = utila.select_page(pagenumbers, pdfpage)
            horizontals = utila.select_page(self.horizontals, pdfpage)

            processed = process_page(pdfpage, rawpage, horizontals)
            if processed is not None:
                header = None

                begin = utila.roundme(processed[1].y0 / pageheight)
                end = hey.textnavigator.navigator.END
                footer = PagesFooterInformation(
                    begin=begin,
                    end=end,
                    page_location=processed[1],
                )
                footer_header = groupme.footer.PageContentFooterHeader(
                    header=header,
                    footer=footer,
                    page=pdfpage,
                )
                result.append(footer_header)
        return result


def process_page(page, rawpage, horizontals):
    if rawpage is None:
        return None
    pagenumber_bounding = rawpage[0]

    distance_to_firsthorizontal = distance(pagenumber_bounding, horizontals)
    if distance_to_firsthorizontal >= MIN_DISTANCE_TO_HORIZONTAL:
        return (page, pagenumber_bounding)
    return None


def distance(bounding, items):
    items = items.content if items else []
    bounding = bounding.y0
    ydistance = [bounding - item.box.y1 for item in items]

    result = min(ydistance, default=utila.INF)
    assert result >= 0, result
    return result


def pagenumber_location(
        horizontals,
        sizeandborders,
        pagenumbers,
        pagetextnavigators,
):
    strategy = PageNumberStrategy(
        horizontals,
        sizeandborders,
        pagenumbers,
        pagetextnavigators,
    )
    result = strategy.result()
    return result
