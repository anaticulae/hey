# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import texmex.navigator
import utila

import groupme.footer
import groupme.footer.strategy as gfs
import groupme.footer.strategy.moving as gfsm
import groupme.footer.strategy.pages as gfsp
import groupme.footnotes.highnotes
import groupme.footnotes.parser
import groupme.footnotes.plain


class PlainMovingFooterStrategy(gfs.FooterHeaderDetectionStrategy):

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
            if processed.footer is None:
                continue
            result.append(processed)

        result = gfsm.judge_detection(result)
        if disable_strategy(result):
            return []
        return result

    def report(self) -> gfs.FooterStrategyResultReport:
        # TODO: Avoid multiple computation, require  concept.
        detected = self.result()
        report = gfsm.analyze(detected)
        return report


BOTTOM_BORDER = 0.60  # TODO: HOLY VALUE

MAX_STRATEGY_ERROR = configo.HV_PERCENT_PLUS(10).value


def disable_strategy(footers) -> bool:
    """The plain moving strategy is only used in unique cases. Mostly
    this strategy detects uncompleted footnotes which are no valid
    footnotes. Therefore we require a strategy to disable these wrong
    results.

    It is not common to have many invalid footnotes. As a result of this
    fact, we disable this strategy if the errors are to high.
    """
    if not footers:
        return False
    nonumber_count = 0
    for page in footers:
        nonumber = [item for item in page.footer.notes if item.number < 0]
        if nonumber:
            nonumber_count += 1
    factor = nonumber_count / len(footers)
    return factor >= MAX_STRATEGY_ERROR


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
    if bottomed is not None:
        footer = extract_footer(
            bottomed,
            pageheight,
            pagenumber_location,
            pagetextnavigator,
        )

    result = iamraw.PageContentFooterHeader(
        header=None,
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
    # TODO: HOW TO HANDLE NON DETECTED PAGENUMBER_LOCATION
    end = pageheight
    if pagenumber_location and pagenumber_location.footer:
        end = pagenumber_location.footer.page_location.y0
    end = utila.roundme(end / pageheight)

    # TODO: USE TWO_THIRDS Strategy
    content = pagetextnavigator.between(
        begin,
        end,
        selector=texmex.navigator.SelectBounding.BOTTOM,
    )

    # TODO: INTRODUCE STRATEGY TO PARSE OTHER FOOTNOTES
    # splitted by highnotes
    footnotes = groupme.footnotes.plain.parse(content)
    footer = iamraw.MovingFooterInformation(
        begin=begin,
        end=end,
        notes=footnotes,
    )
    return footer
