# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Requirements:
    We do not check the header, because it is required, that this header
    is fixed.

Example:
    master/page_72_noimages_toc.pdf
    bachelor/page_111_images_toc.pdf

TODO: Think about header
"""
import iamraw
import utila

import groupme.footer
import groupme.footer.footnotes
import groupme.footer.pages


class MovingFooterStrategy(groupme.footer.FooterHeaderDetectionStrategy):

    def result(self):
        result = []

        pagenumber_locations = groupme.footer.pages.pagenumber_location(
            self.horizontals,
            self.sizeandborders,
            self.pagenumbers,
            self.pagetextnavigators,
        )

        for page in self.horizontals:
            sizeandborder = utila.select_page(
                self.sizeandborders,
                page.page,
            )
            pagetextnavigator = utila.select_page(
                self.pagetextnavigators,
                page.page,
            )
            pagenumber_location = utila.select_page(
                pagenumber_locations,
                page.page,
            )

            processed = process_page(
                pagenumber=page.page,
                pagenumber_location=pagenumber_location,
                horizontals=page.content,
                sizeandborder=sizeandborder,
                pagetextnavigator=pagetextnavigator,
            )
            result.append(processed)

        return result


BOTTOM_BORDER = 0.60  # TODO: HOLY VALUE


def process_page(
        pagenumber,
        pagenumber_location,
        horizontals,
        sizeandborder,
        pagetextnavigator,
):
    pageheight = sizeandborder.size.height

    footer_start = pageheight * BOTTOM_BORDER
    filtered = [item for item in horizontals if item.box.y1 >= footer_start]
    bottomed = max(
        [item.box.y1 for item in filtered],
        default=None,
    )
    footer = None
    header = None

    if bottomed is not None:
        footer = extract_footer(
            bottomed,
            pageheight,
            pagenumber_location,
            pagetextnavigator,
        )

    result = iamraw.PageContentFooterHeader(
        header=header,
        footer=footer,
        page=pagenumber,
    )

    return result


def extract_footer(
        footerstart: float,
        pageheight: int,
        pagenumber_location,
        pagetextnavigator,
):
    begin = footerstart / pageheight
    # in the current parser state, the location of tiny distances between
    # objects is not interpreted correctly. The distance is often to small.
    # TODO: Remove after improving layout parser
    begin = begin - 0.03
    begin = utila.roundme(begin)

    # TODO: HOW TO HANDLE NON DETECTED PAGENUMBER_LOCATION
    end = pageheight
    if pagenumber_location and pagenumber_location.footer:
        end = pagenumber_location.footer.page_location.y0
    end = utila.roundme(end / pageheight)

    content = pagetextnavigator.between(begin, end)
    content = footercontent(content)

    footnotes = groupme.footer.footnotes.parse(content)

    footer = iamraw.MovingFooterInformation(
        begin=begin,
        end=end,
        notes=footnotes,
    )
    return footer


def footercontent(items):
    content = [item[1] for item in items]
    content = utila.NEWLINE.join(content)
    return content
