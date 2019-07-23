# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import exists
from typing import List

from iamraw.sections import AreaItem
from iamraw.sections import Chapter
from iamraw.sections import Content
from iamraw.sections import DocumentSection
from iamraw.sections import Index
from iamraw.sections import Introduction
from iamraw.sections import Sections
from iamraw.sections import Table
from iamraw.sections import TableOfContent
from iamraw.sections import Text
from iamraw.sections import TitlePage
from iamraw.sections import Unknown
from iamraw.sections import WhitePage
from serializeraw import dump_sections
from serializeraw import load_likelihood
from utila import FAILURE
from utila import Flag
from utila import checkdatatype
from utila import error

from sections.feature.chapter import chapter_value_to_percent
from sections.feature.chapter import load_chapter_detection
from sections.feature.whitepage import load_whitepages
from sections.feature.whitepage import whitepage_value_to_percent

MIN_FEATURE_TRUST = 0.4  # Holy value


@checkdatatype
def work(
        chapter: str,
        index: str,
        title: str,
        toc: str,
        whitepage: str,
) -> str:
    """Combine different featuretypes to determine the page type with more
    confidence.

    Args:
        chapter(str): path to chapter extraction
        index(str): path to index extraction
        title(str): path to title extraction
        toc(str): path to toc extraction
        whitepage(str): path to whitepage extraction
    Retruns:
        dumped `Section`
    """

    # TODO: Add @checkfile decorator to utila, to ensure that files exists
    # TODO: Investigate add check if raw content or file path is used
    # failure = False
    # for item in [chapter, index, title, toc, whitepage]:
    #     if not exists(item):
    #         error('sections: missing input %s' % item)
    #         failure = True
    # if failure:
    #     exit(FAILURE)
    potential_features = load_features(
        chapter,
        index,
        title,
        toc,
        whitepage,
    )
    # work
    extracted = extract_sections(*potential_features)

    # save
    dumped = dump_sections(extracted)
    return dumped


def extract_sections(
        chapter,
        index,
        title,
        toc,
        whitepage,
) -> Sections:
    result = []
    for number, page in enumerate(zip(chapter, index, title, toc, whitepage)):
        # TODO:  What if more than one item is max? 1.0, 1.0?
        value = max(page)
        if value < MIN_FEATURE_TRUST:
            # if trust is to low, the feature is not charactaristical enough,
            # therefore the page is treated as a normal text page
            result.append(Text(start=number, end=number, trust=1.0))
            continue
        ctor = BUILDER[page.index(value)]
        result.append(ctor(
            start=number,
            end=number,
            trust=value,
        ))

    grouped = group_sections(result)
    return grouped


BUILDER = [
    Chapter,
    Index,
    TitlePage,
    TableOfContent,
    WhitePage,
]


def is_new_area(current, next_):
    current_class = current.__class__
    next_class = next_ if callable(next_) else next_.__class__
    return current_class != next_class


def group_sections(items: List[AreaItem]) -> Sections:
    result = Sections()
    current = None
    chapter = 1
    for page, item in enumerate(items):
        next_ = determine_document_section(current, item)
        if is_new_area(current, next_):
            current = next_(start=page, end=page, trust=1.0)
            result.content.append(current)
        else:
            # increase section end
            current.end = page
        if isinstance(item, Chapter):
            item.number = chapter
            chapter += 1
        current.content.append(item)
    return result


MATCHING = {
    Chapter: Content,
    Index: Table,
    TableOfContent: Table,
    Text: DocumentSection,  # do not change DocumentSection
    TitlePage: Introduction,
    WhitePage: DocumentSection  # do not change DocumentSection
}


def determine_document_section(current: DocumentSection, actual: AreaItem):
    next_ = MATCHING[type(actual)]
    if next_ == DocumentSection:
        if not current:
            return Unknown
        return current
    return next_


def load_features(chapter, index, title, toc, whitepage):

    chapter = load_chapter_detection(chapter)
    chapter = [chapter_value_to_percent(item) for item in chapter]

    index = load_likelihood(index)
    title = load_likelihood(title)
    toc = load_likelihood(toc)

    whitepage = load_whitepages(whitepage)
    whitepage = [whitepage_value_to_percent(item) for item in whitepage]

    return chapter, index, title, toc, whitepage


def chapters(sections: Sections):
    content = [item for item in sections if isinstance(item, Content)]
    if not content:
        # no content in document
        return []

    result = []
    for area in content:
        for chapter in area:
            result.append((chapter.start, chapter.end))

    return result


def commandline():
    return Flag(
        longcut=name(),
        message='extract document structure from pdf file',
    )


def name():
    return 'sections'
