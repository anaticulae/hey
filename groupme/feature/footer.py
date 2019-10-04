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
import iamraw
import serializeraw
import utila

import groupme.footer
import groupme.footer.fixed
import groupme.footer.moving
import groupme.footer.pages


def work(horizontals: str, sizeandborders: str, pagenumbers: str) -> str:
    """Extract footer and header area out of horizontal lines

    Args:
        horizontals(str): path to file with extract lines
    Returns:
        dumped list with top and bottom border for every page
    """
    utila.call('footer')
    # load
    horizontals = serializeraw.load_horizontals(horizontals)
    sizeandborders = serializeraw.load_pageborders(sizeandborders)
    pagenumbers = serializeraw.load_pagenumbers(pagenumbers)

    # work
    result = extract_footerheader(
        horizontals,
        sizeandborders,
        pagenumbers,
    )

    # dump
    dumped = groupme.footer.dump_headerfooter(result)
    return dumped


def extract_footerheader(
        horizontals: iamraw.PagesWithHorizontalList,
        sizeandborders,
        pagenumbers,
) -> groupme.footer.FooterBorder:
    """Extract most common header/footer of the document

    Args:
        horizontals: a list of pages with a list of horizontals
    Return:
        the most common header/foooter combination for the document
    """

    strategies = [
        groupme.footer.fixed.FixedFooterStrategy,
        groupme.footer.moving.MovingFooterStrategy,
        groupme.footer.pages.PageNumberStrategy,
    ]
    results = [
        strategy(
            horizontals=horizontals,
            sizeandborders=sizeandborders,
            pagenumbers=pagenumbers,
        ).result() for strategy in strategies
    ]

    result = judge_stategy(results)
    return result


def judge_stategy(results):
    return results[0]
