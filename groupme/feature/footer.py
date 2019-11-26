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
import typing

import iamraw
import serializeraw
import utila

import groupme.footer
import groupme.footer.fixed
import groupme.footer.moving
import groupme.footer.pages
import hey.textnavigator
import hey.textnavigator.navigator
import hey.utils


def work(
        text: str,
        text_positions: str,
        horizontals: str,
        sizeandborders: str,
        pagenumbers: str,
        pages=None,
) -> str:
    """Extract footer and header area out of horizontal lines

    Args:
        horizontals(str): path to file with extract lines
    Returns:
        dumped list with top and bottom border for every page
    """
    utila.call('footer')
    # load
    text = serializeraw.load_document(text, pages=pages)
    text_position = serializeraw.load_textpositions(text_positions, pages=pages)
    horizontals = serializeraw.load_horizontals(horizontals, pages=pages)
    sizeandborders = serializeraw.load_pageborders(sizeandborders, pages=pages)
    pagenumbers = serializeraw.load_pagenumbers(pagenumbers, pages=pages)

    pagetextnavigators = hey.textnavigator.navigator.create_pagetextnavigators(
        text,
        text_position,
    )
    # work
    result = extract_footerheader(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        pagenumbers=pagenumbers,
        pagetextnavigators=pagetextnavigators,
    )

    # dump
    dumped = serializeraw.dump_headerfooter(result)
    return dumped


def extract_footerheader(
        horizontals: iamraw.PagesWithHorizontalList,
        sizeandborders: iamraw.PageSizeBorderList,
        pagenumbers,
        pagetextnavigators: hey.textnavigator.navigator.PageTextNavigators,
) -> groupme.footer.PageContentFooterHeaders:
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
            pagetextnavigators=pagetextnavigators,
        ).result() for strategy in strategies
    ]

    result = judge_strategy(results)
    return result


def judge_strategy(
        results: typing.List[groupme.footer.PageContentFooterHeaders],
) -> groupme.footer.PageContentFooterHeaders:
    """Decide which results fits best.

    Zip result of different strategies. Sometimes there are multiple
    options, therefore we have to use the priorities below.

    Sources/Concept:

        - MovingFooter:                footer (first prio)
        - Pages:                       footer (second prio)
        - FixedFooter:      header and footer (third prio)

    Args:
        results: lists of `groupme.footer.FooterHeaderDetectionStrategy`.result
    Returns:
        list of zipped result
    """
    assert results is not None, 'require list of strategy results'
    result = []
    for pagenumber, (fixed, moving, pages) in hey.utils.sync(results):
        header = fixed.header if fixed else None
        footer = fixed.footer if fixed else None

        if pages and pages.footer:
            footer = pages.footer

        if moving and moving.footer and moving.footer.notes:
            footer = moving.footer

        current = iamraw.PageContentFooterHeader(
            header=header,
            footer=footer,
            page=pagenumber,
        )
        result.append(current)
    return result


def judge_strategy_selective(
        results: typing.List[groupme.footer.PageContentFooterHeaders],
) -> groupme.footer.PageContentFooterHeaders:
    return None
