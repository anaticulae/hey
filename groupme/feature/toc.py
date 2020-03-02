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

import iamraw
import serializeraw
import texmex
import utila

import groupme.feature
import groupme.structure
import groupme.toc
import groupme.toc.extractor
import groupme.toc.loader
import groupme.toc.strategy
import groupme.toc.strategy.regex as gtsr
import groupme.utils
import words.headlines

MIN_TOCS_PER_PAGE = 0.2  # TODO: HOLY VALUE


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
    navigators = [item for item in navigators if item.page in selected]
    # TODO: REPLACE WITH UTILA CODE
    # navigators = utila.select_page(
    #     navigators,
    #     page=selected,
    # )

    loaded = groupme.toc.strategy.load(navigators)
    extracted = groupme.toc.extractor.extract(loaded)

    flat = utila.flatten(extracted.content)
    leveled = groupby_level(flat)

    dumped = serializeraw.dump_toc(leveled)
    return dumped


Level = str
Title = str

LeveledTitle = typing.Tuple[Level, Title]
LeveledTitles = typing.List[LeveledTitle]


def select_tocpages(
        textnavigators: texmex.PageTextNavigators) -> typing.List[int]:
    """Use simple approach to decide which page is a toc page."""
    selected = []
    for page in textnavigators:
        utila.debug('page: {page.page}')
        tocpage = gtsr.parse_page(page)
        if tocpage is None:
            utila.log(f'empty page: {page.page}')
            continue
        tocpage = decide_non_level_possible_headlines(tocpage)

        if not tocpage:
            # after filtering, no toc line is left
            continue

        pageslines = groupme.utils.count_textlines(page, remove_empty=True)
        toc_percent = len(tocpage) / pageslines
        if toc_percent < MIN_TOCS_PER_PAGE:
            # avoid missdetection in random pages if only few lines are
            # missdetected as toc line.
            continue
        selected.append(page.page)
    return set(selected)


def decide_non_level_possible_headlines(items):
    """Decide level for toc lines without 1.2.3-pattern in table of content

    Use a whitelist to detect which line could be a headline.
    """
    result = []
    for item in items:
        if item.level is None:
            if not item.title in words.headlines.WHITELIST:
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


def filter_common_headlines(potential_titles: LeveledTitles) -> LeveledTitles:
    """

    In some cases it is possible that mostly equal titles are extracted. That
    is possible when the title in the document differ from the title in the table
    of content. An another possiblity is that titles from footer or header are
    a little bit different.

    Example:
       ('4.1', 'Step 1')    - uniformed title
       ('4.1.', 'Step 1')   - different title
       ('4.2', 'Step 2')    - uniformed title
       ('4.2.', ' Step 2 ') - different title

    This method removes the `different title`.

    Args:
        potential_titles(List[Tuple[Level, Title]]): title to filter
    Returns:
        filtered uniformed title and level, without duplications
    """
    result = []
    used = set()
    for level, title in potential_titles:
        uniformed_level = uniform_level(level)
        striped_title = title.strip()

        uniformed = (
            uniformed_level,
            striped_title,
        )
        # TODO: Remove unified and save the un-unified
        if uniformed in used:
            # Title is already present
            continue
        used.add(uniformed)
        result.append(uniformed)
    return result


def text_snippets(document: iamraw.Document):
    result = []
    for page in document:
        for item in page:
            try:
                # TODO: Why strip?
                result.append(item.text.strip())
            except AttributeError:
                pass
    return result


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
        section = iamraw.Section(
            level=level,
            page=line.page,
            raw=line.raw,
            title=line.title,
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


def is_dotted_line(line: str):
    return line.count(' .') > 2 or line.count('...') > 2


def toc_from_page(page: iamraw.Page) -> typing.List[groupme.feature.RawSection]:
    """Extract headlines from page"""
    page_sections = groupme.structure.sections_from_page(page)
    if not page_sections:
        # Empty page
        return None

    result = []
    # Filter non toc items, very simple rules!
    for index, item in enumerate(page_sections, start=0):
        if not item.title or not item.level:
            continue

        if item.title.count(utila.NEWLINE) > 1:
            continue

        if is_dotted_line(item.title):
            result.append(index)
            continue

        # if len(item.title) > 120:
        #     continue

        result.append(index)
    if not result:
        # TODO: No data on page ?
        return []
    group = group_segmentation(result)
    longest = [page_sections[index] for index in longest_group(group)]
    filtered = [(item.level, strip_title(item.title)) for item in longest]
    return filtered


def group_segmentation(items, max_diff: int = 0):
    """A group is a list of items which stand direct together. A gab of
    max_diff is tollerated

    Example:
        5,6,7,             11,12,13,    19     max_diff 0  - 3 groups
        5,6,7,11,12,13,    19                  max_diff 4  - 2 groups
    """
    result = []
    collect = []
    last = 1000
    for item in items:
        diff = abs(last - item) - 1  # 6-5 = 1, 1 is no diff, it is next number
        if diff > max_diff:
            if collect:
                result.append(collect)
                collect = []
        last = item
        collect.append(item)
    if collect:
        result.append(collect)
    return result


def longest_group(groups):
    size = 0
    longest = None
    for group in groups:
        if len(group) > size:
            longest = group
            size = len(longest)
    return longest


def strip_title(title: str):
    """Remove ... in toc lines"""
    # split ...? .. ....
    return title.split(' .')[0]


def filter_double(items):
    """Return items which occurs twice"""
    result = []
    last = set()
    for item in items:
        before = len(last)
        last.add(item)
        if len(last) == before:
            result.append(item)
    return result


def name():
    return 'toc'


def commandline():
    return utila.Flag(
        longcut=name(),
        message='extract table of content',
    )
