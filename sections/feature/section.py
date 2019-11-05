# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import dataclasses
import typing

import configo
import iamraw
import iamraw.sections
import serializeraw
import utila

import hey
import sections.feature.whitepage

# features with lower trust are not excepted as detected feaute
MIN_FEATURE_TRUST = configo.HV_PERCENT_PLUS(default=40).value

# multiple than one feature have this trust, acceppt all of them
MULTIPLE_FEATURE_TRUST = configo.HV_PERCENT_PLUS(default=90).value


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


def extract_sections(loaded: SectionsRequiredResources) -> iamraw.Sections:
    """Decide which `DocumentSection` is selected of the different
    feature extractor. If more than one feature suits very well, split
    page in different regions.

    Args:
        loaded: result of different `sections` steps
    Returns:
        `Sections` definition for given pages
    """
    result = collections.defaultdict(list)
    for pagenumber, content in hey.utils.sync([
            loaded.chapter,
            loaded.index,
            loaded.title,
            loaded.toc,
            loaded.whitepage,
    ]):
        trusted = most_trusted_items(content)

        if not trusted:
            # if trust is to low, the feature is not charactaristical enough,
            # therefore the page is treated as a normal text page
            result[pagenumber].append(
                iamraw.sections.Text(
                    start=pagenumber,
                    end=pagenumber,
                    trust=1.0,
                ))
            continue

        for index, item in enumerate(trusted):
            # TODO: Preseve order on page
            start = pagenumber + index * 1 / len(trusted)
            end = pagenumber + (index + 1) * 1 / len(trusted)

            ctor = BUILDER[content.index(item)]
            new = ctor(start=start, end=end, trust=item.content.value)

            result[pagenumber].append(new)
    grouped = group_sections(result)
    return grouped


def most_trusted_items(items: list) -> list:
    """Extract most trusted items on a page. There are multiple items
    possible.

    Accepted features must have a higher trust than `MIN_FEATURE_TRUST`.
    Multiple featues on a page require a much higher trust
    `MULTIPLE_FEATURE_TRUST`.

    Args:
        items: detected items on a page
    Returns:
        sorted list of accepted features, max trust stands on the top
    """
    items = list(items)

    items = sorted(
        items,
        key=lambda x: x.content.value if x and x.content else 0.0,
        reverse=True,
    )

    # remove features with to low trust
    items = [
        item for item in items
        if item and item.content and item.content.value >= MIN_FEATURE_TRUST
    ]

    # more than one feature on a page
    if len(items) > 1:
        multiple = [
            item for item in items if item and item.content and
            item.content.value >= MULTIPLE_FEATURE_TRUST
        ]
        assert len(multiple) >= 1
        items = multiple

    return items


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


def group_sections(items: AreaItems) -> iamraw.Sections:
    """Extend ranges of `AreaItems` to avoid empty regions between
    `AreaItems`. A empty region can be created if you have the titlepage
    and after this a blank page before continuing with table of content.
    """
    result = iamraw.Sections()
    current = None
    chapter = 1
    for page, content in items.items():
        for item in content:
            next_ = determine_document_section(current, item)
            if is_new_area(current, next_):
                current = next_(start=page, end=page, trust=1.0)
                result.content.append(current)  # pylint:disable=E1101
            else:
                # increase section end
                current.end = page

            if isinstance(item, iamraw.sections.Chapter):
                # set chapter level
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


def chapters(sections: iamraw.Sections):
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
    return 'section'
