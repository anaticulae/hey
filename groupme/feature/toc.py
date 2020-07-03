# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of content extractor
==========================

Outdated approaches
-------------------

- collect title and check if sequence exists again in the document

"""

import configo
import serializeraw
import texmex
import utila

import groupme.feature
import groupme.toc
import groupme.toc.extractor
import groupme.toc.strategy
import groupme.utils

# minimal percentage of toc lines per page
MIN_TOCS_PER_PAGE = configo.HV_PERCENT_PLUS(0.2, limit=1.0).value

# limit possible toc to the first 15 pages
POSSIBLE_PAGES = utila.make_tuple(15)


def work(
        text: str,
        textpositions: str,
        headerfooter: str,
        sizeandborder: str,
        pages: tuple = None,
) -> str:
    """Extract table of content out of `document`.

    Args:
        text(str): path to load document
        textpositions(str): path to load document textpositions
        headerfooter(str): path with header and footer to determine
                           content border.
        sizeandborder(str): path with page sizes and content border
        pages(tuple): tuple of selected pages
    Returns:
        dump of extracted table of content
    """
    navigators = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textpositions,
        sizeandborderpath=sizeandborder,
        headerfooterpath=headerfooter,
        pages=pages,
    )
    selected = select_tocpages(navigators)
    # select toc pages only
    navigators = utila.select_pages(navigators, pages=selected)

    loaded = groupme.toc.strategy.load(navigators)
    extracted = groupme.toc.extractor.extract(loaded)

    flat = utila.flatten(extracted.content)
    leveled = groupme.toc.group.groupby_level(flat)

    dumped = serializeraw.dump_toc(leveled)
    return dumped


def select_tocpages(textnavigators: texmex.PageTextNavigators) -> utila.Ints:
    """Use simple approach to decide which page is a toc page."""
    selected = []
    for page in textnavigators:
        if utila.should_skip(page.page, POSSIBLE_PAGES):
            continue
        utila.debug(f'page: {page.page}')
        tocpage = groupme.toc.strategy.regex.parse_page(page)
        if tocpage is None:
            utila.log(f'empty page: {page.page}')
            continue
        pageslines = texmex.count_textlines(page, remove_empty=True)
        if not pageslines:
            continue
        tocpage = decide_non_level_possible_headlines(tocpage)
        if not tocpage:
            # after filtering, no toc line is left
            continue
        toc_percent = len(tocpage) / pageslines
        utila.info(f'toc percent: {toc_percent} on page: {page.page}')
        if toc_percent < MIN_TOCS_PER_PAGE:
            # avoid missdetection in random pages if only few lines are
            # missdetected as toc line.
            continue
        selected.append(page.page)
    selected = sorted(utila.make_unique(selected))
    return selected


# TODO: THIS IS STOLEN FROM WORDS
WHITELIST = set([
    'Anhang',
    'Eidesstattliche Erklärung',
    'Literaturverzeichnis',
])


def decide_non_level_possible_headlines(items):
    """Decide level for toc lines without 1.2.3-pattern in table of content

    Use a whitelist to detect which line could be a headline."""
    result = []
    for item in items:
        if item.level is None:
            if not item.title in WHITELIST:
                # remove items which are not part of the white list
                utila.info(f'skip potential headline: {item.title}')
                continue
            item = groupme.toc.TocLine(
                level='1',
                title=item.title,
                page=item.page,
                raw=item.raw,
            )
        result.append(item)
    return result
