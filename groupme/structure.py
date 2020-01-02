# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re
import typing

import utila
from iamraw import Document
from iamraw import Page

import groupme.feature
import groupme.feature.toc
from groupme.feature import HEADLINE
from groupme.feature import create_raw

SMALL_HEADER = 300

# TODO: WE NEED A STRATEGY APPROACH, split different types of
# headlines/table of contents.


def header(document: Document) -> str:
    """Extract header out of document content

    The header starts at the top of the document and ends with the start of the
    content. The start of the content is the first headline.
    """
    tableofcontent = groupme.feature.toc.toc(document)
    if not tableofcontent:
        # No toc in document
        return None
    # Split content from header due first headline
    # TODO: This is very dirty here
    level, title = tableofcontent[0][0], tableofcontent[0][1]
    text = document.text

    def split_header(text, title, level):
        splitted = split_headline(text, title, level)

        if len(splitted) == 3:
            title_ = groupme.feature.format_title(tableofcontent[0])
            splitted = [splitted[0] + title_ + splitted[1], splitted[2]]

        # TODO: IMPROVE OR REMOVE
        utila.error(f'wrong split: {title}')
        return splitted

    splitted = split_header(text, title, level)

    # TODO: We need a better algorithm/ strategy approach
    # Splitting with level splits sometimes in the table of content. This
    # happens, if the headlines in the document have a different style
    # than in the table of content. For example when using
    # "Chapter\nHeadline" instead of "1.2.3 Headline". Therefore we trying
    # to split header without level marker.
    header_tosmall = len(splitted[0]) < SMALL_HEADER
    if header_tosmall:
        # try without `headline level` again
        splitted = split_header(text, title, '')

    assert len(splitted[0]) > SMALL_HEADER, splitted[0]  # front page, toc etc.
    return splitted[0]


def body(document: Document) -> str:
    header_ = header(document)
    text = document.text
    result = text.split(header_)[1]
    return result


def split_headline(text, title, level):
    level = level.replace('.', r'\.')
    headline = re.compile(
        '^%s[ ]{0,3}%s[ ]{0,3}$' % (level, title),
        re.MULTILINE,
    )
    splitted = re.split(
        headline,
        text,
    )
    return splitted


def sections(document: Document) -> typing.List[str]:
    """Determine `sections` from `Document`"""
    result = []
    for page in document.pages:
        result.extend(sections_from_page(page))
    return result


def sections_from_page(page: Page) -> typing.List[str]:
    """Parse headline due regex `HEADLINE` from `Page

    Args:
        page(Page): one page of `Document`
    Returns:
        List[str] of potential headlines
    """
    result, headline, text = [], None, []
    for line in page.text.splitlines():
        parsed = parse_headline(line)
        if parsed:
            if text or headline:
                result.append(create_raw(headline, text))
            headline = parsed
            text = []
        else:
            text.append(line)
    if text:
        result.append(create_raw(headline, text))
    return result


def parse_headline(line: str):
    """Extract potential headline from str

    Use regex to determine headlines with level in document from random text.
    In some cases this will not work, for example:

    ```
        CHAPTER 3
        RestructuredText Customizations
    ```

    Args:
        line(str): random text line of document
    Returns
        (level, title): return potential level/depth and title of headline
    """
    assert isinstance(line, str)
    matched = re.match(HEADLINE, line)
    if not matched:
        return None
    level = matched['level']
    if len(level) <= 2 and level[0].islower():
        return None
    return (level, matched['title'])
