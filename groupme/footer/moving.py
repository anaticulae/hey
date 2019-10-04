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

TODO: Think about header
"""
import groupme.footer
import hey.utils


class MovingFooterStrategy(groupme.footer.FooterHeaderDetectionStrategy):

    def result(self):
        result = {}

        for page in self.horizontals:
            sizeandborder = hey.utils.select_page(
                self.sizeandborders,
                page.page,
            )

            processed = process_page(
                page.page,
                page.content,
                sizeandborder,
            )

            if processed is not None:
                result[page.page] = (None, processed)
        return result


BOTTOM_BORDER = 0.75  # TODO: HOLY VALUE


def process_page(pagenumber, horizontals, sizeandborder):
    pageheight = sizeandborder.size.height

    bottom = pageheight * BOTTOM_BORDER
    filtered = [item for item in horizontals if item.box.y1 >= bottom]
    bottomed = max(
        [item.box.y1 for item in filtered],
        default=None,
    )
    return bottomed
