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
import typing

import configo
import iamraw
import serializeraw
import texmex
import utila

import groupme.feature
import groupme.toc
import groupme.toc.extractor
import groupme.toc.loader
import groupme.toc.strategy
import groupme.toc.strategy.regex as gtsr
import groupme.utils

# minimal percentage of toc lines per page
MIN_TOCS_PER_PAGE = configo.HV_PERCENT_PLUS(0.2, limit=1.0).value


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
    navigators = groupme.toc.loader.load(
        text,
        textpositions,
        headerfooter,
        sizeandborder,
        pages=pages,
    )
    selected = select_tocpages(navigators)
    # select toc pages only
    navigators = utila.select_pages(navigators, pages=selected)

    loaded = groupme.toc.strategy.load(navigators)
    extracted = groupme.toc.extractor.extract(loaded)

    flat = utila.flatten(extracted.content)
    leveled = groupby_level(flat)

    dumped = serializeraw.dump_toc(leveled)
    return dumped


Level = typing.NewType('Level', str)
Title = typing.NewType('Title', str)

LeveledTitle = typing.Tuple[Level, Title]
LeveledTitles = typing.List[LeveledTitle]


def select_tocpages(textnavigators: texmex.PageTextNavigators) -> utila.Ints:
    """Use simple approach to decide which page is a toc page."""
    selected = []
    for page in textnavigators:
        utila.debug(f'page: {page.page}')
        tocpage = gtsr.parse_page(page)
        if tocpage is None:
            utila.log(f'empty page: {page.page}')
            continue
        tocpage = decide_non_level_possible_headlines(tocpage)

        if not tocpage:
            # after filtering, no toc line is left
            continue
        pageslines = texmex.count_textlines(page, remove_empty=True)
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


def uniform_level(level: str) -> str:
    """Uniform potential level

    The valid level format according to DUDEN is X.Y.Z without trailing `.`

    Example:
        1.3.3. - > 1.3.3
        TODO: make upper/lower of ROMAN level iii -> III ? - decide later
    Args:
        level(str): level to unify
    Returns:
        unified level
    """
    assert level
    level = str(level)
    if level.endswith('.'):
        level = level[0:-1]
    return level


def groupby_level(tableofcontent: groupme.toc.TocLines) -> iamraw.Toc:
    """Create `iamraw.Toc` out of list of `groupme.toc.TocLine

    Determine level of toc line and replace it with determined int-level.

    Args:
        tableofcontent: extracted table of content.
    Returns:
        Table of content with replaced levels.`
    """
    assert isinstance(tableofcontent, list), type(tableofcontent)

    def determine_level(level):
        if level is None:
            return 0
        # 1. Einleitung
        # 1.1 Aufbau der Arbeit
        number = level.count('.')  # TODO: NOT VERY STABLE
        if level.endswith('.') and len(level) > 1:
            number = number - 1
        return number

    outlines = []
    for line in tableofcontent:
        if not line:
            utila.error(f'problem while processing lines: {line}')
            continue
        if not isinstance(line, groupme.toc.TocLine):
            continue
        level = determine_level(line.level)
        section = iamraw.SectionRaw(
            level=level,
            page=line.page,
            title=line.title,
            raw=line.raw,
            raw_location=line.raw_location,
        )
        outlines.append(section)

    def level_zero(items):
        """Ensure that no toc has level zero

        Problem:
            1 Einleitung
            1.1 Aufbau der Arbeit
            update every level to ensure
        """
        zero_level = min([item.level for item in items], default=utila.INF) == 0
        if zero_level:
            for item in items:
                item.level = item.level + 1
        return items

    outlines = level_zero(outlines)
    result = iamraw.create_toc(outlines)
    return result
