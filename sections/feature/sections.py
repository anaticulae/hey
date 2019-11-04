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

import iamraw
import iamraw.sections
import serializeraw
import utila

import hey
import sections.feature.whitepage

MIN_FEATURE_TRUST = 0.4  # Holy value


@utila.checkdatatype
def work(
        chapter: str,
        index: str,
        title: str,
        toc: str,
        whitepage: str,
        pages: list = None,
) -> str:
    """Combine different featuretypes to determine the page type with more
    confidence.

    Args:
        chapter(str): path to chapter extraction
        index(str): path to index extraction
        title(str): path to title extraction
        toc(str): path to toc extraction
        whitepage(str): path to whitepage extraction
        pages: select pages for processing
    Returns:
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
    dumped = serializeraw.dump_sections(extracted)
    return dumped


@dataclasses.dataclass
class SectionsRequiredResources:
    chapter: iamraw.PageContentLikelihoods
    index: iamraw.PageContentLikelihoods
    title: iamraw.PageContentLikelihoods
    toc: iamraw.PageContentLikelihoods
    whitepage: typing.List[iamraw.sections.WhitePage]



def extract_sections(loaded: SectionsRequiredResources) -> iamraw.sections.Sections: # yapf:disable
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
            result[number] = iamraw.sections.Text(
                start=number,
                end=number,
                trust=1.0,
            )
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
    iamraw.sections.Chapter,
    iamraw.sections.Index,
    iamraw.sections.TitlePage,
    iamraw.sections.TableOfContent,
    iamraw.sections.WhitePage,
]


def is_new_area(current, next_):
    current_class = current.__class__
    next_class = next_ if callable(next_) else next_.__class__
    return current_class != next_class


AreaItems = typing.List[iamraw.sections.AreaItem]


def group_sections(items: AreaItems) -> iamraw.sections.Sections:
    result = iamraw.sections.Sections()
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
        if isinstance(item, iamraw.sections.Chapter):
            item.number = chapter
            chapter += 1
        current.content.append(item)
    return result


# do not change DocumentSection
# iamraw.sections.DocumentSection
#       iamraw.sections.Text
#       iamraw.sections.WhitePage:
MATCHING = {
    iamraw.sections.Chapter: iamraw.sections.Content,
    iamraw.sections.Index: iamraw.sections.Table,
    iamraw.sections.TableOfContent: iamraw.sections.Table,
    iamraw.sections.Text: iamraw.sections.DocumentSection,
    iamraw.sections.TitlePage: iamraw.sections.Introduction,
    iamraw.sections.WhitePage: iamraw.sections.DocumentSection
}


def determine_document_section(
        current: iamraw.sections.DocumentSection,
        actual: iamraw.sections.AreaItem,
):
    next_ = MATCHING[type(actual)]
    if next_ == iamraw.sections.DocumentSection:
        if not current:
            return iamraw.sections.Unknown
        return current
    return next_


def load_features(
        chapter,
        index,
        title,
        toc,
        whitepage,
        pages=None,
):
    chapter = serializeraw.load_likelihood(chapter, pages=pages)

    index = serializeraw.load_likelihood(index, pages=pages)
    title = serializeraw.load_likelihood(title, pages=pages)
    toc = serializeraw.load_likelihood(toc, pages=pages)

    whitepage = sections.feature.whitepage.load_whitepages(
        whitepage,
        pages=pages,
    )

    result = SectionsRequiredResources(
        chapter=chapter,
        index=index,
        title=title,
        toc=toc,
        whitepage=whitepage,
    )
    return result


def chapters(sections: iamraw.sections.Sections):
    content = [
        item for item in sections if isinstance(item, iamraw.sections.Content)
    ]
    if not content:
        # no content in document
        return []

    result = []
    for area in content:
        for chapter in area:
            result.append((chapter.start, chapter.end))

    return result


def commandline():
    return utila.Flag(
        longcut=name(),
        message='extract document structure from pdf file',
    )


def name():
    return 'sections'
