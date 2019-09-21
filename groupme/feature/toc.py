# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing
from typing import List
from typing import Tuple

import utila
from iamraw import Document
from iamraw import Page
from iamraw import Section
from iamraw import create_toc
from serializeraw import dump_toc
from serializeraw import load_document

import groupme.toc
import groupme.toc.regex
from groupme.feature import RawSection
from groupme.structure import sections_from_page


"""
Outdated approaches:

  - collect title and check if sequence exists again in the document
"""


def work(documentpath: str) -> str:
    document = load_document(documentpath)
    result = toc(document)
    dumped = toc_to_yaml(result)
    return dumped


def toc(document: Document):
    """
    # TODO: Include page distance!
    # TODO: We need a more stable approach
    """
    utila.call('toc')

    result = []
    for index, page in enumerate(document.pages):
        utila.debug('page %d' % index)
        tocpage = groupme.toc.regex.parse_page(page)
        if tocpage is None:
            utila.log('empty page: %d' % index)
            continue
        result.extend(tocpage)

    # if headline occurs on table of content and on page it occurs twive
    result = groupme.toc.remove_duplication(result)
    return result


Level = str
Title = str


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


def filter_common_headlines(potential_titles: List[Tuple[Level, Title]]):
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


def text_snippets(document: Document):
    result = []
    for page in document:
        for item in page:
            try:
                # TODO: Why strip?
                result.append(item.text.strip())
            except AttributeError:
                pass
    return result


def toc_to_yaml(tableofcontent: typing.List[groupme.toc.TocLine]) -> str:
    # TODO: MOVE TO SERIALIZERAW
    outlines = []
    for line in tableofcontent:
        level = 1 + line.level.count('.')  # TODO: NOT VERY STABLE
        section = Section(level=level, title=line.title)
        outlines.append(section)
    dumped = dump_toc(create_toc(outlines))
    return dumped


def toc_from_page(page: Page) -> List[RawSection]:
    """Extract headlines from page"""
    page_sections = sections_from_page(page)
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

        if item.title.count(' .') > 2 or item.title.count('...') > 2:
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
