# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
import texmex
import utila

import groupme.footer
import groupme.footer.strategy
import groupme.footer.strategy.common
import groupme.footer.strategy.fixed
import groupme.footer.strategy.moving
import groupme.footer.strategy.pages
import groupme.utils
import hey.utils


def work(
        text: str,
        text_positions: str,
        fontheader: str,
        fontcontent: str,
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
    fontstore = serializeraw.create_fontstore(fontheader, fontcontent, pages=pages) # yapf:disable
    horizontals = serializeraw.load_horizontals(horizontals, pages=pages)
    sizeandborders = serializeraw.load_pageborders(sizeandborders, pages=pages)
    pagenumbers = serializeraw.load_pagenumbers(pagenumbers, pages=pages)

    pagetextnavigators = texmex.create_pagetextnavigators(
        text,
        text_position,
        fontstore=fontstore,
    )
    # work
    result = extract_footerheader(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        pagenumbers=pagenumbers,
        pagetextnavigators=pagetextnavigators,
    )

    groupme.utils.validate(result)
    # dump
    dumped = serializeraw.dump_headerfooter(result)
    return dumped


def extract_footerheader(
        horizontals: iamraw.PagesWithHorizontalList,
        sizeandborders: iamraw.PageSizeBorderList,
        pagenumbers,
        pagetextnavigators: texmex.PageTextNavigators,
) -> iamraw.PageContentFooterHeaders:
    """Extract most common header/footer of the document

    Args:
        horizontals: a list of pages with a list of horizontals
    Return:
        the most common header/foooter combination for the document
    """
    strategies = groupme.footer.strategies()
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


def judge_strategy(results: typing.List[iamraw.PageContentFooterHeaders],
                  ) -> iamraw.PageContentFooterHeaders:
    """Decide which results fits best.

    Zip result of different strategies. Sometimes there are multiple
    options, therefore we have to use the priorities below.

    Sources/Concept:

        - MovingFooter:                footer (first prio)
        - Pages:                       footer (second prio)
        - FixedFooter:      header and footer (third prio)
        - Common:           header            (last prio)

    Args:
        results: lists of `groupme.footer.FooterHeaderDetectionStrategy`.result
    Returns:
        list of zipped result
    """
    assert results is not None, 'require list of strategy results'
    result = []
    for pagenumber, (
            common,
            fixed,
            moving,
            pages,
    ) in hey.utils.sync(results):
        header = fixed.header if fixed else None
        footer = fixed.footer if fixed else None

        if pages and pages.footer:
            footer = pages.footer

        if moving and moving.footer and moving.footer.notes:
            footer = moving.footer

        if not header and common and common.header:
            header = common.header

        current = iamraw.PageContentFooterHeader(
            header=header,
            footer=footer,
            page=pagenumber,
        )
        result.append(current)

    page_order = [item.page for item in result]
    assert sorted(
        page_order
    ) == page_order, f'require ascending pages order, got: {page_order}'
    return result


def judge_strategy_selective(results: iamraw.PageContentFooterHeaders
                            ) -> iamraw.PageContentFooterHeader:
    return None
