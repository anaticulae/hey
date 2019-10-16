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
import groupme.footer.serialize
import hey.textnavigator


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
    dumped = groupme.footer.serialize.dump_headerfooter(result)
    return dumped


def extract_footerheader(
        horizontals: iamraw.PagesWithHorizontalList,
        sizeandborders,
        pagenumbers,
        pagetextnavigators,
) -> typing.List[groupme.footer.PageContentFooterHeader]:
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

    result = judge_stategy(results)
    return result


def judge_stategy(results):
    count = [
        len([
            item.footer for item in result.values() if item.footer is not None
        ]) for result in results
    ]
    best_result = count.index(max(count)) if max(count) > 0 else -1
    if best_result >= 0:
        best_result = results[best_result].values()
        return best_result
    return []
