# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import typing
from typing import List

import iamraw
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
from utila import Flag
from utila import checkdatatype

import hey
from sections.feature.whitepage import load_whitepages

MIN_FEATURE_TRUST = 0.4  # Holy value


@checkdatatype
def work(
        chapter: str,
        index: str,
        title: str,
        toc: str,
        whitepage: str,
        pages=None,
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
    loaded = load_features(
        chapter,
        index,
        title,
        toc,
        whitepage,
        pages=pages,
    )
    # work
    extracted = extract_sections(loaded)

    # save
    dumped = dump_sections(extracted)
    return dumped


@dataclasses.dataclass
class SectionsRequiredResources:
    chapter: iamraw.PageContentLikelihoods
    index: iamraw.PageContentLikelihoods
    title: iamraw.PageContentLikelihoods
    toc: iamraw.PageContentLikelihoods
    whitepage: typing.List[WhitePage]


def extract_sections(loaded: SectionsRequiredResources) -> Sections:
    result = {}
    for number, content in hey.utils.sync([
            loaded.chapter,
            loaded.index,
            loaded.title,
            loaded.toc,
            loaded.whitepage,
    ]):
        # for number, page in enumerate(zip(chapter, index, title, toc, whitepage)):
        # TODO:  What if more than one item is max? 1.0, 1.0?
        max_item = max(
            content, key=lambda x: x.content.value if x and x.content else 0.0)
        if not max_item or max_item.content.value < MIN_FEATURE_TRUST:
            # if trust is to low, the feature is not charactaristical enough,
            # therefore the page is treated as a normal text page
            result[number] = Text(start=number, end=number, trust=1.0)
            continue
        ctor = BUILDER[content.index(max_item)]
        result[number] = ctor(
            start=number,
            end=number,
            trust=max_item.content.value,
        )
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
    for page, item in items.items():
        next_ = determine_document_section(current, item)
        if is_new_area(current, next_):
            current = next_(start=page, end=page, trust=1.0)
            result.content.append(current)  # pylint:disable=E1101
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


def load_features(chapter, index, title, toc, whitepage, pages=None):
    chapter = load_likelihood(chapter, pages=pages)

    index = load_likelihood(index, pages=pages)
    title = load_likelihood(title, pages=pages)
    toc = load_likelihood(toc, pages=pages)

    whitepage = load_whitepages(whitepage, pages=pages)

    result = SectionsRequiredResources(
        chapter=chapter,
        index=index,
        title=title,
        toc=toc,
        whitepage=whitepage,
    )
    return result


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
