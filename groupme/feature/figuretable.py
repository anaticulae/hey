# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of figures extractor
==========================
"""

import configo
import serializeraw
import texmex
import utila

import groupme.toc.extractor
import groupme.toc.group
import groupme.toc.strategy

# minimal percentage of figure lines per page
MIN_TOFS_PER_PAGE = configo.HV_PERCENT_PLUS(0.2, limit=1.0).value


def work(
        text: str,
        textpositions: str,
        oneline_text: str,
        oneline_textpositions: str,
        headerfooter: str,
        sizeandborder: str,
        pages: tuple = None,
) -> str:
    """Extract table of figures out of `document`.

    Args:
        text(str): path to load document
        textpositions(str): path to load document textpositions
        oneline_text(str): oneline document
        oneline_textpositions(str): oneline document positions
        headerfooter(str): path with header and footer to determine
                           content border.
        sizeandborder(str): path with page sizes and content border
        pages(tuple): tuple of selected pages
    Returns:
        dump of extracted table of content
    """
    oneline = serializeraw.create_pagetextcontentnavigators_fromfile(
        oneline_text,
        oneline_textpositions,
        sizeandborderpath=sizeandborder,
        headerfooterpath=headerfooter,
        pages=pages,
    )
    selected = select_figuretable(oneline)
    # select toc pages only
    oneline = utila.select_pages(oneline, pages=selected)

    loaded = groupme.toc.strategy.load(oneline)
    extracted = groupme.toc.extractor.extract(loaded)

    flat = utila.flatten(extracted.content)
    leveled = groupme.toc.group.groupby_level(flat)

    dumped = serializeraw.dump_toc(leveled)
    return dumped


NO_FIGURES = {
    'Abkürzungsverzeichnis',
    'Inhalt',
    'Inhaltsverzeichnis',
    'Tabellenverzeichnis',
}


def select_figuretable(
        textnavigators: texmex.PageTextNavigators,
        wrong_table=None,
) -> utila.Ints:
    """Use simple approach to decide which page is a figure table page."""
    if wrong_table is None:
        wrong_table = NO_FIGURES
    selected = []
    for page in textnavigators:
        firstheadline = headline(page)
        if firstheadline is not None and firstheadline in wrong_table:
            # This approach works only forward and not backwards.
            # TODO: WHAT SHOULD WE DO WHEN BOTH ARE ON THE SAME PAGE?
            continue
        utila.debug(f'page: {page.page}')
        figurepage = groupme.toc.strategy.regex.parse_page(page)
        if figurepage is None:
            utila.log(f'empty page: {page.page}')
            continue

        level3 = [groupme.toc.group.level(item.level) for item in figurepage]
        level3 = [
            item for item in level3
            if item and isinstance(item.value, int) and item.value >= 3
        ]
        if any(level3):
            # TODO: THINK ABOUT THIS
            # level is mostly a table of content level
            continue
        pageslines = texmex.count_textlines(page, remove_empty=True)
        if not pageslines:
            continue
        figure_percent = len(figurepage) / pageslines
        utila.info(f'toc percent: {figure_percent} on page: {page.page}')
        if figure_percent < MIN_TOFS_PER_PAGE:
            # avoid missdetection in random pages if only few lines are
            # missdetected as toc line.
            continue
        selected.append(page.page)
    selected = sorted(utila.make_unique(selected))
    return selected


def headline(page):
    result = []
    for item in page:
        parsed = groupme.toc.strategy.regex.parse(item.text)
        if parsed:
            continue
        # TODO: REPLACE AFTER FIXING TEXMEX
        # most item is more robust than max item
        textsize = utila.flatten(
            [[item.size] * (item.end - item.start) for item in item.style])
        textsize = utila.mode(textsize)
        if textsize < 15.0:  # TODO: HOLY VALUE
            continue
        result.append(item.text.strip())
    if not result:
        return None
    if len(result) > 1:
        return None
    return result[0]
