# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Requirements:
    We do not check the header, because it is required, that this header
    is fixed.

Example:

- master/page_72_noimages_toc.pdf
- bachelor/page_111_images_toc.pdf

TODO: Think about header
"""
import dataclasses

import configo
import iamraw
import utila

import groupme.footer
import groupme.footer.strategy as gfs
import groupme.footer.strategy.pages as gfsp
import groupme.footnotes.highnotes
import groupme.footnotes.parser


class MovingFooterStrategy(gfs.FooterHeaderDetectionStrategy):

    def result(self):
        result = []

        pagenumber_locations = gfsp.pagenumber_location(
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
            if processed.footer is None and processed.header is None:
                continue
            result.append(processed)

        result = judge_detection(result)
        return result

    def report(self) -> gfs.FooterStrategyResultReport:
        # TODO: Avoid multiple computation, require  concept.
        detected = self.result()
        report = analyze(detected)
        return report


@dataclasses.dataclass
class MovingFooterResultReport(gfs.FooterStrategyResultReport):  # pylint:disable=R0903
    footer: int = None
    header: int = None
    footer_empty: int = None
    too_many_empty_footer: bool = False


# relation between detected and empty detected footer to reduce miss detection
WRONG_STRATEGY_EMPTY_FOOTER_FACTOR = configo.HV_PERCENT_PLUS(default=20,).value

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
    filtered = [item for item in horizontals if item.box.y0 >= footer_start]
    bottomed = max([item.box.y0 for item in filtered], default=None)

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
    begin = begin - 0.0515  # TODO: HOLY VALUE
    begin = utila.roundme(begin)

    # TODO: HOW TO HANDLE NON DETECTED PAGENUMBER_LOCATION
    end = pageheight
    if pagenumber_location and pagenumber_location.footer:
        end = pagenumber_location.footer.page_location.y0
    end = utila.roundme(end / pageheight)

    content = pagetextnavigator.between(begin, end)

    # TODO: INTRODUCE STRATEGY TO PARSE OTHER FOOTNOTES
    # split by highnotes
    footnotes = groupme.footnotes.parser.parse_with_highnotes(content)
    if not footnotes:
        # no footnotes parsed, therefore do not return MovingFooterInformation
        return None
    footer = iamraw.MovingFooterInformation(
        begin=begin,
        end=end,
        notes=footnotes,
    )
    return footer


def analyze(results) -> MovingFooterResultReport:
    footer_count = gfs.count_footer(results)
    emptyfooter_count = groupme.footnotes.parser.count_empty(results)
    empty_factor = emptyfooter_count / footer_count if footer_count else 0
    too_many_empty_footer = empty_factor >= WRONG_STRATEGY_EMPTY_FOOTER_FACTOR

    result = MovingFooterResultReport(
        footer=footer_count,
        footer_empty=emptyfooter_count,
        too_many_empty_footer=too_many_empty_footer,
    )
    return result


def judge_detection(items):
    """Second analyzing step. Prove that `items` contain a good
    detection result.

    The following things will be checked:

    - (x) selection of correct strategy
    - ( ) quality of extracted footnotes
    """
    report = analyze(items)

    # This can happen when using the wrong strategy. If we parse
    # FixedFooter with MovingFooterStrategy, there are a lot of footer
    # which are threated as MovingFooter with Footnote, but this detection
    # is not correct.
    if report.too_many_empty_footer:
        return []

    return items


def footercontent(items):
    """
    Args:
        items(list): list of (bounds, text)
    """
    content = [item.text for item in items]
    content = utila.NEWLINE.join(content)
    return content
