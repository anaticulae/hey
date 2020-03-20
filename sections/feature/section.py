# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import functools
import typing

import configo
import iamraw
import iamraw.sections
import serializeraw
import utila

import hey.utils
import sections.path

# features with lower trust are not expected as detected feature
MIN_FEATURE_TRUST = configo.HV_PERCENT_PLUS(default=40).value

# more than one feature have this trust, accept all of them
MULTIPLE_FEATURE_TRUST = configo.HV_PERCENT_PLUS(default=75).value


@utila.checkdatatype
def work(
        abbreviation: str,
        bibliography: str,
        chapter: str,
        index: str,
        legal: str,
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
        abbreviation,
        bibliography,
        chapter,
        index,
        legal,
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
    abbreviation: iamraw.PageContentLikelihoods
    bibliography: iamraw.PageContentLikelihoods
    chapter: iamraw.PageContentLikelihoods
    index: iamraw.PageContentLikelihoods
    legal: iamraw.PageContentLikelihoods
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
    result = {}
    for pagenumber, content in hey.utils.sync([
            loaded.abbreviation,
            loaded.bibliography,
            loaded.chapter,
            loaded.index,
            loaded.legal,
            loaded.title,
            loaded.toc,
            loaded.whitepage,
    ]):
        trusted = most_trusted_items(content)

        if not trusted:
            # if trust is to low, the feature is not charactaristical enough,
            # therefore the page is treated as a normal text page
            result[pagenumber] = iamraw.sections.Text(
                start=pagenumber,
                end=pagenumber,
                trust=1.0,
            )
            continue

        def create(start, end, trust, typ):
            ctor = BUILDER[typ]
            new = ctor(start=start, end=end, trust=trust)
            return new

        if len(trusted) > 1:
            multiple = iamraw.MultipleSection(
                start=pagenumber,
                end=pagenumber,
                trust=1.0,
            )
            for index, item in enumerate(trusted):
                # TODO: Preseve order on page
                start = pagenumber + index * 1 / len(trusted)
                end = pagenumber + (index + 1) * 1 / len(trusted)
                new = create(
                    start=start,
                    end=end,
                    trust=item.content.value,
                    typ=content.index(item),
                )
                multiple.content.append(new)  # pylint:disable=E1101
            result[pagenumber] = multiple
        else:
            item = trusted[0]
            new = create(
                start=pagenumber,
                end=pagenumber,
                trust=item.content.value,
                typ=content.index(item),
            )
            result[pagenumber] = new

    grouped = group_sections(result)
    return grouped


def most_trusted_items(items: list) -> list:
    """Extract most trusted items on a page. There are multiple items
    possible.

    Accepted features must have a higher trust than `MIN_FEATURE_TRUST`.
    Multiple features on a page require a much higher trust
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
        # TODO: SEARCH FOR A BETTER APROACH, NEED MORE INFORMATION
        # THIS ASSERT SEAMS NOT TO BE USEFUL
        # assert len(multiple) >= 1, str(items)
        if multiple:
            items = multiple
    return items


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
    for page, item in items.items():
        next_ = determine_document_section(current, item)
        if not current and isinstance(item, iamraw.MultipleSection):
            # Multiple section on the start of the document
            # TODO: HOW TO HANDLE MULTIPLE SECTION IN THE MIDDLE OF THE DOCUMENT?
            current = item
            result.content.append(item)  # pylint:disable=E1101
            continue
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


@dataclasses.dataclass
class Abbreviation(iamraw.sections.AreaItem):
    pass


@dataclasses.dataclass
class Bibliography(iamraw.sections.AreaItem):
    pass


@dataclasses.dataclass
class Legal(iamraw.sections.AreaItem):
    pass


BUILDER = [
    Abbreviation,
    Bibliography,
    iamraw.sections.Chapter,
    iamraw.sections.Index,
    Legal,
    iamraw.sections.TitlePage,
    iamraw.sections.TableOfContent,
    iamraw.sections.WhitePage,
]

# do not change DocumentSection
# iamraw.sections.DocumentSection
#       iamraw.sections.Text
#       iamraw.sections.WhitePage:
MATCHING = {
    Abbreviation: iamraw.sections.Appendix,
    Bibliography: iamraw.sections.Appendix,
    Legal: iamraw.sections.Appendix,
    iamraw.MultipleSection: iamraw.MultipleSection,
    iamraw.sections.Chapter: iamraw.MainPart,
    iamraw.sections.Index: iamraw.sections.Table,
    iamraw.sections.TableOfContent: iamraw.sections.Table,
    iamraw.sections.Text: iamraw.sections.DocumentSection,
    iamraw.sections.TitlePage: iamraw.sections.Introduction,
    iamraw.sections.WhitePage: iamraw.sections.DocumentSection,
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


@functools.lru_cache(configo.CACHE_SMALL)
def load_features(
        abbreviation,
        bibliography,
        chapter,
        index,
        legal,
        title,
        toc,
        whitepage,
        pages=None,
) -> SectionsRequiredResources:
    abbreviation = serializeraw.load_likelihood(abbreviation, pages=pages)
    bibliography = serializeraw.load_likelihood(bibliography, pages=pages)
    chapter = serializeraw.load_likelihood(chapter, pages=pages)
    index = serializeraw.load_likelihood(index, pages=pages)
    legal = serializeraw.load_likelihood(legal, pages=pages)
    title = serializeraw.load_likelihood(title, pages=pages)
    toc = serializeraw.load_likelihood(toc, pages=pages)
    white = serializeraw.load_whitepages(whitepage, pages=pages)

    result = SectionsRequiredResources(
        abbreviation=abbreviation,
        bibliography=bibliography,
        chapter=chapter,
        index=index,
        legal=legal,
        title=title,
        toc=toc,
        whitepage=white,
    )
    return result


def chapters(root: iamraw.Sections):
    content = [item for item in root if isinstance(item, iamraw.MainPart)]
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


def load_section_likelihood_frompath(path: str, pages: tuple = None):
    # TODO: we need to improve this
    loaded = load_features(
        sections.path.abbreviation(path),
        sections.path.bibliography(path),
        sections.path.chapter(path),
        sections.path.index(path),
        sections.path.legal(path),
        sections.path.title(path),
        sections.path.toc(path),
        sections.path.whitepage(path),
        pages=pages,
    )
    result = extract_sections(loaded)
    return result


def extract_sections_frompath(
        path: str,
        prefix: str = '',
        pages: tuple = None,
) -> iamraw.Sections:
    import sections.feature.chapter
    import sections.feature.abbreviation
    import sections.feature.bibliography
    import sections.feature.legal
    import sections.feature.title
    import sections.feature.index
    import sections.feature.toc
    import sections.feature.whitepage
    text = iamraw.path.text(path, prefix=prefix)
    textposition = iamraw.path.textposition(path, prefix=prefix)
    toc = iamraw.path.toc(path, prefix=prefix)
    fontheader = iamraw.path.fontheader(path, prefix=prefix)
    fontcontent = iamraw.path.fontcontent(path, prefix=prefix)
    footers = iamraw.path.headerfooters(path, prefix=prefix)

    chapter = sections.feature.chapter.work(
        text,
        textposition,
        toc,
        pages=pages,
    )
    abbreviation = sections.feature.abbreviation.work(
        text,
        textposition,
        pages=pages,
    )
    bibliography = sections.feature.bibliography.work(
        text,
        textposition,
        pages=pages,
    )
    legal = sections.feature.legal.work(text, textposition, pages=pages)
    index = sections.feature.index.work(text, pages=pages)
    title = sections.feature.title.work(
        text,
        fontheader,
        fontcontent,
        pages=pages,
    )
    toc = sections.feature.toc.work(text, pages=pages)
    whitepage = sections.feature.whitepage.work(
        text,
        textposition,
        footers=footers,
        pages=pages,
    )
    loaded = load_features(
        abbreviation,
        bibliography,
        chapter,
        index,
        legal,
        title,
        toc,
        whitepage,
        pages=pages,
    )
    # work
    result = extract_sections(loaded)
    return result
