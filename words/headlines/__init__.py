# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import abc
import re
import typing
import warnings

import iamraw
import utila
from iamraw import PageSizeBorder
from serializeraw import dump_headlines
from serializeraw import load_document
from serializeraw import load_horizontals
from serializeraw import load_pageborders
from serializeraw import load_sections

import groupme.feature.footer
import groupme.footer
import groupme.toc.regex
import hey.textnavigator.navigator
import hey.utils
import sections.feature.sections
import words
from hey.document import BorderList
from hey.document import document_border
from hey.fonts.store import FontStore
from hey.fonts.store import create_fontstore
from hey.textnavigator.fonts import fontdistance_textbounds
from hey.textnavigator.fonts import fontsize_from_textbounds
from hey.textnavigator.navigator import PageTextContentNavigator
from hey.textnavigator.navigator import PageTextNavigators
from hey.textnavigator.navigator import create_pagetextnavigators
from hey.textnavigator.navigator import navigator_to_bounds

"""
TODO:
    add more than one strategy to compute equal footer, header
    and different footer with and without header
"""

WHITELIST = set([
    'Anhang',
    'Eidesstattliche Erklärung',
    'Literaturverzeichnis',
])


class HeadlineExtractorStrategy(abc.ABC):

    def __init__(
            self,
            sectionlist: typing.List[sections.feature.sections.Sections],
            pagetextnavigators: PageTextNavigators,
            fontstore: hey.fonts.store.FontStore,
            sizeandborder,
            headerfooters,
            chapters,
    ):
        self.__result = {}

        self.sectionlist = sectionlist
        self.pagetextnavigators = pagetextnavigators
        self.fontstore = fontstore
        self.sizeandborder = sizeandborder
        self.headerfooters = headerfooters
        self.chapters, self.content = prepare_chapter_and_content(
            sectionlist,
            chapters,
        )
        # bounding box of text content
        self.border = contentborder(
            self.sizeandborder,
            self.headerfooters,
        )

        self.setup()
        self.ready = False

    def result(self):
        if self.ready:
            return self.__result
        self.ready = True

        # run extraction
        for chapter in self.chapters:
            self.extract_chapter(chapter)

        # filter result
        self.__result = self.filter(self.__result)
        extracted = [item for item in self.__result.values()]
        return extracted

    def filter(self, items):
        """Convert level etc."""
        # TODO: IMprove this
        convert_level(items)
        return items

    def setup(self):
        """Run before starting extraction."""
        self.textsize = hey.textnavigator.fonts.document_textsize(
            navigators=self.pagetextnavigators,
            borders=self.sizeandborder,
        )
        self.textdistance = hey.textnavigator.fonts.document_textdistance(
            navigators=self.pagetextnavigators,
            borders=self.sizeandborder,
        )

    def extract_chapter(self, chapter: int):
        assert 0 <= chapter < self.chaptercount, chapter
        result = []
        start, end = self.content[chapter]
        for page in range(start, end + 1):
            pagecontent = PageTextContentNavigator(
                utila.select_page(self.pagetextnavigators, page=page),
                utila.select_page(self.border, page=page),
            )
            pageheadlines = self.extract_page(
                page,
                pagecontent,
            )
            result.extend(pageheadlines)
        self.__result[chapter] = result

    def extract_page(
            self,
            page,
            pagecontent,
    ):
        result = []
        xoff = pagecontent.offset[0]
        xoff = xoff if xoff is not None else 0
        bounds = navigator_to_bounds(pagecontent)
        bounds = hey.textnavigator.fonts.textbounds(
            pagecontent,
            utila.select_page(self.border, page=page),
        )
        without_content = [item[0] for item in bounds]
        # PageContentNavigator, the header and footer is ignored
        textdistances = fontdistance_textbounds(without_content)
        for containerid, (textbounds, text) in enumerate(
                bounds,
                start=xoff,
        ):
            splitted = text.splitlines()
            if len(splitted) > 1:
                continue
            headline = self.extract_headline(
                text=text,
                textbounds=textbounds,
                textdistances=textdistances,
                page=page,
                containerid=containerid,
                contentstart=xoff,
            )
            if not headline:
                continue
            result.append(headline)
        return result

    @abc.abstractmethod
    def extract_headline(
            self,
            text,
            textbounds,
            textdistances,
            page,
            containerid,
            contentstart,
    ):
        return None

    @property
    def chaptercount(self):
        return len(self.chapters)


def prepare_chapter_and_content(sections_, chapter):
    assert isinstance(sections_, sections.feature.sections.Sections)
    assert sections_, 'no sections provided'
    if chapter is None:
        # process all chapter
        # TODO: clearify code
        content = determine_content_border(sections_)
        chapter = list(range(len(content)))
    else:
        content = sections.feature.sections.chapters(sections_)
        chapter = [chapter] if isinstance(chapter, int) else chapter
    return chapter, content


def contentborder(sizeandborders, headerfooters):
    assert all([isinstance(item, PageSizeBorder) for item in sizeandborders])
    result = {}
    pages = [item.page for item in sizeandborders]
    for page in pages:
        pageborder = utila.select_page(sizeandborders, page).border
        footerheader = utila.select_page(headerfooters, page)
        footerheader = hey.utils.select_content(footerheader, (None, None))

        top = footerheader[0] if footerheader[0] else 0
        bottom = footerheader[1] if footerheader[1] else pageborder.bottom

        result[page] = iamraw.Border(
            left=pageborder.left,
            right=pageborder.right,
            top=top,
            bottom=bottom,
        )
    return result


HORIZONTAL_MIN_COUNT = 5  # TODO: HOLY VALUES
FIRST_LEVEL = 0.9  # TODO: HOLY VALUE
SECOND_LEVEL = 0.7


def convert_level(result: iamraw.PagesHeadlineList) -> int:
    """Convert chapter level based on text distances to logical level
    (1,2,3,4,...).

    Hint: This function updates the level
    TODO: copy items
    """

    # pylint:disable=len-as-condition
    utila.call('convert_level')
    utila.info('empty PageHeadlineList')
    if not result:
        return result

    if not any(result):
        return {}
    assert isinstance(result, dict), type(result)

    maxsize = max([
        max([item.level
             for item in chapter])
        for chapter in result.values()
        if chapter
    ])
    # TODO: check this approach
    first_level = FIRST_LEVEL * maxsize
    second_level = SECOND_LEVEL * maxsize

    def get_level(value):
        if value >= first_level:
            return 1
        if value >= second_level:
            return 2
        return 3

    # TODO: copy elements
    for items in result.values():
        for item in items:
            item.level = get_level(item.level)
    return result


def determine_content_border(items):
    # analyze all chapter of the document
    contents = [
        item for item in items
        if isinstance(item, sections.feature.sections.Content)
    ]
    # support more than one content element
    chapters = [[
        chapter
        for chapter in content.content
        if isinstance(chapter, iamraw.sections.Chapter)
    ]
                for content in contents]
    chapters = utila.flatten(chapters)

    if not chapters:
        # TODO: INVESTIGATE HERE
        return []

    result = []
    for current, after in zip(chapters[:-1], chapters[1:]):
        # TODO: check after.start - 1 later
        result.append((current.start, after.start - 1))
    result.append((chapters[-1].start, contents[-1].end))

    # ensure ascending page numbers
    assert all([start <= end for start, end in result]), str(result)
    return result
