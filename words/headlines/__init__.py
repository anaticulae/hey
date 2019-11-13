# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import abc
import typing

import iamraw
import iamraw.sections
import utila

import hey.fonts.store
import hey.textnavigator.fonts
import hey.textnavigator.navigator
import sections.feature.section
import words.feature
import words.loader.basic
import words.utils.skipper

WHITELIST = set([
    'Anhang',
    'Eidesstattliche Erklärung',
    'Literaturverzeichnis',
])


class HeadlineExtractorStrategy(abc.ABC):

    def __init__(
            self,
            sectionlist: typing.List[iamraw.Sections],
            basic: words.loader.basic.BasicRequiredResources,
            chapters,
    ):
        self.__result = {}

        self.sectionlist = sectionlist
        self.pagetextnavigators = basic.textnavigators
        self.fontstore = basic.fontstore
        self.sizeandborder = basic.sizeandborder
        self.headerfooters = basic.headerfooters
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

    def result(self, pages=None):
        if self.ready:
            return self.__result
        self.ready = True

        # run extraction
        for chapter in self.chapters:
            # TODO: replace with utila code
            if words.utils.skipper.should_skip(self.content[chapter], pages):
                continue
            self.extract_chapter(chapter)

        # filter result
        self.__result = self.filter(self.__result)
        extracted = [item for item in self.__result.values()]
        return extracted

    def filter(self, items):  # pylint:disable=R0201
        """Convert level etc."""
        # TODO: IMprove this
        convert_level(items)
        return items

    def setup(self):
        """Run before starting extraction."""
        self.textsize = hey.textnavigator.fonts.document_textsize(
            navigators=self.pagetextnavigators,)

        self.textdistance = hey.textnavigator.fonts.document_textdistance(
            navigators=self.pagetextnavigators,
            borders=self.sizeandborder,
        )

    def extract_chapter(self, chapter: int):
        assert 0 <= chapter < self.chaptercount, chapter
        result = []
        start, end = self.content[chapter]
        for page in range(start, end + 1):
            textnavi = utila.select_page(self.pagetextnavigators, page=page)
            border = utila.select_page(self.border, page=page)
            if not border:
                # empty page
                continue
            pagecontent = hey.textnavigator.navigator.PageTextContentNavigator(
                textnavi,
                border,
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
        xoff, xend = pagecontent.offset
        xoff = xoff if xoff is not None else 0
        bounds = hey.textnavigator.fonts.textbounds(
            pagecontent,
            utila.select_page(self.border, page=page),
        )
        without_content = [item.bounds for item in bounds]
        # PageContentNavigator, the header and footer is ignored
        textdistances = hey.textnavigator.fonts.fontdistance_textbounds(
            without_content)

        textfeeds = [item.bounds.xdist for item in bounds]

        for containerid, item in enumerate(
                pagecontent,
                start=xoff,
        ):
            splitted = item.text.splitlines()
            if len(splitted) > 1:
                continue
            headline = self.extract_headline(
                textinfo=item,
                textdistances=textdistances,
                textfeeds=textfeeds,
                page=page,
                containerid=containerid,
                content_range=(xoff, xend),
            )
            if not headline:
                continue
            result.append(headline)
        return result

    def extract_headline(
            self,
            textinfo,
            textdistances,
            textfeeds,
            page,
            containerid,
            content_range,
    ):
        text = textinfo.text
        contentstart, contentend = content_range
        distanceid = containerid - contentstart
        fontdistance = textdistances[distanceid]
        textfeed = textfeeds[distanceid]
        textsize = hey.textnavigator.style.TextStyle.textsizes(textinfo.style)

        distance_tosmall = fontdistance < self.smallest_headlinedistance()
        headline_tosmall = textsize < self.smallest_textsize()
        lastitem = (distanceid + 1) == contentend

        skip = self.should_skip(
            distance_tosmall=distance_tosmall,
            headline_tosmall=headline_tosmall,
            textfeed=textfeed,
            lastitem=lastitem,
        )

        utila.debug(f'{self.__class__.__name__}: {skip} {text}')
        if skip:
            return None

        dist_top = textdistances[distanceid]
        dist_bottom = None if lastitem else textdistances[distanceid + 1]
        level = self.levelme(textsize, dist_top, dist_bottom)

        text = text.strip()
        headline = iamraw.Headline(
            container=containerid,
            level=level,
            page=page,
            text=text,
        )
        return headline

    @abc.abstractmethod
    def should_skip(
            self,
            distance_tosmall,
            headline_tosmall,
            textfeed,
            lastitem,
    ):
        pass

    def levelme(
            self,
            textsize: float,  # pylint:disable=W0613
            dist_top: float,
            dist_bottom: float,
    ) -> float:
        level = dist_top
        if dist_bottom is None:
            # Headline is alone on the page end
            level = level * 2
        else:
            level = level + dist_bottom
        return level

    @property
    def chaptercount(self):
        return len(self.chapters)

    @abc.abstractmethod
    def smallest_headlinedistance(self):
        pass

    @abc.abstractmethod
    def smallest_textsize(self):
        pass


def prepare_chapter_and_content(sections_, chapter):
    assert isinstance(sections_, iamraw.Sections)
    assert sections_, 'no sections provided'
    if chapter is None:
        # process all chapter
        # TODO: clearify code
        content = determine_content_border(sections_)
        chapter = list(range(len(content)))
    else:
        content = sections.feature.section.chapters(sections_)
        chapter = [chapter] if isinstance(chapter, int) else chapter
    return chapter, content


def contentborder(sizeandborders, headerfooters):
    assert all([isinstance(it, iamraw.PageSizeBorder) for it in sizeandborders])
    result = {}
    pages = [item.page for item in sizeandborders]
    for page in pages:
        selected = utila.select_page(sizeandborders, page)
        pageheight = selected.size.height
        pageborder = selected.border
        footerheader = utila.select_page(headerfooters, page)

        if footerheader is None:
            continue

        top = 0
        if footerheader.header:
            top = pageheight * footerheader.header.end

        bottom = pageheight
        if footerheader.footer:
            bottom = pageheight * footerheader.footer.begin

        top, bottom = utila.roundme(top), utila.roundme(bottom)

        result[page] = iamraw.Border(
            left=pageborder.left,
            right=pageborder.right,
            top=top,
            bottom=bottom,
        )
    return result


FIRST_LEVEL = 0.8  # TODO: HOLY VALUE
SECOND_LEVEL = 0.5


def convert_level(result: iamraw.PagesHeadlineList) -> int:
    """Convert chapter level based on text distances to logical level
    (1,2,3,4,...).

    Hint: This function updates the level
    TODO: copy items
    """

    # pylint:disable=len-as-condition
    utila.call('convert_level')
    if not result:
        return result

    if not any(result):
        utila.info('empty PageHeadlineList')
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
    contents = [item for item in items if isinstance(item, iamraw.MainPart)]
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
