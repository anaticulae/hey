#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""How to extract text blocks out of the text and chapter structure

    1. Split the whole content by headlines into seprate blocks
        1.a. Skip non text blocks
    2.

"""
from dataclasses import dataclass
from re import match
from typing import List
from typing import Tuple

from iamraw import Document
from iamraw import Page
from iamraw import Section
from iamraw import Toc
from iamraw import create_toc
from serializeraw import dump_toc
from serializeraw import load_document
from utila import NEWLINE
from utila import file_read
from yaml import dump

HEADLINE = (r'^(?P<level>([\d|I|a|b|c]+\.?)+)'
            r'[ ]+'
            r'(?P<title>[\w]+[\w| |\d|\.|&]+)$')

Level = str
Text = str
Title = Tuple[Level, Text]


@dataclass
class RawSection:
    """Section with title(level,title) and content(text)"""
    title: str = ''
    text: str = ''
    level: str = None


def format_title(title: Title) -> str:
    """Convert title to str"""
    return title[0] + ' ' + title[1]


def header(document: Document) -> str:
    tableofcontent = toc(document)
    # Split content from header due first headline
    first_headline = format_title(tableofcontent[0])
    splitted = document.text.rsplit(first_headline, 1)
    assert len(splitted[0]) > 300  # front page, toc etc.
    return splitted[0]


def content(document: Document) -> str:
    header_ = header(document)
    result = document.text.split(header_)[1]
    return result


def chapter(path: str):
    """Extract chapter structure from document path"""
    # toc: Toc = load_toc(toc_path)
    document: Document = load_document(file_read(path))

    tableofcontent = toc(document)
    documentheader, _content = header(document), content(document)
    chapters = []
    for title in tableofcontent[1:]:  # skip first one
        headline = format_title(title)
        current_chapter, headline, rest = _content.partition(headline)
        _content = headline + rest
        chapters.append(current_chapter)
    chapters.append(_content)

    return tableofcontent, chapters, documentheader


def sections(document: Document):
    result = []
    for page in document.pages:
        result.extend(sections_from_page(page))
    return result


def toc(document: Document):
    """
    # TODO: Include page distance!
    """
    result = []
    for page in document.pages:
        result.extend(toc_from_page(page))

    # Title must occurs double, first in the TOC and after this, following in
    # the text.
    hundert_percent_toc = filter_double(result)
    return hundert_percent_toc


def toc_to_yaml(toc):
    termal = []
    for level, title in toc:
        level = 1 + level.count('.')  # TODO: NOT VERY STABLE
        termal.append(Section(level=level, title=title))

    return dump_toc(create_toc(termal))


def chapter_to_yaml(chapter):
    result = []
    for item in chapter:
        title, _, content = item.partition(NEWLINE)
        result.append({'title': title, 'content': content})
    return dump(result)


def toc_from_page(page: Page) -> List[RawSection]:
    """Extract headlines from page"""
    page_sections = sections_from_page(page)
    if not page_sections:
        raise ValueError('No sections in page: %s' % page)

    result = []
    # Filter non toc items, very simple rules!
    for index, item in enumerate(page_sections, start=0):
        if not item.title or not item.level:
            continue

        if item.title.count(NEWLINE) > 1:
            continue

        if item.title.count(' .') > 2 or item.title.count('...') > 2:
            result.append(index)
            continue

        # if len(item.title) > 120:
        #     continue

        result.append(index)
    group = group_segmentation(result)
    longest = [page_sections[index] for index in longest_group(group)]

    filtered = [(item.level, strip_title(item.title)) for item in longest]

    return filtered


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


def create_raw(headline: Tuple[str, str], text) -> RawSection:
    raw = RawSection()
    if text:
        raw.text = ''.join(text)
    if headline:
        raw.title = headline[1]
        raw.level = headline[0]
    return raw


def sections_from_page(page: Page):
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
    assert isinstance(line, str)
    matched = match(HEADLINE, line)
    if not matched:
        return None
    level = matched['level']
    if len(level) <= 2 and level[0].islower():
        return None
    return (level, matched['title'])
