# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import operator
# TODO: MOVE TO TEXMEX
import re

import texmex
import utila

import sections.utils.spa
import words.text.word

MIN_LIKELIHOOD = 0.3  # TODO: HOLY VALUE


def work(document: str, position: str, pages=None) -> str:
    data = sections.utils.spa.Data(
        document=document,
        position=position,
        pages=pages,
    )

    config = sections.utils.spa.Config(
        likelihood_name='bibliography_table',
        page_analysis=analyse_page,
    )

    dumped = sections.utils.spa.work(
        data=data,
        config=config,
    )

    return dumped


def analyse_page(navigator: texmex.PageTextNavigator
                ) -> sections.feature.StatisticalResultItem:
    raw = ' '.join([line.text for line in navigator])
    collected = []
    for method in [years, dates, pages]:
        collected.extend(method(raw))

    marker = len(collected)
    if special_chars(raw):
        # thirty percent bonus
        marker *= 1.3  # TODO: HOLY VALUE
    likelihood = len(navigator) / marker if marker else 0.0
    if likelihood < MIN_LIKELIHOOD:
        # TODO: CHECK THIS
        # this can not be a bib table
        marker = 0
    return len(navigator), marker


def special_chars(raw: str) -> list:
    # TODO: A LOT OF MISMATCHES AS A RESULT OF PROGRAM CODE IN DOCUMENT
    result = []
    for line in raw.splitlines():
        parsed = words.text.word.split_words(line, validate_sentences=False)
        result.extend(parsed)
    counted = raw.count(';') + raw.count(',') + raw.count('/') + raw.count(':')
    counted += raw.count('[') + raw.count(']') + raw.count(')') + raw.count('(')

    word_count = len(result)
    classifier = counted / word_count if word_count else 0
    if word_count > 40 and classifier > 0.3:  # TODO HOLY VALUE
        return True
    return False


def years(raw: str, min_=1950, max_=2020):
    """Extract sorted list of years out of `raw` text.

    >>> years('1999, Helm is born in 1987. Mud exists since 1800. 2050 20000 2020')
    [1987, 1999, 2020]
    """
    result = []
    pattern = r'\b(19|20)\d{2}\b'
    for item in re.finditer(pattern, raw):
        item = utila.extract_match(item)
        year = int(item)
        if min_ <= year <= max_:
            result.append(year)
    result = sorted(result)
    return result


def dates(raw: str, min_year=1950, max_year=2020):
    """Extract sorted list of dates out of `raw` text.

    >>> dates('Stand 20.10.2020, (15.11.2014), 01.01.1999 01.01.1940')
    [(1999, 1, 1), (2014, 11, 15), (2020, 10, 20)]
    """
    result = []
    pattern = r'(\d{1,2})\.(\d{1,2})\.(\d{4})'
    for item in re.findall(pattern, raw):
        day, month, year = item
        day, month, year = int(day), int(month), int(year)
        if not 1 <= day <= 31:
            continue
        if not 1 <= month <= 12:
            continue
        if not min_year <= year <= max_year:
            continue
        result.append((year, month, day))
    result = sorted(result, key=operator.itemgetter(0, 1, 2))
    return result


def pages(raw: str):
    """Extract single pages and page ranges out of `raw` text.

    >>> pages('S. 13-50 S.30 S. 1-5 S.319-350, Seite 20-30., page 500 p.4')
    [(1, 5), (4, 4), (13, 50), (20, 30), (30, 30), (319, 350), (500, 500)]
    """
    result = []
    pattern = r"""(S|S\.|Seite|p|p\.|page)
                [ ]{0,4}
                (
                    (?P<pstart>\d{1,4})[ ]{0,2}\-[ ]{0,2}(?P<pend>\d{1,4})|
                    (?P<page>\d{1,4})
                )
               """
    for item in re.finditer(pattern, raw, re.VERBOSE):
        try:
            # single page
            pstart = int(item['page'])
            result.append((pstart, pstart))
        except TypeError:
            # from page start till page end
            pstart = int(item['pstart'])
            pend = int(item['pend'])
            result.append((pstart, pend))
    result = sorted(result, key=operator.itemgetter(0))
    return result
