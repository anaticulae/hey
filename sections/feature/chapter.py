# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Find the starts of a chapter.

What is typical for a start of chapter?

* Mostly there is a space between header and title start
* There is a number/chapter number
* There is a huge font
* The title is listed in table of content


1. Locate the distance between first line and header
2. Check the second line

"""
import re
import typing

import iamraw
import serializeraw
import utila
import yaml

import hey.textnavigator.navigator


def work(document: str, position: str, tocpath: str, pages=None) -> str:
    """Determine likelihood of beeing a chapter startpage

    Args:
        document(str):
        position(str):
        tocpath(str):
        pages(list): list with page number to work on
    Returns:
        dumped list with ChapterLikelihood
    """
    # load and setup
    pages = tuple(pages) if pages else None
    document = serializeraw.load_document(document, pages=pages)
    position = serializeraw.load_textpositions(position, pages=pages)
    tocs = serializeraw.load_toc(tocpath)

    navigators = hey.textnavigator.navigator.create_pagetextnavigators(
        text=document,
        text_positions=position,
    )

    # work
    result = space_between_header_and_first_line(
        navigators=navigators,
        tocs=tocs,
    )

    # write result
    dumped = serializeraw.dump_likelihood(result)
    return dumped


FIRST_QUARTER = 0.35


def space_between_header_and_first_line(
        navigators: hey.textnavigator.navigator.PageTextNavigators,
        tocs,
) -> iamraw.PageContentLikelihoods:
    result = []
    for page in navigators:
        first_content = page.before(FIRST_QUARTER)
        chapter_rate = contain_chapter(first_content)
        chapter_rate += contain_toc(first_content, tocs)

        if is_tocpage(first_content):
            # TODO: See todo below
            chapter_rate = 0
        if chapter_rate <= 0.0:
            continue

        rate_in_percent = chaptervalue_to_percent(chapter_rate, tocs)

        result.append(
            iamraw.PageContentLikelihood(
                page=page.page,
                content=iamraw.Likelihood(rate_in_percent, 'chapter'),
            ))
        # TODO: There is the possiblity that header and start of chapter
        # are together, support later
        # result.append(0.0)
    return result


# We need only one number with dot, because we want only chapters, not
# sections etc.
NUMBER_PATTERN = re.compile(
    r'^'  # page start
    r'[0-9]{1,2}\.'  # chapter number with dot
    r'[ ]{1,4}'
    r'\D',  # non numeric element
    re.VERBOSE,
)


def contain_chapter(content):
    """Check if `content` contains elements which are hints that this
    content is part of the start of the chapter.

    A big hint is that the word `Kapitel` occurs on the start of the
    text. We have to keep in mind, that the sentence: 'Wie in Kapitel ..
    beschrieben' can occurs everywhere, therefore only searching the
    word is not a good approach. Only some works use this pattern.

    A second option is to look for the headline-pattern: '1. Einleitung'.
    """

    def startwith_chapterpattern(raw):
        firstline = raw.splitlines()[0] if raw else ''

        result = 'kapitel' in firstline or 'chapter' in firstline
        return result

    def startwith_firstlevelheadline(raw):
        # Search a number with possible dot
        matched = re.match(NUMBER_PATTERN, raw)
        return matched is not None

    raw = rawcontent(content)

    result = 0.0
    if startwith_chapterpattern(raw):
        result += 1.0
    if startwith_firstlevelheadline(raw):
        result += 0.5
    else:
        result -= 0.5

    return result


def is_tocpage(content):
    raw = rawcontent(content)
    dots = raw.count('.')

    result = dots > 20
    return result


def contain_toc(content, toc):
    flat_toc = [item.title for item in toc.children]
    if not flat_toc:
        # no table of content was extracted
        return 0
    flat_content = ' '.join([item.text for item in content])

    # is any toc title part of content
    toc_count = sum(item in flat_content for item in flat_toc)
    if 0 < toc_count <= 2:
        return 1.0
    return -0.5


def chaptervalue_to_percent(chaptervalue: float, hastoc: bool) -> float:
    """Convert `chaptervalue` to percent.

    Args:
        chaptervalue(float): value of detected features
        hastoc(bool): if no toc is provided, some features can not be
                       processed.
    """
    # TODO: HOLY VALUES
    # TODO: IMPROVE THIS CONCEPT
    if not hastoc and chaptervalue >= 1.0:
        return 1.0
    if chaptervalue >= 2.5:
        return 1.0
    if chaptervalue >= 0.5:
        return 0.5
    return 0.0


def rawcontent(content) -> str:
    raw = utila.NEWLINE.join([item.text for item in content])
    raw = raw.lower()
    return raw


def dump_chapter_detection(pages: typing.List[float]) -> str:
    result = []
    for index, chapter in enumerate(pages):
        result.append({
            'page': index,
            'chapter': '%.2f' % chapter,
        })
    return yaml.dump(result)
